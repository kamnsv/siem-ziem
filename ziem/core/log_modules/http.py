"""
    ZIEM
    Бенгарт Захар

    Модуль сбора сообщений с источника по протоколу HTTP.
"""

import asyncio
from aiohttp import web
from datetime import datetime
from ..db import log_error

class Http_server():
    """
    The main class for ZIEM
    """

    def __init__(self, agent, queue_alerts, queue_rep):
        self.IP = "0.0.0.0"
        self.PORT = 46600
        self.queue_alerts = queue_alerts
        self.queue_rep = queue_rep
        self.systems = {}
        for a in agent:
            self.systems[a['name']] = {
                'node': a['name'],
            }

    async def run(self):
        server = web.Server(self.putlogs)
        runner = web.ServerRunner(server)
        await runner.setup()
        site = web.TCPSite(runner, self.IP, self.PORT)
        await site.start()

    async def putlogs(self, request):
        try:
            name = request.headers['name']
            name = 'TVV_SIKN432'
            data = await request.json()
            if name in self.systems:
                for d in data:
                    alert = {
                        'alr_time': datetime.now(),
                        'alr_ip': request.remote,
                        'alr_node': name,
                        'alr_log': name,
                        'alr_raw': d,
                    }
                    await self.queue_alerts.put(alert)
                    await self.queue_rep.put(alert)                    
                return web.Response(text="ok")
        except Exception as e:
            print(e)
            log_error(e, '1208')
    
async def http(agent, queue_alerts, queue_rep):
    #IP = '172.30.1.5' 
    http_server = Http_server(agent, queue_alerts, queue_rep)
    loop = asyncio.get_running_loop()
    loop.create_task(http_server.run(), name='LOG-http')
    while True:
        await asyncio.sleep(100*3600)
