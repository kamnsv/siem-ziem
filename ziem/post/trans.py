"""
    ZIEM
    Камнев Сергей
    Менеджер отправки данных

"""
import os
import json
import asyncio
import logging
from datetime import datetime

from ziem.core.db import readjson, log_error, get_db, write_db
from .sender import Sender
from .prots import Prots

class Trans(Prots):
    """
    Отправка данных в сендер
    """
    
    collections = ('alerts', 'events', 'incs')
    time_key = {
            'alerts': 'alr_time',
            'incs':   'inc_time',
            'events': 'time'
        }
    batch_size = int(os.getenv('ZIEM_POST_BATCH', '1000'))
    
    def __init__(self, ignore_name=[]):
        self.db = get_db()
        self.speriod = int(os.getenv('ZIEM_SEND_PERIOD', '4'))
        
        raw = readjson('/var/opt/ziem/conf/settings.json')
        
        self.senders = []
        for opt in raw.get('senders'):
            if opt['name'] in ignore_name: continue     
            try:
                self.senders.append(Sender(opt))
            except Exception as e: 
                logging.error('Ошибка инициализации сендера: ' + json.dumps(opt) + repr(e))
        
        
    async def run(self):
        try:
            await self.get_time()
            while True:
                
                await asyncio.sleep(self.speriod)          
                b = datetime.now()
                
                for sender in self.senders: # по отправителям
                    
                    if not sender.enabled: 
                        continue
                    
                    for col in self.collections:
                                               
                        if  getattr(sender, col)['on']:
                                                       
                            t = getattr(sender, col)['time']
                            if t not in self.time: self.time[t] = b
                            a = self.time.get(t)
                            
                            data = await self.get_data(col, a, b)

                            code = -3
                            if len(data):
                                code = await self(col, data, sender) # передача
                            
                            # интерпритация результата    
                            if -3 == code:
                                print(f'{sender} {col} {a} - {b}: Пусто')
                                
                            elif -1 == code: 
                                self.time[t] = data[-1][self.time_key[col]]
                                logging.debug(f'{sender} {col} {a} - {b}: Передано {len(data)}')
                                
                            elif -2 == code:
                                logging.debug(f'{sender} {col} {a} - {b}: Ошибка соединения')
                                pass
                            
                            else:
                                logging.debug(f'{sender} {col} {a} - {b}: Прервана {code+1}/{len(data)}')
                                self.time[t] = data[code][self.time_key[col]]

                await self.update_time()
                
        except Exception as e:
            log_error(e, '1203')
            
    async def get_time(self):
        doc = await self.db['post'].find_one({'name': 'transmitter_time'})
        if doc: 
            del doc['_id']
            self.time = doc
       
    async def update_time(self):
        self.time['name'] = 'transmitter_time'
        await self.db['post'].drop();    
        await self.db['post'].insert_one(self.time);
    
        
    async def get_data(self, col, a, b):    
        
        return await self.db[col].find(
                    {"$and": [
                    {self.time_key[col]: {'$gte': a }},
                    {self.time_key[col]: {'$lt':  b }} ]
                    }).sort(self.time_key[col], 1
                           ).to_list(length=self.batch_size)

        
        
        