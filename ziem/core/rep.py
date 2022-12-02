"""
    ZIEM
    Бенгарт Захар

    Модуль Работы с БД
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from .db import log_error, get_db, write_db, readjson

class Reporteizer:
    """
    Запись в БД и Контроль потока
    """
    def __init__(self, rep_logs, rep_events, incs, logs):
        self.queue_alerts = logs
        self.queue_logs = rep_logs
        self.queue_events = rep_events
        self.queue_incs = incs
        self.db = get_db()
        self.coros = {
            'REP-writelogs' : self.writelogs(),
            'REP-writevents' : self.writevents(),
            'REP-writeincs' : self.writeincs(),
            'REP-flowmonitor' : self.flow_monitor(),
        }
        self.wait = 4
        self.ping = {}  # состояния объектов
        # name: id object
            # active: False or True
            # datetime: YYYY-MM-DD hh:mm:ss
        

    async def run(self):
        try:
            self.loop = asyncio.get_running_loop()
            self.create_tasks()
            while True:
                await asyncio.sleep(self.wait)
                await self.check_loop()
        except Exception as e:
            log_error(e, '1200')

    def create_tasks(self):
        # создание задач из корутин
        self.tasks = {}
        for coro in self.coros:
            self.tasks[coro] = self.loop.create_task(self.coros[coro], name=coro)

    async def check_loop(self):
        for name, task in self.tasks.items():
            if task.done():
                print(task)
                coro = self.coros[name]
                self.tasks[name] = self.loop.create_task(
                    coro['function'](*coro['args']), name=name)
                logging.info('REP ~ Restart task: ' + name)

    async def writelogs(self):
        # запись сообщений в БД
        col = self.db['alerts']
        ping = self.db['ping']
    
        while True:
            try:
                await asyncio.sleep(self.wait)
                data = []
                data_ping = []
                while not self.queue_logs.empty():
                    alert = await self.queue_logs.get()
                    #print(alert)
                    t = await self.toggle_ping(alert)
                    #print(['В базу', 'Пропуск'][t], alert)
                    if t: continue # Пропуск дублирующих сообщений об успешном состоянии]
                    if alert.get('ping', None) is not None: 
                        data_ping.append(alert.pop('ping'))
                        #print('*', data_ping)  
                    data.append(alert)
                if data: await write_db(col, data)
                if data_ping: await write_db(ping, data_ping)
            except Exception as e:
                log_error(e, '1202')
    
    async def toggle_ping(self, alert):  # Сообщение об успешном соединении
 
        # Если последнее собщение было о не успешном подключение, а это об успешном, то мы его положем в базу
        if 'ZIEM_ZIEM' != alert['alr_log']: return False # сообщение не от зиема
        if alert.get('ping') is None: return False # не имеет флага активности
        
        # Проверка последнего сообщения
        ping = alert.get('ping')
        name = ping['name']
        last = self.ping.get(name, None)
        active = None if last is None else last['active']
        if active == ping['active']: # состояние не поменялось
            if False == active: return False # плохое состояние передавать в БД
            return True # не отправлять дубликаты хорошего состояния
        
        # name: id object
            # active: False or True
            # datetime: YYYY-MM-DD hh:mm:ss
        
        self.ping[name] = {'active': ping['active'],
                           'datetime': alert['alr_time']} # установим новое состояние
        return False
 
    async def writevents(self):
        # запись событий в БД
        col = self.db['events']
        while True:
            try:
                await asyncio.sleep(self.wait)
                data = []
                while not self.queue_events.empty():
                    data.append(await self.queue_events.get())
                if data:
                    await write_db(col, data)
            except Exception as e:
                log_error(e, '1202')

    async def writeincs(self):
        # запись инцидентов в БД
        col = self.db['incs']
        while True:
            try:
                await asyncio.sleep(self.wait)
                data = []
                while not self.queue_incs.empty():
                    data.append(await self.queue_incs.get())
                if data:
                    await write_db(col, data)
            except Exception as e:
                log_error(e, '1202')

    async def flow_monitor(self):
        # отчет о потоке сообщений от источников
        
        rules_raw = readjson('/var/opt/ziem/conf/log_rule.json')
        log_names = {}
        for rule in rules_raw:
            if 'name' in rule and 'net_flow' in rule:
                log_names[rule['name']] = {
                    'ip': rule['ip'],
                    'flow_max': int(rule['net_flow']),
                    'flow_current': 0,
                    'alert_count': 0,
                }
                
        
        while True:
            time = datetime.now()
            await asyncio.sleep(3600)
            alerts = []
            for log_name in log_names:
                query = {"$and":[ {'alr_time': {'$gte': time}}, {'alr_node': log_name} ]}
                doc = await self.db['alerts'].find_one(query)
                if doc:
                    log_names[log_name]['alert_count'] = 1
                    
                log_names[log_name]['flow_current'] += 1
                
                if log_names[log_name]['flow_current'] == log_names[log_name]['flow_max']:
                    
                    if 0 == log_names[log_name]['alert_count']:
                        log_error(log_name, '1212')
                        raw = {
                            'code': '1212',
                            'node': log_name,
                            'desc': 'Отсутствуют сообщения от источника, node:',
                        }
                        alert = {
                            'alr_ip': '127.0.0.1',
                            'alr_node': 'ZIEM_ZIEM',
                            'alr_time': datetime.now(),
                            'alr_log' : 'ZIEM_ZIEM',
                            'alr_raw' : json.dumps(raw, default=str, ensure_ascii=False),
                            }
                        alerts.append(alert)
                        
                    log_names[log_name]['alert_count'] = 0
                    log_names[log_name]['flow_current'] = 0
                    
            for alert in alerts:
                await self.queue_alerts.put(alert)