"""
    ZIEM
    Бенгарт Захар

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

def get_db():
    # получение доступа к БД
    with open('/etc/opt/ziem/ziem.k', 'rb') as f:
        key = f.read()
    fern_key = Fernet(key)
    with open("/etc/opt/ziem/db", 'r') as f:
        uri = f.readline()
    client = motor.motor_asyncio.AsyncIOMotorClient(
        fern_key.decrypt(uri.encode()).decode())
    return client['ziem']


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
    
def log_error(e, code=''):
    
    f = inspect.currentframe()
    current = inspect.getframeinfo(f)
    caller  = inspect.getframeinfo(f.f_back)
    nline = f.f_back.f_lineno
    module  = caller.filename.split('/')[-1][:-3]
    fun     = caller.function
    insp = f'[{nline}] {module}.{fun}: '
    
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
        '1203': 'Ошибка отправки в Sender',
        '1204': 'Ошибка отправки в OPC сервер',
        '1205': 'Ошибка задачи Отчета о работе ZIEM',
        '1206': 'Ошибка задачи Контроля потока сообщений',
        '1207': 'Ошибка обработки данных',
        '1208': 'Ошибка задачи',
        '1209': 'Ошибка чтения файла',
        '1210': 'Ошибка задачи Мониторинга сети',
        '1211': 'Ошибка подключения к источнику',
        '1212': 'Отсутствуют сообщения от источника',
        '1213': 'Источник недоступен по сети',
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
        desc = insp + codes[code]
    else:
        desc =  insp + 'Описание не найдено'
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
