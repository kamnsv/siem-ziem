"""
    ZIEM
    Бенгарт Захар

    Модуль сбора сообщений с источника по протоколу Syslog.
"""

import asyncio
from datetime import datetime

from ..db import log_error

class EchoServerProtocol:
    def __init__(self, systems, queue_alerts, queue_rep):
        self.systems = systems
        self.queue_alerts = queue_alerts
        self.queue_rep = queue_rep
        self.con_lost = False

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            try:
                message = data[:1024].decode('utf-8')
            except:
                message = data[:1024].decode('cp1251')
            ip = addr[0]
            if ip in self.systems:
                node = self.systems[ip]['node']
                sub = self.systems[ip].get('sub')
                alert = {
                    'alr_time': datetime.now(),
                    'alr_ip': ip,
                    'alr_node': node,
                    'alr_sub': sub,
                    'alr_log': node,
                    'alr_raw': message,
                }
                self.queue_alerts.put_nowait(alert)
                self.queue_rep.put_nowait(alert)
        except Exception as e:
            log_error(e, '1207')

    def connection_lost(self):
        self.con_lost = True
    
async def syslog(agent, queue_alerts, queue_rep):
    #IP = '172.30.1.5' 
    IP = '0.0.0.0' 
    PORT = 514
    PORT_WIN = 5515
    try:
        systems = {}
        for a in agent:
            systems[a['ip']] = {
                'node': a['name'],
                'sub': a.get('sub')
            }
            if 'logs' in a:
                systems[a['ip']]['logs'] = a['logs']
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: EchoServerProtocol(systems, queue_alerts, queue_rep),
            local_addr=(IP, PORT))
        #transport, protocol = await loop.create_datagram_endpoint(
        #    lambda: EchoServerProtocol_Win(systems, queue_alerts, queue_rep, loop, task_name),
        #    local_addr=(IP, PORT_WIN))
        while True:
            await asyncio.sleep(3600)
    except Exception as e:
        log_error(e, '1208')
