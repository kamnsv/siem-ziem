"""
    ZIEM
    Камнев Сергей
    Модуль Отпрвка в отдельной задаче

"""
import os
import json
import psutil
import asyncio
import logging
from datetime import datetime
from ziem.core.db import readjson, log_error, get_db, write_db


from .sender import Sender

class Single:
    """
    Генерация отчета каждые 30 минут
    """
    def __init__(self, name='SenderReport'):
        self.db = get_db()
        self.rperiod = int(os.getenv('ZIEM_REPORT_PERIOD', '1800'))
        raw = readjson('/var/opt/ziem/conf/settings.json')
        self.sender = None
        for sender in raw['senders']:
            if sender['name'] == name:
                self.sender = Sender(sender)
                break
        else:
            logging.debug(f'Параметры для инициализации сендера "{name}" не найдены')
        
            
    async def run(self):
        # отчет о работе ZIEM
        if not self.sender: return
        try:
            self.time = datetime.now()
            while True:
                await asyncio.sleep(self.rperiod)
                if not self.sender.enabled: continue
                await self.get_data()
                await self.write_data()
                await self.sender('incs', self.data)
        except Exception as e:
            log_error(e, '1205')

            
            
    async def get_data(self):
        count_alert = await self.db['alerts'].count_documents({'alr_time': {'$gte': self.time}})
        count_event = await self.db['events'].count_documents({'time': {'$gte': self.time}})
        count_inc = await self.db['incs'].count_documents({'inc_time': {'$gte': self.time}})
        self.time = datetime.now()
        self.get_procmem()
        self.get_cpu()
        self.get_hdd()
        self.get_mem()
        self.get_dataerror()
        event = {
            'time' : self.time,
            'ziem_mem': self.proc_mem,
            'cpu_load': self.cpu,
            'hdd_load': self.hdd,
            'mem_load': self.mem,
            'count_alert': count_alert,
            'count_event': count_event,
            'count_inc': count_inc,
            'data_error': self.data_error,
            'count_error': len(self.data_error),
        }
        self.data = {
            'inc_time': self.time,
            'inc_name': 'ZIEM_Report',
            'inc_mesg': 'Служебная информация по работе ZIEM',
            'inc_crit': 'None',
            'events': event,
        }

    async def write_data(self):
        await self.db['report'].insert_one(self.data['events'])

        
    def get_dataerror(self):
        self.data_error = []
        with open('/var/log/ziem/ziem.log', 'r') as f:
            data_raw = f.readlines()
        data = []
        for d_raw in data_raw:
            if len(d_raw) > 1:
                if d_raw[0] == '~':
                    d = d_raw.split('~')
                    if len(d) > 6:
                        d_time = datetime.strptime(d[1], '%m-%d-%Y %H:%M:%S')
                        if d_time > time:
                            if d[2] == 'ERROR':
                                self.data_error.append(d_raw)    
    
    def get_procmem(self):
        pid = int(os.popen('systemctl show --property MainPID --value ziemcored').read())
        if pid != 0:
            self.proc_mem = int(psutil.Process(int(pid)).memory_info().rss / 1024 / 1024)
        else:
            self.proc_mem = 0

            
    def get_mem(self):
        # информация о памяти
        mem = psutil.virtual_memory()
        self.mem = int((mem.total - mem.available)/mem.total * 100) 

        
    def get_hdd(self):
        # информация о жестком
        hdd_root = psutil.disk_usage('/')
        hdd_home = psutil.disk_usage('/home')
        hdd_var = psutil.disk_usage('/var')
        used = hdd_root.used + hdd_home.used + hdd_var.used
        total = hdd_root.total + hdd_home.total + hdd_var.total
        self.hdd = int(used/total*100)

        
    def get_cpu(self):
        # информация о процессоре
        self.cpu = int(psutil.getloadavg()[2] / psutil.cpu_count() * 100)    