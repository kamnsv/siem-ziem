"""
    Agent for remote control ZIEM

    Description:
        Agent for ZIEM remote managment.
        It connect every XXX seconds to ZIEM and get info about update.
        If necessary it update self, ZIEM, ZIEM configuration.

    Author:
        Bengart Zakhar
        Kamnev Sergey
"""

import os
import json
import asyncio
import aiohttp
import logging
import subprocess
import pkg_resources
from aiohttp import TCPConnector
from getpass import getpass
from cryptography.fernet import Fernet

from logging.handlers import RotatingFileHandler
from .db import Database

class Ziemagent():
    """
    Main class for ZIEM Agent
    """
    def __init__(self, port=None):
        if port is None: port = '46000'
        self.init_log()
        self.port = port
        self.http = 'https://'
        self.config = {
            'name': '',
            'ziemcc_ip': '',
            'obj_id': '',
            'token': '',
        }
        
        try:
            self.read_config()
        except Exception as e: 
            print("Initialization read config error: " + repr(e))
        try:
            self.read_crypto()
        except Exception as e: 
            print("Initialization read crypto error: " + repr(e))
        
        self.host = self.config.get('ziemcc_ip')
        self.config['ziemcc_port'] = port
        self.obj  = self.config.get('obj_id')
        self.name  = self.config.get('name')
        self.token = self.config.get('token')
        #self.log.error("Initialization error: " + repr(e))
        
        self.period = int(os.getenv('ZIEMAGENT_PERIOD', '10'))
        
        
    def init_log(self):
        """
        Configure Agent self.log
        """
        flog = '/var/log/ziem/agent.log'
        self.log = logging.getLogger('agent')
        h = RotatingFileHandler(flog, maxBytes=10000000, backupCount=10)
        f = logging.Formatter(os.environ['ZIEM_FORMAT_LOG']) 
        h.setFormatter(f)
        self.log.addHandler(h)
        self.log.setLevel(logging.INFO)   
        
    def read_crypto(self):
        """
        Configure Agent crypto keys
        """
        with open('/etc/opt/ziem/agent.k', 'rb') as f:
            key = f.read()
        self.fern_key = Fernet(key)
        self.config['token'] = self.fern_key.decrypt(self.config['token'].encode()).decode()

    def read_config(self):
        try:
            with open('/var/opt/ziem/agent', 'r') as f:
                data = json.load(f)
        except: return 
        self.config.update(data)
        #raise Exception("Config not set, run: ziemagent --setconfig")

    def setconfig(self):
        """
        Configure ziemagent
        """
        self.config['name'] = input('Enter ziemagent name: ')
        self.config['ziemcc_ip'] = input('Enter ZIEMCC IP: ')
        with open('/var/opt/ziem/agent', 'w') as f:
            json.dump(self.config, f, indent=4, default=str, ensure_ascii=False)
        self.log.info("Change ziemagent config")

    def showconfig(self):
        """
        Show ziemagent config
        """
        with open('/var/opt/ziem/agent', 'r') as f:
            data = f.read()
        print('Current ziemagent config')
        print(data)

    async def run(self):
        """
        Main function for run Agent
        """
        while True:
            await asyncio.wait_for(self.putversion() ,timeout=30)
            
            await asyncio.sleep(self.period)
        
            isupdate = await self.getupdate()
            
            
            
            if isupdate is None: continue
            
            self.log.info("Update data: " + json.dumps(isupdate))
            
            
            if isupdate.get('updateziem'):
                await asyncio.wait_for(self.updateziem(isupdate) ,timeout=30)
                
            if isupdate.get('updateconfig'):
                data = await asyncio.wait_for(self.getconfweb(), timeout=30)
                await self.saveconfweb(data)
                self.saveconf(data)
                
            if isupdate.get('updateagent'):
                await asyncio.wait_for(self.updateagent(isupdate) ,timeout=30)
                
    async def getupdate(self):
        #print('Get update info from ZIEM Center')
        url = self.http + self.host + f':{self.port}/obj/getupdate' 
        params = {
            'name': self.config['name']
        }
        data = None
        try:
            async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.get(url, params=params) as resp:
                    data = await resp.json()
            self.log.info("Get update info from ZIEM Center")
            return data
        except Exception as e:
            self.log.error("Cant update ziemagent: " + repr(e))

    
    async def updateagent(self, isupdate):
        #print('Update Agent')
        try:
            self.log.info("Starting update ziemagent...")
            repo = self.host + ':' + self.port + '/pypirepo'
            cmd = f'sudo /opt/ziem/venv/bin/pip install --trusted-host {self.host} '
            cmd += f'--index-url {self.http}{self.obj}:{self.token}@{repo} '
            cmd += 'ziemagent -U -I --disable-pip-version-check'
            os.system(cmd)
            self.log.info("Update ziemagent complete, restarting...")
            os.system('sudo systemctl restart ziemagentd')
        except Exception as e:
            self.log.error("Cant update ziemagent: " + repr(e))
            await asyncio.sleep(10)
            

    async def updateziem(self, isupdate):
        print('Update ZIEM')
        try:
            self.log.info("Starting update ziem...")
            self.log.info("Starting update ziemagent...")
            repo = self.host + ':' + self.port + '/pypirepo'
            cmd = f'sudo /opt/ziem/venv/bin/pip install --trusted-host {self.host} '
            cmd += f'--index-url {self.http}{self.obj}:{self.token}@{repo} '
            cmd += 'ziem -U -I --disable-pip-version-check'
            os.system(cmd)
            self.log.info("Update ziem complete, restarting services...")
            os.system('sudo systemctl restart ziemcored')
            os.system('sudo systemctl restart ziemwebd')
            os.system('sudo systemctl restart ziempostd')
        except Exception as e:
            self.log.error("Cant update ziem: " + repr(e))
            await asyncio.sleep(10)

    async def putversion(self):
        """
        Put installed Agent and ZIEM versions to ZIEM Center
        """
        cmd = '/opt/ziem/venv/bin/pip freeze | grep %s=='
        version_ziem = os.popen(cmd % 'ziem').read().strip().split('==')[-1]
        version_agent = os.popen(cmd % 'ziemagent').read().strip().split('==')[-1]
        data = {
            'name': self.config['name'],
            'version_ziem': version_ziem,
            'version_agent': version_agent,
        }
        url = self.http + self.host + f':{self.port}/obj/putversion'
        headers = {'content-type': 'application/json'}
        pload = json.dumps(data, indent=4, default=str, ensure_ascii=False)
        try:
            async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.put(url, 
                                       data=pload, 
                                       timeout=10, 
                                       headers=headers) as resp:
                    if resp.status != 200:
                        self.log.error("Cant put versions, response:" + 
                                      str(resp.status))
            self.log.info("Put ziemagent version to center: " + version_agent)
            self.log.info("Put ziem version to center: " + version_ziem)
        except Exception as e: 
            self.log.error("Cant putversion ziemagent: " + repr(e))
            

    def saveconf(self, data):
        """
        Save ZIEM working configs and rules to /var/opt/ziem/...
        """
        os.system('/opt/ziem/venv/bin/ziem --confinstall')
        os.system('systemctl restart ziemcored')
        self.log.info("Save ziem config, restart CORE")

    async def getconfweb(self):
        """
        Get ZIEM Web configs and rules
        """
        url = self.http + self.host + f':{self.port}/obj/getconfweb'
        params = {
            'name': self.config['name']
        }            
        auth = aiohttp.BasicAuth(login=self.config['obj_id'], 
                                 password=self.config['token'], 
                                 encoding='utf-8')
        try:
            async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.get(url, params=params, timeout=10, auth=auth) as resp:
                    if 200 == resp.status:
                        data = await resp.json()
                        
                        return data
                    else:
                        raise  Exception("Code status server: " + resp.status)
        except Exception as e:
                self.log.error("Connection to ZIEMCC getconfweb failed - " + repr(e))
                await asyncio.sleep(10)
                return await self.getconfweb()

    async def saveconfweb(self, data):
        """
        Save ZIEM Web configs and rules to DB
        """
        webdb = Database()
        async with await webdb.client.start_session() as s:
            for d in data:
                if data[d]:
                    await webdb.write(d, data[d])
        self.log.info("Save ziem web config")

    async def connect(self):
        """
        Connect to ZIEM CC
        """
        url = self.http + self.host + f':{self.port}/obj/connect'
        async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
            pswd = getpass("Enter password to connect: ")
            data = {
                'username': self.config['name'],
                'password': pswd,
            }
            headers = {'content-type': 'application/json'}
            pload = json.dumps(data, indent=4, default=str, ensure_ascii=False)
            async with session.post(url, data=pload, timeout=10, headers=headers) as resp:
                if resp.status != 200:
                    self.log.error("Connection to ZIEMCC failed - " + str(resp.status))
                else:
                    resp_text = await resp.json()
                    self.config['token'] = self.fern_key.encrypt(resp_text['token'].encode()).decode()
                    self.config['obj_id'] = resp_text['obj_id']
                    with open('/var/opt/ziem/agent', 'w') as f:
                        json.dump(self.config, f, indent=4, default=str, ensure_ascii=False)
                    self.log.info("Connected to ZIEMCC")
            return data        