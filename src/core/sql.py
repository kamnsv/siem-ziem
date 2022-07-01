"""
    ZIEM
    Камнев Сергей

    Модуль работы с БД PostgreSQL
"""
import os
import asyncio
import logging
from datetime import datetime
from cryptography.fernet import Fernet
import psycopg2
import json 

class Psql:
    __user   = 'zuser'# os.getenv('ZIEM_USER')
    __dbname = 'ziem'
    __host   = 'localhost'
    
    __key = None
    if os.path.isfile('/etc/opt/ziem/ziem.k'):
        with open('/etc/opt/ziem/ziem.k', 'rb') as f:
            __key = f.read()
        fern_key = Fernet(__key)
    
    __pwd = None
    if os.path.isfile('/etc/opt/ziem/sql'):
        with open("/etc/opt/ziem/sql", 'r') as f:
            __pwd = f.readline()
    __pwd = '%s'
    
    __path = '/opt/ziem/src/sql/%s.sql'
    
    __column_name = {} # наполняются при работе
    
    err_col = 'Название коллекции не задано'
    err_con = 'Ошибка подключения к PostgreSQL'
    err_exe = 'Ошибка выполнения запроса'
    err_exf = 'Файл "%s" для выполнения зпроса не найден...'
    err_q = 'Фильтр для коллекции "%s" не задан'
    
    def __init__(self, col=None):
        self.__col = col
        self.__q   = None
        self.__res = None
        if col is not None:
            self.__timeseries = self.__timeseries()
            self.drop_collection = None
            self.create_collection = None
            
    def __timeseries(self):
        return self.__get_type_filed('timestamp')
        
    def __getitem__(self, item):
        return Psql(item)
    
    def __get_con(self):
        con = None
        try:
            con = psycopg2.connect(dbname=self.__dbname, user=self.__user, 
                                   password=self.__pwd, host=self.__host)
        except Exception as e:
            print(self.err_con)
            print(e)
        return con     
        
    def __execute_file(self, name, data):
        path = self.__path % name
        
        if not os.path.isfile(path): 
            print(err_exf % path)
            return False        
        with open(path, 'r') as f:
            q = f.read() % data
            self.__execute(q)
        return True
        
    def __execute(self, q):
        con = self.__get_con()
        if con is None: return
        res = None
        with con:
            with con.cursor() as cur:
                try:
                    cur.execute(q)
                    try:
                        res = cur.fetchall()
                    except: pass
                except Exception as e:
                    print(self.err_exe)
                    print(e)
        return res
        
    async def drop_collection(self, col):
        function_name = f'{col}_delete_old_rows_function'
        trigger_name = f'{col}_delete_old_rows_trigger'
        self.__execute(f'DROP TRIGGER IF EXISTS {trigger_name} ON {col};')
        self.__execute(f'DROP FUNCTION IF EXISTS {function_name}();')
        self.__execute(f'DROP TABLE IF EXISTS {col};')
            
    async def create_collection(self, col, timeseries=None, expireAfterSeconds=None):
        q = f'CREATE TABLE {col}( _id SERIAL PRIMARY KEY, data jsonb'
        
        if type(timeseries) == dict:
            
            timeField = timeseries.get('timeField')
            if timeField is not None:
                q += f', {timeField} TIMESTAMP DEFAULT current_timestamp'
            
            metaField = timeseries.get('metaField')
            if metaField is not None:
                q += f', {metaField} varchar(255) NOT NULL'
            
            q += ');'
            
        self.__execute(q)   
            
        if None in [expireAfterSeconds, timeseries]: return
        
        timeField = timeseries.get('timeField')
        if timeField is None: return
    
        function_name = f'{col}_delete_old_rows_function'
        trigger_name = f'{col}_delete_old_rows_trigger'
        
        self.__execute_file('f_expire', 
                            {
                                'function_name':  function_name, 
                                'table_name':     col,
                                'time_field':     timeField,
                                'expire_sec':     expireAfterSeconds,
                            })
        
        self.__execute_file('t_expire', 
                            {
                                'trigger_name':   trigger_name,
                                'table_name':     col,
                                'function_name':  function_name, 
                            })
        
        
        
    def __get_columns_name(self):
        assert (self.__col is not None and self.err_col)
        
        if self.__column_name.get(self.__col) is None:
            q = f"SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{self.__col}'";
            self.__column_name[self.__col] = self.__execute(q)
            
        return self.__column_name[self.__col]
        
        
    def __get_type_filed(self ,t):
        for col in self.__get_columns_name():
            if t in col[1]: return col[0]
        return None
        
    async def insert_many(self, data):
        assert (self.__col is not None and self.err_col)
        
        for one in data:
            await self.insert_one(one)
            
            
    async def insert_one(self, data):
        assert (self.__col is not None and self.err_col)
        
        col_name = self.__get_columns_name()
        q = f'INSERT INTO {self.__col} (data'
        
        time_field = self.__get_type_filed('timestamp')
        meta_field = self.__get_type_filed('character')
        
        if time_field in data: q +=f', {time_field}'
        if meta_field in data: q +=f', {meta_field}'
        
        q += ') VALUES ('
        q += "'%s'" % json.dumps(data, indent=4, sort_keys=True, default=str)
        
        if time_field in data: q +=", '%s'" % data[time_field]
        if meta_field in data: q +=", '%s'" % data[meta_field]
        
        q += ');'    
        self.__execute(q)
     
    def __filter_to_where(self, fil):
        assert (self.__col is not None and self.err_col)
        q = f'SELECT * FROM {self.__col}'
        
        if fil is not None:
            j = json.dumps(fil, indent=4, sort_keys=True, default=str)
            q += f" WHERE data @> '{j}'"  
            
        return q
    
    def find_one(self, fil=None):
        assert (self.__col is not None and self.err_col)
        
        q = self.__filter_to_where(fil) 
        
        q += ' ORDER BY '
        if self.__timeseries:
            q += f'{self.__timeseries} DESC'
        else:
            q += f'_id ASC'
        
        q += ' LIMIT 1;'
        res = self.__execute(q)
        
        if not len(res): return None
    
        data = res[0][1]
        data['_id'] = res[0][0]
        return data
    
    def find(self, fil):
        assert (self.__col is not None and self.err_col)
        self.__q = self.__filter_to_where(fil)  
        return self
    
    def __iter__(self):
        self.__q += ';'
        res = self.__execute(self.__q)
        for r in res:
            r[1]['_id'] = r[0]
            r = r[1]
        self.__res = res
        return iter(res)
    
    def __len__(self):
        if self.__res is None:
            self.__iter__()
        return len(self.__res)    
    
    def sort(self):
        assert (self.__col is not None and self.err_col)
        assert (self.__q is not None and self.err_q % self.__col)
        
    
    def count(self):
        assert (self.__col is not None and self.err_col)
        assert (self.__q is not None and self.err_q % self.__col)
        
    def update_one(self, fil, opt):
        assert (self.__col is not None and self.err_col)
        ...
    
    
    def update_many(self):
        assert (self.__col is not None and self.err_col)
        ...
    
    
    def replace_one(self):
        assert (self.__col is not None and self.err_col)
    
         
        
def get_db():
    return Psql()

def get_col(col):
    return Psql(col)
    
async def write_db(col, data):
    # запись данных в БД
    await col.insert_many(data)

async def dropdb():
    # удаление записей из БД
    db = get_db()
    await db.drop_collection('alerts')
    await db.create_collection(
        'alerts',
        timeseries = {
            'timeField': 'alr_time',
            'metaField': 'alr_node',
            'granularity': 'seconds',
        },
        expireAfterSeconds=31536000)
    await db.drop_collection('events')
    await db.create_collection(
        'events',
        timeseries = {
            'timeField': 'time',
            'metaField': 'node',
            'granularity': 'seconds',
        },
        expireAfterSeconds = 31536000)
    await db.drop_collection('incs')
    await db.create_collection(
        'incs',
        timeseries = {
            'timeField': 'inc_time',
            'metaField': 'name',
            'granularity': 'seconds',
        },
        expireAfterSeconds = 31536000)
    await db.drop_collection('report')
    await db.create_collection(
        'report',
        timeseries={
            'timeField': 'time',
            'granularity': 'minutes',
        },
        expireAfterSeconds = 31536000)
    await db.drop_collection('logweb')
    await db.create_collection(
        'logweb',
        timeseries={
            'timeField': 'time',
            'metaField': 'src',
            'granularity': 'minutes',
        },
        expireAfterSeconds = 31536000)
    await db.drop_collection('ping')
    await db.create_collection('ping',
        timeseries={
            'timeField': 'time',
            'metaField': 'name',
            'granularity': 'minutes',
        },
        expireAfterSeconds = 31536000)                           
    
    
loop = asyncio.get_event_loop()
#loop.run_until_complete(dropdb()) 

db = get_db()
col = db['ping']
loop.run_until_complete(write_db(col, [{'name': 'node1', 'active': True, 'time': datetime.now()}])) 

print(list(col.find({'name': 'node1'})))