"""
    Books(Directory) reader agent for ZIEM

      Description:
          Every XXX seconds it connects to the sources and receives information about the update.

    Author:
        Kamnev Sergey
"""

import os
import json
import yaml
import asyncio
import aiohttp
import logging
from aiohttp import TCPConnector
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from .db import Database
from ziem.web.bksview import str_to_date

class Booksreader():

    
    def __init__(self, period, cfg):
        self.cfg = cfg
        self.period = period
        self.period_try = int(os.getenv('ZIEM_BOOKS_TRY_UPDATE_SEC', '60'))
        self.ziemcc = {'ZIEM_CC_IP': self.cfg['ziemcc_ip'], 
                       'ZIEM_CC_PORT': self.cfg['ziemcc_port']}
        self.init_log()
        self.api_fail = {}
        self.log.info("Start books reader service")
        
    def init_log(self):
        """
        Configure Booksreader logging
        """
        flog = '/var/log/ziem/bks.log'
        self.log = logging.getLogger('bks')
        h = RotatingFileHandler(flog, maxBytes=10000000, backupCount=10)
        f = logging.Formatter(os.environ['ZIEM_FORMAT_LOG'])
        h.setFormatter(f)
        self.log.addHandler(h)
        self.log.setLevel(logging.INFO)   
        
        
    async def run(self):
        """
        Main function for run Booksreader
        """
        while True:
            await self.update_books()
            await asyncio.sleep(self.period_try)
        
            
    async def update_books(self):
        
        api = await self.get_api_bks()
        if api:
            self.log.info("Update books: " + ', '.join(api))
        else:
            self.log.info("No books for update")
            
        for book, url in api.items():
            try:
                data = await asyncio.wait_for(self.query_server(url), timeout=30)
                data = await self.parse_data(book, data)
                if data is None: 
                    await self.set_book(book)
                    continue
                if 0 == len(data): 
                    self.log.info(f'Not data book "{book}" from api {url}')
                    continue
                self.log.info(f'Loaded data book "{book}" from api {url}')
                await self.set_book(book, data)
            except Exception as e:
                self.log.error(f'Error update book "{book}" from url {url}: ' + repr(e))
                await self.set_book(book)

    
    async def get_api_bks(self):
        api_bks = {} # book: url
        try:
            webdb = Database()
            async with await webdb.client.start_session() as s:
                col = webdb.db['opt_bks']
                async for doc in col.find({'api': {'$exists': True}}):
                    if not doc['api'] or not doc['active']: continue 
                    scheduled = str_to_date(doc.get('scheduled'))
                    if not scheduled or scheduled < datetime.now():
                        url = doc['api']
                        try:
                            url = url % self.ziemcc
                        except: pass    
                        api_bks.update({doc['name']: {'url': url, 'token': doc.get('token')}})
                        
        except Exception as e:
            self.log.error("Error connect mongoDB: " + repr(e))
            
        return api_bks
    
    async def query_server(self, api):
        
        url = api.get('url')    
        token = api.get('token')
        headers = {}
        if token:
            headers.update({'Authorization': f'Token token={token}'}) 
        try:
            async with aiohttp.ClientSession(connector=TCPConnector(ssl=False), headers=headers) as session:
                    async with session.get(url, timeout=20) as resp:
                        if 200 == resp.status:
                            try:
                                return await resp.json(content_type=resp.headers.get('Content-Type','text/html'))
                            except Exception as e:
                                self.log.error(f"Error serialize data url '{url}': " + repr(e))
                        self.log.info(f"Server {url} query code {resp.status}")      
        except Exception as e:
            self.log.error(f"Error send query to server '{url}': " + repr(e))          
                    
    async def set_book(self, book, data=None):
        
        if data:
            self.log.info(f'Write DB "{book}" number of records ' + str(len(data)))
        
            try:
                webdb = Database()
                async with await webdb.client.start_session() as s:
                    await webdb.write(f'bks_{book}', data)
                    
                await self.set_scheduled(book, self.period) 
                
            except Exception as e:
                self.log.error(f"Cant update data book {book}: " + repr(e))
                await self.set_scheduled(book, 60)   
        else:
            await self.set_scheduled(book, 60)
            
        
        
    async def set_scheduled(self, book, sec):
        scheduled = datetime.now() + timedelta(seconds=sec)
        self.log.info(f'Set scheduled update "{book}" to {scheduled}')
        webdb = Database()
        try:
            async with await webdb.client.start_session() as s:
                col = webdb.db['opt_bks']
                col.update_one( {'name': book},
                              {
                                  '$set': {
                                    'scheduled': scheduled,
                                    'updated': datetime.now(),
                                  }
                              }
                        )
                
        except Exception as e:
            self.log.error(f"Cant update scheduled book {book}: " + repr(e)) 
            
            
    async def parse_data(self, book, raw):
        
        if raw is None: return None
       
        webdb = Database()
        async with await webdb.client.start_session() as s:
            col = webdb.db['opt_bks']
            bks = await col.find_one({'name': book})
            key_list = bks.get('data_list_key')
            key_value = bks.get('data_value_key', 'name')
            
        end = key_value.split('.')[-1]
        
        data = []
        
        data_list = raw
        
        if key_list:
            try:
                for k in key_list.split('.'):
                    data_list = data_list.get(k)
            except Exception as e:
                self.log.error(f"Iterable data list '{key_list}' not exist: " + repr(e))     
                return None
            
        error_end, error_read = 0, 0       
        count_cases = len(data_list)
        now = datetime.now().strftime("%Y-%m-%d")
        for row in data_list:
            item = {'name':'', 'desc':[]}
            
            try:
                for k in key_value.split('.')[:-1]:
                    row = row.get(k)
            except Exception as e:  
                error_read += 1
                continue
            
            if type(row) != dict or end not in row:
                error_end += 1
                continue
                
            item['name'] = row[end].lstrip().lower()
            del row[end]
            item['desc'] = ''
            try:
                item['desc'] = yaml.dump(row, allow_unicode=True)
            except: pass
            item['pubdate'] = now 
            data.append(item)
        
        if error_read:
            self.log.error(f"Data for key {key_value} is not available in {error_read} items out of {count_cases}")  
        if error_end:
            self.log.error(f"End element has no data for key '{end}' in {error_end} cases of {count_cases}")  
        
        return data
    
