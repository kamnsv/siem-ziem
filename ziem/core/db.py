"""
    ZIEM
    Бенгарт Захар
    Камнев Сергей

    Модуль работы с БД MongoDB
    Запись ошибок в журнал работы и чтение json файлов
"""
import inspect
import json
import socket
import traceback
import asyncio
import logging
from datetime import datetime
import motor.motor_asyncio
from cryptography.fernet import Fernet
import sys
import os

def get_db():
    #if not os.getenv('ZIEM_MONGO'):
     #   return Psql()
    # получение доступа к БД
    con_str = 'mongodb://zuser:123456@mongo:27017/?authSource=ziem&authMechanism=SCRAM-SHA-256'
    try:
        with open('/etc/opt/ziem/ziem.k', 'rb') as f:
            key = f.read()
        fern_key = Fernet(key)
        with open("/etc/opt/ziem/db", 'r') as f:
            uri = f.readline()
        con_str = fern_key.decrypt(uri.encode()).decode()  
    except: pass
    client = motor.motor_asyncio.AsyncIOMotorClient(con_str)
    return client['ziem']


async def write_db(col, data):
    # запись данных в БД
    await col.insert_many(data)

       
async def dropdb(*, data_col={}, spec_col='ALL'): # удаление записей из БД
    db = get_db()
    data_col.update(init_col_env()) # из параметров
    if (spec_col not in data_col) and ('ALL' != spec_col):
        print(f'Коллекция "{spec_col}" не найдена среди "%s".' % ', '.join(list(data_col.keys())))  
    for col, data in data_col.items():
        if spec_col in ('ALL', col):
            print('Очистка:', col, data)
            await db.drop_collection(col)
            await db.create_collection(col,
                timeseries=data['timeseries'],
                expireAfterSeconds=int(data['expireAfterSeconds']))
            
    
def log_error(e, code=''):
       
    # запись логов в журнал
    codes = {
        # info
        '1100': 'Старт ZIEM',
        '1101': 'Перезапуск задачи',
        '1102': 'Запуск задачи',    
        # error
        '1200': 'Ошибка модуля',
        '1201': 'Ошибка перезапуска задачи',
        '1202': 'Ошибка записи данных в БД',
        '1203': 'Ошибка отправки в Sender по HTTP',
        '1204': 'Ошибка отправки в OPCUA сервер',
        '1205': 'Ошибка задачи Отчета о работе ZIEM',
        '1206': 'Ошибка задачи Контроля потока сообщений',
        '1207': 'Ошибка обработки данных',
        '1208': 'Ошибка задачи',
        '1209': 'Ошибка чтения файла',
        '1210': 'Ошибка задачи Мониторинга сети',
        '1211': 'Ошибка подключения к источнику',
        '1212': 'Отсутствуют сообщения от источника',
        '1213': 'Источник недоступен по сети',
        '1214': 'Ошибка отправки по Syslog UDP',
        '1215': 'Ошибка отправки по Syslog TCP',
        '1215': 'Ошибка соединения по Syslog TCP',
        # good
        '1311': 'Успешное подключения к источнику',
        '1312': 'Поступают сообщения от источника',
        '1313': 'Источник доступен по сети',
    }    
    if logging.getLogger().level == 10:
        tb =  traceback.format_exc()
        if not 'NoneType: None' in tb:
            print(tb)
            logging.debug(tb)
    if code in codes:
        desc = codes[code]
    else:
        desc = 'Описание не найдено'
        code = '1000'
    task_name = asyncio.current_task().get_name()
    message = code + ' ~ ' + task_name + ' ~ ' + desc + ' : ' + repr(e)
    logging.error(message)
    print(message)
    
def readjson(file):
    # чтение из файла
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except Exception as e:
        log_error(e, '1209')
        return {}

def init_col_env():
    # загрузка параметров коллекций
    fname = os.path.dirname(os.path.abspath(__file__))[:-4] + 'cfg/db_core.json'
    with open(fname) as f: # из json
        data_col = f.read()
    exp_data = os.getenv('ZIEM_CORE_EXPIRATION_DATA', '31536000')
    s = {'ttl_alert': os.getenv('ZIEM_CORE_EXPIRATION_ALERT', exp_data),
         'ttl_event': os.getenv('ZIEM_CORE_EXPIRATION_EVENT', exp_data),
         'ttl_inc':   os.getenv('ZIEM_CORE_EXPIRATION_INC', exp_data),
         'ttl_ping':  os.getenv('ZIEM_CORE_EXPIRATION_PING', exp_data),
         'ttl_log':   os.getenv('ZIEM_CORE_EXPIRATION_LOG', exp_data),
         'ttl_rep':   os.getenv('ZIEM_CORE_EXPIRATION_REP', exp_data) ,
        }
    return json.loads(data_col % s)       
     