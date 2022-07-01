"""
    ZIEM
    Бенгарт Захар

    Модуль Отправки данных и Генерации отчета

"""
import sys
sys.path.append("..")

import os
import json
import psutil
import aiohttp
import asyncio
import logging
import socket
from datetime import datetime
from datetime import timedelta
from asyncua import Client, Node, ua
from aiohttp import TCPConnector
from core.db import readjson, log_error, get_db, write_db
from logging.handlers import RotatingFileHandler
import logging.handlers

def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logging.error(f"Exception: {msg}")


class PosterBase:
    """
    Базовый класс для чтения настроек
    """

    def __init__(self):
        self.tasks = {}
        self.db = get_db()
        raw = readjson('/var/opt/ziem/conf/settings.json')
        if 'sender_ip' in raw:
            self.sender_ip = raw['sender_ip']
            if 'sender_port' in raw:
                if raw['sender_port']:
                    self.sender_ip += ':' + raw['sender_port']
        if 'opc_ip' in raw:
            self.opc_ip = raw['opc_ip']
            if 'opc_port' in raw:
                if raw['opc_port']:
                    self.opc_ip += ':' + raw['opc_port']
        if 'cor_name' in raw:
            self.cor_name = raw['cor_name']

    def readjson(self, file):
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except Exception as e:
            log_error(file, '1209')
            return {}

    def send_syslog(self, data):
        # отправка сообщения в сислог ZIEM
        for d in data:
            #print(d)
            d = json.dumps(d['alr_raw'], indent=4, default=str, ensure_ascii=False)
            try:
                #self.my_logger.debug('here')
                message = '123'
                data = b'<29>' + d.encode('utf-8')
                print('send', self.UDP_IP, self.UDP_PORT)
                self.sock.sendto(data, (self.UDP_IP, self.UDP_PORT))
            except Exception as e:
                print(e)

    async def send_http(self, send_data, url):
        # отправка инцидентов в сендер
        #i = 1
        url = 'https://' + self.sender_ip + '/' + url
        for d in send_data:
            async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
                data = {
                    'ServiceName': 'Ziem',
                    'Data': d,
                    'Playground': self.cor_name,
                }
                headers = {'content-type': 'application/json'}
                pload = json.dumps(data, indent=4, default=str, ensure_ascii=False)
                async with session.post(url, data=pload, timeout=1, headers=headers) as resp:
                    if resp.status != 200:
                        #print(json.dumps(data, indent=4, default=str, ensure_ascii=False))
                        #print(i)
                        log_error(str(resp.status), '1203')
                #await asyncio.sleep(5)
                #i += 1

    async def send_opc(self, inc):
        # отправка инцидентов в OPCUA
        #opc_ip = "172.30.1.17"
        #port = "62544"
        url = 'opc.tcp://' + self.opc_ip
        client = Client(url=url)
        async with client as c:
            var = c.get_node("ns=2;s=ZIEM.Incidents")
            val = inc['inc_mesg']
            for event in inc['events']:
                if event['alr_node']:
                    val += ', ' + event['alr_node']
                if event['alr_ip']:
                    val += ' ' + event['alr_ip']
            v = await var.write_value(val)
            await asyncio.sleep(1)

class Poster(PosterBase):
    """
    Отправка в Сендер
    """

    def run(self, debug=False):
        """
        Старт рутин
        """
        self.set_logging(debug)
        self.create_coros()
        self.loop = asyncio.get_event_loop()
        #self.loop.current_task().set_name(self.TASK_NAME)
        try:
            logging.error('1001 ~ Старт POST: post started')
            self.loop.set_exception_handler(handle_exception)
            self.create_tasks()
            self.loop.run_forever()
        except Exception as e:
            log_error(e, '1200')
            self.loop.stop()

    def __init__(self):
        super(Poster, self).__init__()
        self.POST_LOG = '/var/log/ziem/post.log'
        self.POST_LOG_SIZE = 10000000
        self.POST_LOG_COUNT = 10
        self.TASK_NAME = 'POST-POST'

    def set_logging(self, debug):
        if debug:
            with open(self.POST_LOG, 'w') as f:
                f.write('Debug mode\n')
            level = logging.DEBUG
        else:
            level = logging.INFO
        logging.basicConfig(
            handlers=[RotatingFileHandler(self.POST_LOG, 
                                          maxBytes=self.POST_LOG_SIZE, 
                                          backupCount=self.POST_LOG_COUNT)],
            level=level,
            format=' ~ %(asctime)s ~ %(levelname)s ~ %(message)s')

    def create_coros(self):
        report = Report()
        transmitter = Transmitter()
        self.coros = {
            'POST-CHECKER': {
                'function': self.check_loop,
                'args': (),
            },
            'POST-REPORT': {
                'function': report.run,
                'args': (),
            },
            'POST-TRANSMITTER': {
                'function': transmitter.run,
                'args': (),
            },
        }        

    async def check_loop(self):
        # проверка задач на их завершение
        while True:
            await asyncio.sleep(120)
            running_tasks = asyncio.all_tasks()
            for name, task in self.tasks.items():
                if task.done():
                    if task.exception():
                        log_error(task.exception(), '1208')
                    coro = self.coros[name]
                    self.tasks[name] = self.loop.create_task(
                        coro['function'](*coro['args']), name=name)
                    logging.info('POST-CHECKER ~ Restart task: ' + name)

    def create_tasks(self):
         for k,v in self.coros.items():
            self.tasks[k] = self.loop.create_task(
                v['function'](*v['args']), name=k)


class Report(PosterBase):
    """
    Генерация отчета каждые 30 минут
    """
    def __init__(self):
        super(Report, self).__init__()
        self.db = get_db()

    async def run(self):
        # отчет о работе ZIEM
        try:
            self.time = datetime.now()
            while True:
                    await asyncio.sleep(1800)
                    #await write_db(self.db['report'], [event])
                    await self.get_data()
                    await self.write_data()
                    await self.send_http([self.data], 'sendupmongo')
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
            'inc_cor': self.cor_name,
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


class Transmitter(PosterBase):
    """
    Отправка данных в сендер
    """

    def __init__(self):
        super(Transmitter, self).__init__()
        self.db = get_db()
        self.UDP_IP = "192.168.98.110"
        self.UDP_PORT = 514
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    async def run(self):
        try:
            await self.get_time()
            while True:
                await asyncio.sleep(10)
                data = {}
                time = datetime.now() - timedelta(seconds=30)
                alerts = await self.db['alerts'].find(
                    {"$and": [
                    {'alr_time': {'$gte': self.time['messages'] }},
                    {'alr_time': {'$lt': time }} ]
                    }).to_list(length=1000)
                incs = await self.db['incs'].find(
                    {"$and":[
                    {'inc_time': {'$gte': self.time['sendupmongo'] }},
                    {'inc_time': {'$lt': time }}
                    ]}).to_list(length=1000)
                if alerts:
                    data['messages'] = [alerts]
                if incs:
                    data['sendupmongo'] = incs
                for d in data:
                    await self.send_http(data[d], d)
                    #await self.send_syslog(data[d])
                    self.time[d] = time
                await self.update_time()
        except Exception as e:
            log_error(e, '1203')
            
    async def get_time(self):
        doc = await self.db['post'].find_one({'name': 'transmitter_time'})
        if doc:
            self.time = doc['time']
        else:
            time = datetime.now()
            self.time = {
                'messages': time,
                'events': time,
                'sendupmongo': time,
            }
    async def update_time(self):
        await self.db['post'].update_one(
            {'name': 'transmitter_time'}, 
            {'$set': {'time': self.time}}, upsert=True)
