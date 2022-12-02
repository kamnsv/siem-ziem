"""
    ZIEM
    Бенгарт Захар

    Модуль опроса сети и определения доступности источников.
    Посылает каждую минуту PING запросы по протоколу ICMP.
    Если в течение 3 раз не пришел ответ, источник считается недоступным.
"""

import json
import asyncio
from datetime import datetime
import os 

from ..db import log_error

async def netmap(agent, queue_alerts, queue_rep):
    try:
        i = 0
        hosts = { ip: {} for ip in agent}
        while "true":
            for ip, node in agent.items():
                if ip == '127.0.0.1':
                    continue
                send = False
                if i == 0:
                    hosts[ip]['count'] = 0
                response = await ping(ip)
                if response == 1:
                    hosts[ip]['count'] += 1
                elif response == 0:
                    hosts[ip]['count'] = 0
                if hosts[ip]['count'] == 3:
                    raw = {
                        'code': '1213',
                        'ip': ip,
                        'node': node,
                        'desc': 'Источник недоступен по сети'
                    }
                    alert = {
                        'alr_ip': '127.0.0.1',
                        'alr_node': 'ZIEM_ZIEM',
                        'alr_sub': agent.get('sub'),
                        'alr_time': datetime.now(),
                        'alr_log' : 'ZIEM_ZIEM',
                        'alr_raw' : json.dumps(raw, default=str, ensure_ascii=False),
                        }
                    await queue_alerts.put(alert)
                    await queue_rep.put(alert)
                    log_error(ip, '1213')
            i += 1
            if i == 86300:
                i = 0
            await asyncio.sleep(60)
    except Exception as e:
        log_error(e, '1210')

async def ping(ip):
    cmd = 'ping -4 -c1 -W1 ' + ip
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stderr:
        return 1
    if '1 received' in stdout.decode('utf-8'):
        return 0
    else:
        return 1
    
def pinger(ip):
    cmd = f'ping -4 -c1 -W1 {ip} | grep time'
    return os.popen(cmd).read().strip()