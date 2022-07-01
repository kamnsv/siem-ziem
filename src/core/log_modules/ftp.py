"""
    ZIEM
    Бенгарт Захар

    Модуль сбора сообщений с источника по протоколу FTP.
    Работает в асинхронном режиме.
    Скачивает файл с применением оффсета каждую минуту.
"""

import asyncio
import aioftp
from os import makedirs
from datetime import datetime
import json

from ..db import log_error

async def ftp(agent, queue_alerts, queue_rep):
    # инициализация модуля
    try:
        alerts = []
        ip = agent['ip']
        ip2 = agent['ip_rez']
        port = port2 = 21
        if agent['port']:
            port = int(agent['port'])
        if agent['port_rez']:
            port2 = int(agent['port_rez'])
        node = agent['name']
        usr = agent['login']
        pswd = ''
        if 'pswd' in agent:
            pswd = agent['pswd']
        logs = agent['logs']
        time_sleep = 60
        PATH_LOG = "/var/opt/ziem/log/agents/ftp/" + node
        makedirs(PATH_LOG, exist_ok=True)
        while True:
            # подключение и скачивание каждого лога
            for log in logs:
                time = datetime.now()
                try:
                    alerts = await asyncio.wait_for(
                        get_log(ip, port, usr, pswd, log, PATH_LOG),
                        timeout=30)
                except:
                    if ip2: ip = ip2
                    if port2: port = port2
                    alerts = await asyncio.wait_for(
                            get_log(ip, port, usr, pswd, log, PATH_LOG),
                            timeout=30)
                # Успешное подключение
 
                raw = {
                    'code': '1311',
                    'ip': ip,
                    'node': node,
                    'desc': 'Успешное подключения к FTP источнику'
                }
                alert = {
                    'alr_ip': '127.0.0.1',
                    'alr_node': 'ZIEM_ZIEM',
                    'alr_time': datetime.now(),
                    'alr_log' : 'ZIEM_ZIEM',
                    'alr_raw' : raw,
                    'ping': {'name': node, 'active': True, 'time': datetime.now()},
                    
                }
                await queue_alerts.put(alert)
                await queue_rep.put(alert)
                    
                for a in alerts:
                    if a:
                        alert = {
                            'alr_time': time,
                            'alr_ip': ip,
                            'alr_node': node,
                            'alr_log': log,
                            'alr_raw': a,
                        }
                        await queue_alerts.put(alert)
                        await queue_rep.put(alert)
                await asyncio.sleep(5)
            await asyncio.sleep(time_sleep)
    except Exception as e:
        if ('Connect call failed' in repr(e) or
            'Login incorrect' in repr(e)):
            raw = {
                'code': '1211',
                'ip': ip,
                'node': node,
                'desc': 'Ошибка подключения к источнику'
            }
            alert = {
                'alr_ip':   '127.0.0.1',
                'alr_node': 'ZIEM_ZIEM',
                'alr_time': datetime.now(),
                'alr_log' : 'ZIEM_ZIEM',
                'alr_raw' : raw,
                'ping': {'name': node, 'active': False, 'time': datetime.now()},
                }
            await queue_alerts.put(alert)
            await queue_rep.put(alert)
        log_error(e, '1208')


async def get_log(ip, port, usr, pswd, log, PATH_LOG):
    # получение лога, используется оффсет файла при скачивании
    file = PATH_LOG + '/' + log.split('/')[-1]
    try:
        # чтение оффсета
        with open(file, "r") as f:
            offset = int(f.readline())
    except:
        offset = 0
        with open(file, "w") as f:
            f.write("0")
    async with aioftp.Client.context(ip, port, usr, pswd) as client:
        data = b''
        try:
            async with client.download_stream(log, offset=offset) as stream:
                async for block in stream.iter_by_block():
                    data += block
                if offset == 0:
                    # если оффсет 0, то данные обнуляем и не отправляем
                    offset += len(data)
                    data = b''
                else:
                    # увеличиваем оффсет
                    offset += len(data)
                with open(file, "w") as f:
                    f.write(str(offset))
        except Exception as e:
            if "StatusCodeError" in repr(e):
                # если ошибка по оффсету, то обнуляем его
                with open(file, "w") as f:
                    f.write("0")
            else:
                raise(e)
        return data.decode("utf-8").split('\n')