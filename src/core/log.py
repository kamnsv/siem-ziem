"""
    ZIEM
    Бенгарт Захар

    Модуль Логгирования
    Получение сообщений от источников
    Необходимо правило для каждого типа источников - протокола
    Протоколы работают как отдельные модули в папке log_modules
    Сообщения затем попадают в модуль Нормализации
"""

import asyncio
import logging
from cryptography.fernet import Fernet

from .log_modules import WMISubscription
from .log_modules import ftp
from .log_modules import syslog
from .log_modules import netmap
from .log_modules import opcua
from .log_modules import http
from .db import readjson, log_error, get_db

class Loggereizer:
    """
    The main class for Loggereizer
    """
    def __init__(self, queue_alerts, queue_rep):
       
        self.queue_alerts = queue_alerts
        self.queue_rep = queue_rep
        wmi = WMISubscription()
        self.protocols = {
            'syslog': syslog,
            'ftp': ftp,
            'wmi': wmi.run,
            'netmap': netmap,
            'opcua': opcua,
            #'http': http,
        }

    async def run(self):
        """
        Start all Coroutines
        """
        try:
            self.loop = asyncio.get_running_loop()
            self.read_rules('/var/opt/ziem/conf/log_rule.json')
            self.create_coros()
            await self.create_tasks()
            logging.debug('LOG ~ Protocols=' + ', '.join(self.protocols.keys()))
            logging.debug('LOG ~ Rules=' + ', '.join(self.rules.keys()))
            logging.debug('LOG ~ Coros=' + ', '.join(self.coros.keys()))
            while True:
                await asyncio.sleep(120)
                await self.check_loop()
        except Exception as e:
            log_error(e, '1200')

    def read_rules(self, file):
        # чтение конфигов агентов
        rules_raw = readjson(file)
        
        with open('/etc/opt/ziem/ziem.k', 'r') as f:
            key = f.read()

        fern_key = Fernet(key)
        self.rules  = {}
        
        # парсинг конфига агентов
        
        for s in rules_raw:
            
            if ('protocol' in s and
                'name' in s and
                'ip' in s):
                
                self.rules[s['name']] = s
                if 'pswd' in s:
                    self.rules[s['name']]['pswd'] = fern_key.decrypt(s['pswd'].encode()).decode()
        
    
    def create_coros(self):
        # создание корутин с функциями и очередями
        self.coros = {}
        rule_syslog = []
        rule_http = []
        for name, rule in self.rules.items():
            protocol = rule['protocol']
            if protocol in self.protocols:
                if protocol == 'syslog':
                    rule_syslog.append(rule)
                elif protocol == 'http':
                    rule_http.append(rule)
                elif protocol == 'netmap':
                    continue
                elif protocol == 'wmi':
                    wmi = WMISubscription()
                    self.coros['LOG-' + name] = {
                        'function': wmi.run,
                        'args': (rule, self.queue_alerts, self.queue_rep),
                    }
                else:
                    self.coros['LOG-' + name] = {
                        'function': self.protocols[protocol],
                        'args': (rule, self.queue_alerts, self.queue_rep),
                    }
        rule_netmap = { v['ip']: k for k,v in self.rules.items() }
        self.coros['LOG-netmap'] = {
            'args': (rule_netmap, self.queue_alerts, self.queue_rep),
            'function': self.protocols['netmap'],
        }
        self.coros['LOG-syslog'] = {
            'args': (rule_syslog, self.queue_alerts, self.queue_rep),
            'function': self.protocols['syslog'],
        }
        #self.coros['LOG-http'] = {
        #    'args': (rule_http, self.queue_alerts, self.queue_rep),
        #    'function': http,
        #}

    async def create_tasks(self):
        # создание задач из корутин
        self.tasks = {}
        for k,v in self.coros.items():
            self.tasks[k] = self.loop.create_task(v['function'](*v['args']), name=k)
            #log_error(k, '1102')
            await asyncio.sleep(1)

    async def check_loop(self):
        # проверка задач на их завершение
        self.loop = asyncio.get_running_loop()
        for name, task in self.tasks.items():
            if task.done():
                coro = self.coros[name]
                self.tasks[name] = self.loop.create_task(
                    coro['function'](*coro['args']), name=name)
                #log_error(name, '1101')

