"""
    ZIEM
    Бенгарт Захар

    Модуль Корреляции.
    Получение событий от модуля Нормализации.
    Правила корреляции содержат события с определенной таксономией
    Если событие имеет данную таксономию, то оно попадает в это правило
    Имеются следующие виды правил:
        простое - 1 событие генерит 1 инцидент
        сложное - необходима обработка нескольких событий
    Если событие формирует инцидент, то он попадает в модуль Отправки
"""

import asyncio
import logging
import os
from os import makedirs
from datetime import datetime

from .db import log_error, readjson

class Correleizer:
    """
    Основной класс для корреляции
    """
    def __init__(self, queue_events, queue_incs):
        self.queue_events = queue_events
        self.queue_incs = queue_incs

    async def run(self):
        # Старт рутин
        try:
            self.loop = asyncio.get_running_loop()
            self.read_deeprules()
            await self.init_fastax()
            await self.init_deeptax()
            self.create_coros()
            self.create_tasks()
            logging.debug('COR ~ Deeprules= ' + ', '.join(self.raw_rules.keys()))
            while True:
                await asyncio.sleep(60)
                await self.check_loop()
        except Exception as e:
            log_error(e, '1200')
    
    def get_books(self):
        books = {}
        path = '/var/opt/ziem/conf'
        for fname in os.listdir(path):
            full = os.path.join(path, fname)
            if os.path.isdir(full): continue
            if not fname.endswith('.json'): continue
            if not fname.startswith('bks_'): continue
            name = fname[4:-5]
            json_data = readjson(full)
            data = [ j['name'] for j in json_data if j.get('name') ]
            books[name] = data    
        return books
        
    def read_deeprules(self):
        # чтение сложных правил с конфигов
        data = readjson('/var/opt/ziem/conf/cor_deeprule.json')
        books = self.get_books()
        self.raw_rules = {}
        for rule in data:
            deeprule = {}
            if ('events' not in rule or 
                'name' not in rule or 
                'crit' not in rule or 
                'desc' not in rule):
                continue
            #make info
            deeprule['filter'] = []
            taxes = []
            name = rule['name']
            deeprule['name'] = name
            deeprule['info'] = {
                'name': name,
                'mesg': rule['desc'],
                'crit': rule['crit'],
                'clas': '',
            }
            if 'clas' in rule:
                deeprule['info']['clas'] = rule['clas']
            for event in rule['events']:
                if ('tax_main' not in event or 
                    'tax_object' not in event or 
                    'tax_action' not in event):
                    continue
                tax = (event['tax_main'] + ':' 
                       + event['tax_object'] + ':' 
                       + event['tax_action'])
                taxes.append(tax)
                incfilter = {}
                if 'incfilter' in event:
                    for data in event['incfilter']:
                        values = [x for x in data.get('value','').split(',')]
                        values += books.get(data.get('book',''), [])
                        incfilter[data['field']] = [x.strip().lower() for x in set(values) if x]
                excfilter = {}
                if 'excfilter' in event:
                    for data in event['excfilter']:
                        values = [x for x in data.get('value','').split(',')]
                        values += books.get(data.get('book',''), [])
                        excfilter[data['field']] = [x.strip().lower() for x in set(values) if x]
                filtr = {
                    'tax': tax,
                }
                if incfilter:
                    filtr['inc'] = incfilter
                if excfilter:
                    filtr['exc'] = excfilter   
                if 'count' in event:
                    if isinstance(event['count'], int):
                        if event['count'] > 0:
                            filtr['count'] = event['count']
                if 'diff' in event:
                    if event['diff']:
                        filtr['diff'] = event['diff']
                deeprule['filter'].append(filtr)
                
            # создание опций
            uniq = []
            timer = False
            if 'uniq1' in rule:
                uniq.append(rule['uniq1'])
            if 'uniq2' in rule:
                uniq.append(rule['uniq2'])
            if 'timer' in rule:
                if isinstance(rule['timer'], int):
                    if rule['timer'] > 0:
                        timer = rule['timer']
            deeprule['tax'] = taxes
            deeprule['uniq'] = uniq
            deeprule['timer'] = timer
            self.raw_rules[name] = deeprule    
            
    def create_coros(self):
        # создание корутин с функциями и очередями
        self.deeprules = {}
        self.coros = {}
        for name, rule in self.raw_rules.items():
            queue_in = asyncio.Queue()
            deeprule = Deeprule(queue_in, rule, self.queue_incs)
            fastrule = Fastrule(self.queue_events, self.deeptax, 
                                self.deeprules, self.fastax, self.queue_incs)
            self.coros['COR-' + name] = {
                'function': deeprule.run,
                'args': (),
            }
            self.deeprules['COR-' + name] = {
                'rule': rule,
                'queue_in': queue_in,
            }
            
        if len(self.raw_rules):    
            self.coros['COR-fastrule'] = {
                    'function': fastrule.run,
                    'args': (),
            }

    def create_tasks(self):
        # создание задач из корутин
        self.tasks = {}
        for k,v in self.coros.items():
            self.tasks[k] = self.loop.create_task(v['function'](*v['args']), name=k)

    async def check_loop(self):
        # проверка задач на их завершение
        for name, task in self.tasks.items():
            if task.done():
                # если задача упала, рестартуем ее
                coro = self.coros[name]
                queue_in = asyncio.Queue()
                self.tasks[name] = self.loop.create_task(
                    coro['function'](*coro['args']), name=name)
                if name != 'COR-fastrule':
                    self.deeprules[name]['queue_in'] = queue_in
                logging.info('COR ~ Restart task: ' + name)


    async def init_fastax(self):
        # инициализация простых правил
        self.fastax = {}
        rules = readjson('/var/opt/ziem/conf/cor_fastrule.json')
        for r in rules:
            rule = {}
            info = {
                'name': r['name'],
                'mesg': r['desc'],
                'crit': r['crit'],
            }
            if 'clas' in r:
                info['clas'] = r['clas']
            tax = r['tax_main'] + ':' + r['tax_object'] + ':' + r['tax_action']
            self.fastax[tax] = info

    async def init_deeptax(self):
        # инициализация сложных правил
        makedirs('/var/opt/ziem/cor/diff', exist_ok=True)
        self.deeptax = {}
        for rule in self.raw_rules.values():
            taxes = rule['tax']
            for tax in taxes:
                if tax in self.deeptax:
                    if ('COR-' + rule['name']) not in self.deeptax[tax]:
                        self.deeptax[tax].append('COR-' + rule['name'])
                else:
                    self.deeptax[tax] = ['COR-' + rule['name'],]


class Rule:
    """
    Базовый класс для сложных и простых правил
    """
    
    def __init__(self):
        settings = readjson('/var/opt/ziem/conf/settings.json')
        if 'cor_name' in settings:
            self.cor_name = settings['cor_name']
        else:
            self.cor_name = ""

    def add_inc(self, metevent, time, name, mesg, crit, clas):
        # добавление инцидента
        
        inc = {
            'inc_time': time,
            'inc_name': name,
            'inc_mesg': mesg,
            'inc_crit': crit,
            'inc_clas': clas,
            'inc_cor': self.cor_name,
        }
        
        inc['events'] = []
        
        sub = set()
        
        for e in metevent.values():
            
            if not e['event'].get('system') or e['event'].get('system') == '':
                e['event']['system'] = 'none'
            sub.add(e['event']['system'])
            
            inc['events'].append(e['event'])

        inc['inc_sub'] = ','.join(sorted(sub))

        return inc

        
        
class Fastrule(Rule):
    """
    Простое правило
    Простое правило, прием событий, отправка в сложные правила
    """
    def __init__(self, queue_events, deeptax, deeprules, fastax, queue_incs):
        super(Fastrule, self).__init__()
        self.queue_incs = queue_incs
        self.queue_events = queue_events
        self.deeptax = deeptax
        self.deeprules = deeprules
        self.fastax = fastax

    async def run(self):
        try:
            while True:
                e = await self.queue_events.get()
                time = datetime.now()
                try:
                    if e['tax'] in self.deeptax:
                        # если событие есть в сложных правилах
                        for rule in self.deeptax[e['tax']]:
                            await self.deeprules[rule]['queue_in'].put(e)
                    if e['tax'] in self.fastax:
                        # если событие в простом правиле
                        info = self.fastax[e['tax']]
                        metevent = {e['tax']: {'event' : e}}
                        inc = self.add_inc(metevent, time, **info)
                        await self.queue_incs.put(inc)
                except Exception as e:
                    log_error(e, '1207')
        except Exception as e:
            log_error(e, '1208')


class Deeprule(Rule):
    """
    Сложное правило
    Определение инцидентов по сложным правилам
    """
    def __init__(self, queue_in, rule, queue_incs):
        super(Deeprule, self).__init__()
        self.queue_in = queue_in
        #self.rule = rule
        self.tax = rule['tax']
        self.uniq = rule['uniq']
        self.timer = rule['timer']
        self.filtr = rule['filter']
        self.name = rule['name']
        self.info = rule['info']
        self.queue_incs = queue_incs
        
    async def run(self):
        self.metevents = {}
        try:
            while True:
                try:
                    event = await self.queue_in.get()
                    time = datetime.now()
                    for f in self.filtr:
                        if self.check_filter(event, f):
                            # если событие проходит через фильтры
                            self.make_uniq(event)
                            self.add_metevent(event, f, self.filtr.index(f))
                            if self.check_metevent():
                                # если метасобытие полностью заполнилось взводим инцидент
                                inc = self.add_inc(self.metevents[self.metuniq], 
                                              time, **self.info)
                                self.clear_metevent()
                                await self.queue_incs.put(inc)
                            break
                except Exception as e:
                    log_error(e, '1207')
        except Exception as e:
            log_error(e, '1208')

    def check_filter(self, event, filtr):
        # проверка события по фильтрам
        if event['tax'] not in filtr['tax']:
            return False
        if 'exc' in filtr:
            # проверка исключающего фильтра
            for field, value in filtr['exc'].items():
                if field in event:
                    if field == 'time':
                        check_field = str(event[field].hour)
                    else:
                        if event[field]:
                            check_field = event[field].lower()
                    if check_field in value:
                        return False
        if 'inc' in filtr:
            # проверка включающего фильтра
            for field, value in filtr['inc'].items():
                if field not in event:
                    return False
                if field == 'time':
                    check_field = str(event[field].hour)
                else:
                    check_field = event[field].lower()
                if check_field not in value:
                    return False
        if 'diff' in filtr:
            # проверка контроля значения
            if filtr['diff'] not in event:
                return False
        return 1

    def make_uniq(self, event):
        # создание уникальности события
        self.metuniq = ''
        for u in self.uniq:
            if u in event:
                self.metuniq += event[u]

    def add_metevent(self, event, filtr, index):
        # добавление события в метасобытие
        if self.metuniq not in self.metevents:
            self.metevents[self.metuniq] = {}
            self.metevents[self.metuniq][index] = {
                'event': event,
            }
        elif index not in self.metevents[self.metuniq]:
            self.metevents[self.metuniq][index] = {
                'event': event,
            }
        metevent = self.metevents[self.metuniq][index]
        if 'count' in filtr or 'diff' in filtr:
            # если есть агрегация и контроль значения
            if 'check_bit' not in metevent:
                metevent['check_bit'] = {}
            t1 = event['time']
            t2 = metevent['event']['time']
            if 'count' in filtr:
                if 'count' not in metevent['check_bit']:
                    metevent['check_bit']['count'] = False
                    metevent['meta_count'] = 0
                if (t1 - t2).seconds > self.timer:
                    metevent['meta_count'] = 1
                count = metevent['meta_count']
                if (t1 - t2).seconds <= self.timer:
                    count += 1
                if (count == filtr['count']):
                    metevent['check_bit']['count'] = True
                metevent['meta_count'] = count
            if 'diff' in filtr:
                path = '/var/opt/ziem/cor/diff/' + self.name + '-' + self.metuniq
                diff = event[filtr['diff']]
                if 'diff' not in metevent['check_bit']:
                    try:
                        with open(path, 'r') as f:
                            metevent['meta_diff'] = f.read(diff)
                        metevent['check_bit']['diff'] = False
                    except:
                        metevent['check_bit']['diff'] = False
                        metevent['meta_diff'] = diff
                        with open(path, 'w') as f:
                            f.write(diff)
                if (t1 - t2).seconds <= self.timer or self.timer == 0:
                    if (diff != metevent['meta_diff']):
                        metevent['check_bit']['diff'] = True
                        metevent['meta_diff'] = diff
                        with open(path, 'w') as f:
                            f.write(diff)
        metevent['event'] = event
        
    def check_metevent(self):
        # проверка метасобытия
        metevent = self.metevents[self.metuniq]
        if len(self.tax) == len(metevent):
            if self.timer:
                times = [ x['event']['time'] for x in metevent.values() ]
                if (max(times) - min(times)).seconds > self.timer:
                    return False
            for event in metevent.values():
                if 'check_bit' in event:
                    for bit in event['check_bit'].values():
                        if not bit:
                            return False
            return True

    def clear_metevent(self):
        # очистка метасобытия
        self.metevents[self.metuniq] = (
            {t:e for t, e in self.metevents[self.metuniq].items() 
            if 'check_bit' in e})
        for check, event in self.metevents[self.metuniq].items():
            for bit in event['check_bit']:
                self.metevents[self.metuniq][check]['check_bit'][bit] = False