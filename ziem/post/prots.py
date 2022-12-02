"""
    ZIEM
    Камнев Сергей

    Протоколы Отправки данных

"""

import os
import json
import aiohttp
import asyncio
import logging
import socket
import time
from asyncua import Client, Node, ua
from aiohttp import TCPConnector

class Consend:
    
    def __init__(self, ip:str, port:str, url=''):
        self.ip = ip
        self.port = int(port)
        self.url = url
        self.timeout = int(os.getenv('ZIEM_POST_TIMEOUT', '20'))
    
    # Обогащение данных для передачи, перевод в строку
    async def dump(self, data):
        return json.dumps({"ServiceName": "Ziem",  "Data": data}, indent=4, default=str, ensure_ascii=False)
    
    # подключение
    async def connect(self):
        logging.debug(f'{self} подключение...')
        
    # отправка        
    async def send(self, data):
        data = await self.dump(data)
        logging.debug(f'{self} отправка: {data}')
        
    # закрытие
    async def close(self):
        logging.debug(f'{self} закрытие...')
    
    async def __aenter__(self):
        await self.connect()
        
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()
        

        
class SendTCP(Consend):   #async
        
    async def connect(self):
        self.start = time.time()
        
        fut = asyncio.open_connection(self.ip, self.port)
        try:
            self.reader, self.writer = await asyncio.wait_for(fut, timeout=self.timeout)
        except asyncio.TimeoutError:
            raise Exception(f'Timeout, skipping {self.ip}:{self.port}')

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
        #print('time:', time.time()-self.start)
    
    async def send(self, data):
        n = len(data)
        data = await self.dump(data)
        data_bytes = bytes(data + '\n', 'UTF-8')
        #print('len bytes', len(data_bytes),n)
        
        self.writer.write(data_bytes)
        await self.writer.drain()

        out = await self.reader.read(100)
        #print(out)
        if b'200' != out:
            raise Exception(f'Ответа TCP {out}')
               
            
            
class sSendTCP(Consend):  #sync
    
    async def connect(self):
        self.start = time.time()
        self.__s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__s.settimeout(self.timeout)
        self.__s.connect((self.ip, self.port))
    
    
    async def close(self):
        self.__s.close()
        print('time:', time.time()-self.start)
        
    async def send(self, data):
        n = len(data)
        data = await self.dump(data)
        data_butes = bytes(data + '\n', 'UTF-8')
        print('len bytes', len(data_butes),n)
       # print(data_butes)
        self.__s.sendall(data_butes)
        out = self.__s.recv(1024)
        if b'200' != out:
            raise Exception(f'Ответа TCP {out}')
                       
        
class SendHTTP(Consend):
    async def connect(self):
        self.adr = f'http://{self.ip}:{self.port}/{self.url}'
        if 443 == self.port:
            self.adr = f'https://{self.ip}/{self.url}'
        self.headers = {'content-type': 'application/json'}
        
    async def send(self, data):
        
        data = await self.dump(data)
        async with aiohttp.ClientSession(connector=TCPConnector(ssl=False), conn_timeout=self.timeout) as cs: 
            async with cs.post(self.adr, data=data, headers=self.headers) as resp:
                if '200' == resp.status:
                    raise Exception(f'Код ответа {resp.status} от "{self.adr}"')
                

        
class SendUDP(Consend):
    async def connect(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
             
    async def send(self, data):
        data = await self.dump(data)
        self.__s.sendto(bytes(data + '\n', 'UTF-8'), (self.ip, self.port))
        
class SendOPCUA(Consend):
    async def connect(self):
        url = f'opc.tcp://{self.ip}:{self.port}'
        self.__s = client = Client(url=url)
    
    async def close(self):
        await self.__s.disconnect()
        
    async def send(self, data):
        data = await self.dump(data)
        async with self.__s as c:
            var = c.get_node(self.url)
            v = await var.write_value(data)
        

        
# Протоколы отправки   
class Prots:
    # Методы принимают название коллекции, массив данных и Сендер
    # Все методы возвращают результат - целое число:
    # -1: успешна отправка
    # -2: ошибка соединения
    # >= 0: номер не отправленного сообщения
    
    async def __call__(self, col, data, sender):
        return await getattr(self, f'send_{sender.prot}')(col, data, sender)
    
    async def send_data(self, col: str, data: list, colsend)-> int:
        try:
            await colsend.connect()
        except Exception as e: 
            logging.error(f'Ошибка соединения {colsend} {e}')
            return -2
            
        if 'incs' == col and list == type(data):
            
            for i, d in enumerate(data):
                try:
                    await colsend.send(d)
                except Exception as e:
                    logging.error(f'Ошибка {colsend} отправки инцидента {d} {e}')
                    await colsend.close()
                    return i

        else: # alrs, eves
                
                try:
                    await colsend.send(data) 
                except Exception as e: 
                    logging.error(f'Ошибка {colsend} отправки пакета {col} {e}')
                    await colsend.close()
                    return 0
                
        await colsend.close()        
        return -1 

    # Syslog по UDP
    async def send_sysudp(self, col: str, data, sender) -> int:
        colsend = SendUDP(sender.ip, sender.port, getattr(sender, col)['url'])
        return await self.send_data(col, data, colsend)
    
    # Syslog по TCP
    async def send_systcp(self, col: str, data, sender) -> int:
        colsend = SendTCP(sender.ip, sender.port, getattr(sender, col)['url'])
        return await self.send_data(col, data, colsend)
                
    async def send_http(self, col: str, data, sender) -> int:
        colsend = SendHTTP(sender.ip, sender.port, getattr(sender, col)['url'])
        return await self.send_data(col, data, colsend)

    async def send_opcua(self, col: str, data, sender) -> int:
        colsend = SendOPCUA(sender.ip, sender.port, getattr(sender, col)['url'])
        return await self.send_data(col, data, colsend)