"""
    ZIEM
    Бенгарт Захар
    Камнев Сергей
    Модуль Отправки данных
"""

import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
import logging.handlers

from ziem.core.db import log_error
from .sender import Sender
from .prots import Prots
from .report import Report
from .trans import Trans

def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logging.error(f"Exception: {msg}")

        
class Poster:
    
    tasks = {}
    
    def run(self, debug=False):
        """
        Старт рутин
        """
        self.set_logging(debug)
        self.create_coros()
        self.loop = asyncio.get_event_loop()
        #self.loop.current_task().set_name(self.TASK_NAME)
        try:
            logging.info('1001 ~ Старт POST: post started')
            self.loop.set_exception_handler(handle_exception)
            self.create_tasks()
            self.loop.run_forever()
        except Exception as e:
            log_error(e, '1200')
            self.loop.stop()

    def __init__(self):
        self.POST_LOG = '/var/log/ziem/post.log'
        self.POST_LOG_SIZE = 10000000
        self.POST_LOG_COUNT = 10
        self.TASK_NAME = 'POST-POST'

    def set_logging(self, debug):
        if debug:
            level = logging.DEBUG
            print('DEBUG')
        else:
            level = logging.INFO
        logging.basicConfig(
            handlers=[RotatingFileHandler(self.POST_LOG, 
                                          maxBytes=self.POST_LOG_SIZE, 
                                          backupCount=self.POST_LOG_COUNT)],
            level=level,
            format=os.environ['ZIEM_FORMAT_LOG'])

    def create_coros(self):
        sender_report = os.getenv('ZIEM_SENDER_REPORT', 'SenderReport')
        report = Report(sender_report)
        transmitter = Trans(ignore_name=[sender_report])
               
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
            self.tasks[k] = self.loop.create_task(v['function'](*v['args']), name=k)