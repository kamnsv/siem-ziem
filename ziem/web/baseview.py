"""
    ZIEM 
    
    Description:

    Author:
        Bengart Zakhar
"""

import json
import socket
from datetime import datetime
from flask import current_app, g
from flask.cli import with_appcontext
from cryptography.fernet import Fernet
import pymongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from flask import session
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

def get_db():

    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client['ziem'] 
        
    return g.db

def get_col(collection):

    db = get_db()
    return g.db[collection]

def get_rawdb():
    with open('/etc/opt/ziem/ziem.k', 'rb') as f:
        key = f.read()
    fern_key = Fernet(key)
    with open("/etc/opt/ziem/db", 'r') as f:
        uri = f.readline()
    client = MongoClient(fern_key.decrypt(uri.encode()).decode())
    return client['ziem']

def clearweb():
    db = get_rawdb()
    db['log_rule'].drop()
    db['log_cred'].drop()
    db['nor_rule'].drop()
    db['cor_fastrule'].drop()
    db['cor_deeprule'].drop()
    db['blocl_user'].drop()
    print('DB~ Clear Database')

def dropweb():
    clearweb()
    db = get_rawdb()
    db['main'].drop()
    db['opt_taxmain'].drop()
    db['opt_taxobject'].drop()
    db['opt_taxaction'].drop()
    db['opt_protocol'].drop()
    db['opt_profile'].drop()
    db['opt_field'].drop()
    db['opt_clas'].drop()
    db['opt_crit'].drop()
    print('DB~ Drop Database')

def dropuser():
    db = get_rawdb()
    col = db['users']
    col.drop()
    user = {
        'name': 'admin',
        'pswd': generate_password_hash('admin'),
    }
    col.insert_one(user)  
    print('DB~ Reset admin password')
    dropblockuser(db)
    
def dropblockuser(db):
    db['block_user'].drop()
    n = int(os.getenv('ZIEM_WEB_BLOCKUSER_TIME', 3))
    db.create_collection('block_user')
    db['block_user'].create_index([( "time", pymongo.ASCENDING )], expireAfterSeconds=n)
    print(f'DB~ Drop block user, ttl {n} sec')
    
def write_log(code, msg='', src=''):
    col = get_col('logweb')
    codes = log_codes()
    if code in codes:
        desc = codes[code]
    else:
        desc = 'Описание не найдено'
        code = 2000
    data = {
        'time' : datetime.now(),
        'src' : src,
        'code': str(code),
        'desc' : desc,
        'msg': msg,
        'user': g.user,
    }
    col.insert_one(data)
    del data['_id']
    change_conf = (2104, 2105, 2106, 2109, 2110, 
                   2112, 2113, 2114, 2117, 2118, 2120)
    
    me = json.dumps(data, default=str, ensure_ascii=False)
    send_syslog(me)
    try:
        flog = '/var/log/ziem/web.log'
        log = logging.getLogger('web')
        h = RotatingFileHandler(flog, maxBytes=10000000, backupCount=10)
        f = logging.Formatter(os.environ['ZIEM_FORMAT_LOG'])
        h.setFormatter(f)
        log.addHandler(h)
        log.setLevel(logging.INFO)
        log.info(me)
    except Exception as e:
        logging.error(me + repr(e))
    

def log_codes():
    return {
        2100: 'Вход пользователя',
        2101: 'Выход пользователя',
        2103: 'Добавлено правило',
        2104: 'Изменено правило',
        2105: 'Скопировано правило',
        2106: 'Удалено правило',
        2107: 'Правила установлены в ядро ZIEM',
        2108: 'Правила экспортированы',
        2109: 'Добавлена УЗ для подлключения к источнику',
        2110: 'Изменена УЗ для подлключения к источнику',
        2111: 'Удалена УЗ для подключения к источнику',
        2112: 'Базовые настройки изменены',
        2113: 'Настройки добавлены через импорт данных',
        2114: 'Настройки изменены через импорт данных',
        2115: 'Настройки экспортированы',
        2116: 'Добавлен параметр',
        2117: 'Изменен параметр',
        2118: 'Удален параметр',
        2119: 'Перезапуск ядра ZIEM',
        2120: 'Обновление ZIEM',
        2121: 'Неуспешный вход пользователя',
        2122: 'Остановка ядра ZIEM',
        2123: 'Старт ядра ZIEM',
        2124: 'Добавлен пользователь ZIEM',
        2125: 'Изменен пользователь ZIEM',
        2126: 'Удален пользователь ZIEM',

    }

def send_syslog(message):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 514
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))    

def get_choice(select):
    if select == 'obj':
        choices = (
            [("main", "Основной")] + [(x['name'], x['name']) 
            for x in get_col('obj_rule').find().sort('name') 
            if x['name'] != 'main'])
    elif select == 'tax_main':
        choices = (
            [("", "---")] + [(x['name'], x['desc']) 
            for x in get_col('opt_taxmain').find().sort('desc')])
    elif select == 'tax_object':
        choices = (
            [("", "---")] + [(x['name'], x['desc']) 
            for x in get_col('opt_taxobject').find().sort('desc')])
    elif select == 'tax_action':
        choices = (
            [("", "---")] + [(x['name'], x['desc']) 
            for x in get_col('opt_taxaction').find().sort('desc')])
    elif select == 'crit':
        choices = (
            [("", "---")] + [(x['name'], x['desc']) 
            for x in get_col('opt_crit').find()])
    elif select == 'clas':
        choices = (
            [("", "---")] + [(x['name'], x['name']) 
            for x in get_col('opt_clas').find().sort('name')])
    elif select == 'field' or select == 'bks':
        choices = (
            [("", "---")] + [(x['name'], x['desc']) 
            for x in get_col(f'opt_{select}').find().sort('desc')])
    elif select == 'profile':
        choices = (
            [("", "---")] + [(x['name'], x['name']) 
            for x in get_col('opt_profile').find().sort('name')])
    elif select == 'protocol':
        choices = (
            [("", "---")] + [(x['name'], x['name']) 
            for x in get_col('opt_protocol').find().sort('name')])
    elif select == 'login':
        choices = (
            [("", "---")] + [(x['name'], x['name']) 
            for x in get_col('log_cred').find().sort('name')])
    elif select == 'normrule':
        choices = (
            [("", "---")] + [(x['name'], x['name']) 
            for x in get_col('nor_rule').find({'obj':'main'}).sort('name')])
    elif select == 'sub':
        choices = (
            [("", "---")] + [(x['name'], x['desc']) 
            for x in get_col('opt_sub').find().sort('desc')])
        
    elif select == 'type':
        choices = [("", "---")]
        col = get_col('opt_type')
        for x in col.find():
            if get_col('log_rule').find({'type': {'$eq': x['name']}}).count():
                choices += [(x['name'], x['desc'])]
                
    elif select == 'types':
        choices = (
            [("", "---")] + [(x['name'], x['desc']) 
            for x in get_col('opt_type').find().sort('desc')])
        
    elif select == 'backup':
        choices = (
        [('/log/get_backup/log_rule/current', 'Текущая конфигурация')] 
        + [('/log/get_backup/log_rule/' + str(x['_id']), x['time']) 
        for x in get_col('backup').find()])
    
    return choices