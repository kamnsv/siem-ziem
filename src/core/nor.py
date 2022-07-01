"""
    ZIEM
    Бенгарт Захар

    Модуль Нормализации
    Получение сообщений от модуля Логирования
    Необходимо отдельное правило для каждого профиля
    Нормализация происходит с помощью регекса или id сообщения
    Каждое событие должно иметь таксономию.
    Если необходимы поля (пользователь, имя_процесса),
    то значения ищутся через регекс
    События затем попадают в следующий модуль Корреляции
"""

# -*- coding: utf-8 -*-
import json
import asyncio
import logging
from re import search, sub
from datetime import datetime

from .db import readjson, log_error

class Normaleizer:
    """
    Основной класс для нормализации
    """
    def __init__(self, queue_alerts, queue_events, queue_rep):
        self.queue_alerts = queue_alerts
        self.queue_events = queue_events
        self.queue_rep = queue_rep
        self.profiles = {
            #'Netmap': self.rule_netmap,
            'Syslog' : self.rule_syslog,
            'MSWindows' : self.rule_mswindows_not,
            'WinSyslog' : self.rule_mswindows_syslog,
            'ProsoftRegul' : self.rule_prosoftregul,
            'CiscoASA' : self.rule_ciscoasa,
            'OPCUA' : self.rule_opcua,
            'KICS': self.rule_kics,
            'WinCC': self.rule_wincc,
            'ZIEM': self.rule_ziem,
        }


    async def run(self):
        # старт рутин
        try:
            self.loop = asyncio.get_running_loop()
            self.read_rules('/var/opt/ziem/conf/nor_rule.json')
            self.create_logrules()
            logging.debug('NOR ~ Profiles=' + ', '.join(self.profiles.keys()))
            logging.debug('NOR ~ Rules=' + ', '.join(self.rules.keys()))
            self.loop.create_task(self.nor_main(), name='NOR')
            while True:
                await asyncio.sleep(3600)
        except Exception as e:
            log_error(e, '1200')

    def read_rules(self, file):
        # парсинг правил
        self.rules = {}
        raw_rules = readjson(file)
        for r in raw_rules:
            rule = {}
            for f in ['events', 'name', 'tax_main', 'profile', 'logs', 'norm', 'obj']:
                if f not in r:
                    continue
            name = r['name']
            rule['profile'] = r['profile']
            rule['norm'] = r['alr_norm']
            rule['tax_main'] = r['tax_main']
            rule['logs'] = r['logs']
            self.filter = {}
            for event in r['events']:
                if ('tax_object' not in event or 
                    'tax_action' not in event):
                    continue
                tax = (event['tax_object'] + ':' 
                       + event['tax_action'])
                self.filter[event['string']] = {
                    'tax': tax,
                    'msg': event['alr_msg']
                }
                if event['regex']:
                    self.filter[event['string']]['regex'] = event['regex']
            rule['filter'] = self.filter
            self.rules[name] = rule

    def create_logrules(self):
        # создание правил
        self.log_rules = {
        }
        for name, rule in self.rules.items():
            profile = rule['profile']
            if profile in self.profiles:
                if rule['logs']:
                    for log in rule['logs']:
                        self.log_rules[log] = {
                            'profile': self.profiles[profile],
                            'filter': rule['filter'],
                            'tax_main': rule['tax_main'],
                        }

    async def nor_main(self):
        # основной процесс, прием сообщений
        while True:
            try:
                alert = await self.queue_alerts.get()
                if ('alr_time' in alert and
                    'alr_ip' in alert and
                    'alr_log' in alert):
                    log = alert['alr_node'] + '-' + alert['alr_log']
                    
                    if log in self.log_rules:
                        self.filter = self.log_rules[log]['filter']
                        self.tax_main = self.log_rules[log]['tax_main']
                        event = self.log_rules[log]['profile'](alert)
                        if event:
                            await self.queue_events.put(event)
                            await self.queue_rep.put(event)
            except Exception as e:
                log_error(e, '1207')
                
                
    def rule_mswindows_not(self, alert):
        # правило нормализации для Windows
        event = {}
        code = alert['alr_code']
        if code in self.filter:
            strings = alert['alr_raw']
            event['node'] = alert['alr_node']
            event['ip'] = alert['alr_ip']
            for field, value in self.filter[code].items():
                if field == 'regex':
                    for regex_field, regex_value in value.items():
                        try: event[regex_field] = strings[int(regex_value)]
                        except: continue
                else:
                    event[field] = value
            if 'process' in event:
                event['process'] = event['process'].split('\\')[-1]
            event['tax'] = self.tax_main + ':' + event['tax']
            event['time'] = alert['alr_time']
            event['raw'] = {
                'raw' : alert['alr_raw'],
                'code': alert['alr_code'],
                'log': alert['alr_log'],
                #'rec': alert['alr_rec'],
            }
        return event


    def rule_netmap(self, alert):
        # правило нормализации для Мониторинга сети
        event = {}
        for field, value in self.filter.items():
            if field in alert['alr_raw']:
                event['node'] = alert['alr_node']
                event['ip'] = alert['alr_ip']
                for regex_field, regex_value in value.items():
                    event[regex_field] = regex_value
                event['tax'] = self.tax_main + ':' + event['tax']
                event['time'] = alert['alr_time']
                event['raw'] = {
                    'raw' : alert['alr_raw'],
                }
        return event

    def rule_prosoftregul(self, alert):
        # правило нормализации для Prosoft Regul
        event = {}
        for search_string, event_data in self.filter.items():
            if search_string in alert['alr_raw']:
                event['node'] = alert['alr_node']
                event['ip'] = alert['alr_ip']
                for field, value in event_data.items():
                    if field == 'regex':
                        for regex_field, regex_value in value.items():
                            event[regex_field] = self.regex(regex_value, alert['alr_raw'])
                    else:
                        event[field] = value
                event['tax'] = self.tax_main + ':' + event['tax']
                event['time'] = alert['alr_time']
                #datetime.strptime(alert['raw'][0:19], '%d.%m.%Y %H:%M:%S')
                event['raw'] = {
                    'raw' : alert['alr_raw']
                }
                break
        return event

    def rule_syslog(self, alert):
        # правило нормализации для Syslog
        event = {}
        for search_string, event_data in self.filter.items():
            if search_string in alert['alr_raw']:
                event['node'] = alert['alr_node']
                event['ip'] = alert['alr_ip']
                for field, value in event_data.items():
                    if field == 'regex':
                        for regex_field, regex_value in value.items():
                            event[regex_field] = self.regex(regex_value, alert['alr_raw'])
                    else:
                        event[field] = value
                event['tax'] = self.tax_main + ':' + event['tax']
                event['time'] = alert['alr_time']
                event['raw'] = {
                    'raw' : alert['alr_raw']
                }
                break
        return event

    def rule_kics(self, alert):
        # правило нормализации для KICS
        event = {}
        code = search('type="([0-9]*)"', alert['alr_raw'])
        if code:
            code = code.group(1)
            if code in self.filter:
                event['node'] = alert['alr_node']
                event['ip'] = alert['alr_ip']
                for field, value in self.filter[code].items():
                    if field == 'regex':
                        for regex_field, regex_value in value.items():
                            event[regex_field] = self.regex(regex_value, alert['alr_raw'])
                    else:
                        event[field] = value
                event['tax'] = self.tax_main + ':' + event['tax']
                event['time'] = alert['alr_time']
                event['raw'] = {
                    'raw' : alert['alr_raw'],
                    'code': code,
                }
        return event

    def rule_ciscoasa(self, alert):
        # нормализация для CiscoASA
        event = {}
        code = search('-([0-9]*):',alert['alr_raw'][0:10]).group(1)
        if code in self.filter:
            event['node'] = alert['alr_node']
            event['ip'] = alert['alr_ip']
            for field, value in self.filter[code].items():
                if field == 'regex':
                    for regex_field, regex_value in value.items():
                        event[regex_field] = self.regex(regex_value, alert['alr_raw'])
                else:
                    event[field] = value
            event['tax'] = self.tax_main + ':' + event['tax']
            event['time'] = alert['alr_time']
            event['raw'] = {
                'raw' : alert['alr_raw'],
                'code': code,
            }
        return event

    def rule_mswindows_syslog(self, alert):
        # нормализация для Windows по протоколу Syslog
        event = {}
        code = alert['alr_code']
        if code in self.filter:
            strings = alert['alr_raw']
            event['node'] = alert['alr_node']
            event['ip'] = alert['alr_ip']
            for field, value in self.filter[code].items():
                if field == 'regex':
                    for regex_field, regex_value in value.items():
                        try: event[regex_field] = strings[int(regex_value)]
                        except: continue
                else:
                    event[field] = value
            event['tax'] = self.tax_main + ':' + event['tax']
            event['time'] = alert['alr_time']
            event['raw'] = {
                'raw' : alert['alr_raw'],
                'code': alert['alr_code'],
                'log': alert['alr_log'],
                'rec': alert['alr_rec'],
            }
        return event

    def rule_opcua(self, alert):
        # нормализация для OPCUA
        event = {}
        for search_string, event_data in self.filter.items():
            if search_string in alert['alr_raw']:
                event['node'] = alert['alr_node']
                event['ip'] = alert['alr_ip']
                for field, value in event_data.items():
                    if field == 'regex':
                        for regex_field, regex_value in value.items():
                            event[regex_field] = self.regex(regex_value, str(alert['alr_raw']))
                    else:
                        event[field] = value
                event['tax'] = self.tax_main + ':' + event['tax']
                event['time'] = alert['alr_time']
                event['raw'] = {
                    'raw' : alert['alr_raw'],
                }
                break
        return event

    def rule_wincc(self, alert):
        # нормализация для WinCC
        event = {}
        alert_split = alert['alr_raw'].split(',')
        for search_string, event_data in self.filter.items():
            if search_string in alert_split[4]:
                event['node'] = alert_split[2]
                event['ip'] = alert['alr_ip']
                for field, value in event_data.items():
                    if field == 'regex':
                        for regex_field, regex_value in value.items():
                            event[regex_field] = alert_split[int(regex_value)]
                    else:
                        event[field] = value
                event['tax'] = self.tax_main + ':' + event['tax']
                event['time'] = alert['alr_time']
                #datetime.strptime(alert['raw'][0:19], '%d.%m.%Y %H:%M:%S')
                event['raw'] = {
                    'raw' : alert['alr_raw']
                }
                break
        return event

    def rule_ziem(self, alert):
        # нормализация для ZIEM           
        event = {}
        #alert_split = alert['alr_raw'].split(' ~ ')
        raw = alert['alr_raw']
        if type(raw) != dict:
            raw = json.loads(raw)
        code = raw['code']
        if code in self.filter:
            event['time'] = alert['alr_time']
            event['node'] = alert['alr_node']
            event['ip'] = alert['alr_ip']
            for field, value in self.filter[code].items():
                if field == 'regex':
                    for regex_field, regex_value in value.items():
                        if regex_value in raw:
                            event[regex_field] = raw[regex_value]
                else:
                    event[field] = value
            event['tax'] = self.tax_main + ':' + event['tax']
            event['raw'] = {
                'raw' : alert['alr_raw'],
                'code': code,
            }
        return event

    def regex(self, regex, alert):
        # обработка события с помощью регекса
        if "%s" in regex:
            regex = sub(r"%s", "([^\r\n\t\f\v \"\(\)',\]]+)", regex)
        elif "%a" in regex:
            regex = sub(r"\(", "\\\(", regex)
            regex = sub(r"\)", "\\\(", regex)
            regex = sub(r"%a", "(.+)", regex)
        m = search(regex, alert)
        if m:
            return m.group(1)
