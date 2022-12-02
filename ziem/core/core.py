"""
    ZIEM
    Бенгарт Захар

    Главный модуль ZIEM.
    Запуск всех остальных модулей.
    Очередность прохождения данных:
        Источник -> 
        Логирование -> 
        Нормализация -> 
        Корреляция -> 
        Отправка -> 
        Сторонние системы
"""
import os
import asyncio
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from .log import Loggereizer
from .nor import Normaleizer
from .cor import Correleizer
from .rep import Reporteizer
from .db import log_error

from functools import *

class Core():
    """
    Основной класс
    """

    def __init__(self):
        
        self.CONF_CHANGED = '/var/opt/ziem/conf/conf_changed'
        self.ZIEM_LOG = '/var/log/ziem/ziem.log'
        self.ZIEM_LOG_SIZE = 10000000
        self.ZIEM_LOG_COUNT = 10
        self.TASK_NAME = 'ZIEM-ZIEM'
        self.tasks = {}
        
    async def run(self, debug=False):
        """
        Запуск ZIEM и всех модулей
        """
        print('ziem Core')
        self.set_logging(debug)
        logs = asyncio.Queue()
        events = asyncio.Queue()
        incs = asyncio.Queue()
        rep_logs = asyncio.Queue()
        rep_events = asyncio.Queue()
        rep_incs = asyncio.Queue()
        log = Loggereizer(logs, rep_logs)
        nor = Normaleizer(logs, events, rep_events)
        cor = Correleizer(events, incs)
        rep = Reporteizer(rep_logs, rep_events, incs, logs)
        asyncio.current_task().set_name(self.TASK_NAME)
        loop = asyncio.get_event_loop()
        loop.create_task(log.run(), name='ZIEM-LOG')
        loop.create_task(nor.run(), name='ZIEM-NOR')
        loop.create_task(cor.run(), name='ZIEM-COR')
        loop.create_task(rep.run(), name='ZIEM-REP')
        try:
            log_error('core started', '1100')
            while True:
                #t1 = datetime.now()
                await asyncio.sleep(600)
                #t2 = (datetime.now() - t1)
                #running_tasks = asyncio.all_tasks()
                #print('[*] running tasks: ' + str(len(running_tasks)))
                #print('[+] loop tick: ' + str(t2))
        except Exception as e:
            log_error(e, '1200')
            loop.stop()

    def set_logging(self, debug):
        if debug:
            with open(self.ZIEM_LOG, 'w') as f:
                f.write('Debug mode\n')
            level = logging.DEBUG
        else:
            level = logging.ERROR
        logging.basicConfig(
            handlers=[RotatingFileHandler(self.ZIEM_LOG, 
                                          maxBytes=self.ZIEM_LOG_SIZE, 
                                          backupCount=self.ZIEM_LOG_COUNT)],
            level=level,
            format=os.environ['ZIEM_FORMAT_LOG'])
        
        class FixExceptions(logging.Filter):
            def filter(self, record):
                #record.msg = 'TestMsg'#record.msg.replace('\n', '</br>')
                return True

        logging.getLogger().addFilter(FixExceptions())


    async def check_loop(self, loop):
        # проверка задач на их завершение
        for name, task in self.tasks.items():
            if task.done():
                logging.error('CORE ~ Stop ZIEM')
                loop.stop()
