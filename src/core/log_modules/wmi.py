"""
    ZIEM
    Бенгарт Захар

    Модуль сбора сообщений с источника ОС Windows.
    Используется протокол WMI для подключения к источнику.
    Происходит подписка на сообщения с журналов,
    которые отправляются обратно раз в 10 секунд.
    Далее происходит быстрый поиск по сырым бинарным данным.
"""

import asyncio
from datetime import datetime

from .wmi_modules.dtypes import NULL
from .wmi_modules.dcomrt import DCOMConnection
from .wmi_modules import wmi as impacket_wmi
from .wmi_modules.rpcrt import RPC_C_AUTHN_LEVEL_PKT_INTEGRITY
from .wmi_modules.structure import hexdump

from ..rep import log_error
import json


class WMISubscription:
    """
    Class for subscrpition to EventLog via WMI
    """
    def __init__(self):
        self.lTimeout = 0x00002710
        self.uCount = 100

    async def run(self, agent, queue_alerts, queue_rep):
        username = agent['login']
        password = ''
        if 'pswd' in agent:
            password = agent['pswd']
        ip = agent['ip']
        ip2 = agent['ip_rez']
        node = agent['name']
        logs = agent['logs']
        query = "select * from __InstanceCreationEvent WHERE TargetInstance isa 'Win32_NTLogEvent' and ("
        for log in logs:
            query += "TargetInstance.LogFile='" + log + "' OR "
        query = query[:-4] + ")"
        try:
            dcom = DCOM(ip, ip2, username, password)
            
            async with dcom:
                iEnum = IEnum(dcom.connection, query)
                # Успешное подключение
                raw = {
                    'code': '1311',
                    'ip': ip,
                    'node': node,
                    'desc': 'Успешное подключения к WMI источнику'
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
                
                async with iEnum:
                    self.request_init(iEnum.connection)
                    while True:
                        alerts = []
                        response = await asyncio.wait_for(
                            self.next_fast(iEnum.connection), timeout=15)
                        if len(response) < 2000:
                            if response[-4:] == b'\x04\x00\x04\x00':
                                continue
                            else:
                                break
                        alerts = self.parse_fast(ip, node, response)
                        for alert in alerts:
                            await queue_alerts.put(alert)
                            await queue_rep.put(alert)
                        await asyncio.sleep(1)
        except Exception as e:
            if ('Connect call failed' in repr(e) or
                'TimeoutError' in repr(e)):
                raw = {
                    'code': '1211',
                    'ip': ip,
                    'node': node,
                    'desc': 'Ошибка подключения к источнику'
                }
                alert = {
                    'alr_ip': '127.0.0.1',
                    'alr_node': 'ZIEM_ZIEM',
                    'alr_time': datetime.now(),
                    'alr_log' : 'ZIEM_ZIEM',
                    'alr_raw' : raw,
                    'ping': {'name': node, 'active': False, 'time': datetime.now()},
                    }
                await queue_alerts.put(alert)
                await queue_rep.put(alert)
            log_error(e, '1208')

    def request_init(self, iEnum):
        self.request = impacket_wmi.IEnumWbemClassObject_Next()
        self.request['lTimeout'] = 0x00002710
        self.request['uCount'] = 100
        self.request['ORPCthis'] = iEnum.get_cinstance().get_ORPCthis()
        self.request['ORPCthis']['flags'] = 0
        #await iEnum.connect(iEnum._iid)
        self.dce = iEnum.get_dce_rpc()

    async def next_fast(self, iEnum):
        await self.dce.call(self.request.opnum, 
                            self.request, 
                            iEnum.get_iPid())
        await asyncio.sleep(11)
        response = await self.dce.recv()
        return response

    def parse_fast(self, ip, node, raw):
        """
        fast parse raw packets from recieved objects
        """
        alerts = []
        time = datetime.now()
        # split raw data for events by b'MEOW'
        for raw_b in raw.split(b'\x4d\x45\x4f\x57')[1:]:
            # search offset to 'Win32_NTLogEvent' in raw data
            i = 0x0900
            offset = 0
            while i < 0x0a00:
                if raw_b[i:i + 7] == b'\x57\x69\x6E\x33\x32\x5F\x4E':
                    offset = i
                    break
                else:
                    i += 1
            if offset == 0:
                raise Exception('Parse packet error')
            # search EventCode, start from offset - 55
            event_code = str(
                int.from_bytes(raw_b[offset - 55 : offset - 53], 'little'))
            # search RecordNumber, start from offset - 67
            record_number = str(
                int.from_bytes(raw_b[offset - 67 : offset - 63], 'little'))
            # search LogFile, Time, ComputerName
            data = self.parse_array(raw_b[offset + 17:offset + 300], 6)
            log_name = data[0]
            time_generated = data[4]
            computer_name = data[5]
            # search InsertionStrings
            # first find offset, where strings start
            strings_offset = int.from_bytes(
                raw_b[offset - 19 : offset - 17], 'little')
            strings_offset = offset - 1 + strings_offset
            # need add (items count * size 4 bytes) to offset
            items_count = int.from_bytes(
                raw_b[strings_offset :strings_offset + 2], 'little')
            strings_offset += items_count*4 + 4
            raws = raw_b[strings_offset : strings_offset + 2048]
            # split \x00... trash data and add last delimiter
            raws = raws.split(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')[0]
            raws += b'\x00\x00\x00\x02'
            # search data in strings, k - begin data, i - end data
            i = k = 0
            strings = self.parse_array(raws, items_count)
            alerts.append({
                'alr_ip': ip,
                'alr_node': node,
                'alr_time': time,
                'alr_log' : log_name,
                'alr_code': event_code,
                'alr_raw' : strings,
                'alr_rec' : record_number,
                'time': time_generated,
                'name': computer_name,
                })
        return alerts

    def parse_array(self, data_raw, min_length):
        try:
            data = []
            while len(data) < min_length:
                d = ''
                i = 1
                if data_raw[0] == 0x00:
                    while data_raw[i] != 0x00:
                        i += 1
                    d = data_raw[1:i].decode('utf-8')
                elif data_raw[0] == 0x01:
                    while data_raw[i:i + 2] != b'\x00\x00':
                        i += 2
                    d = data_raw[1:i].decode('utf-16le')
                    i += 1
                data.append(d)
                data_raw = data_raw[i + 1:]
            return data
        except:
            return []

class DCOM:
    def __init__(self, ip, ip2, username, password):
        self.domain = ''
        self.lmhash = ''
        self.nthash = ''
        self.options_aesKey = ''
        self.ip = ip
        self.ip2 = ip2
        self.username = username
        self.password = password
        self.dcom = ''

    async def connect(self):
        self.connection = DCOMConnection(self.ip, self.username, self.password, 
                                   self.domain, self.lmhash, self.nthash, 
                                   self.options_aesKey, oxidResolver=False, 
                                   doKerberos='', kdcHost='')
        await self.connection.initConnection()

    async def __aenter__(self):
        try:
            await self.connect()
        except:
            if self.ip2:
                self.ip = self.ip2
                await self.connect()
            else:
                raise

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.disconnect()


class IEnum:
    def __init__(self, dcom, query):
        self.namespace = '//./root/cimv2'
        self.dcom = dcom
        self.query = query
        self.connection = ''

    async def connect(self):
        iInterface = await self.dcom.CoCreateInstanceEx(
            impacket_wmi.CLSID_WbemLevel1Login, 
            impacket_wmi.IID_IWbemLevel1Login)
        iWbemLevel1Login = impacket_wmi.IWbemLevel1Login(iInterface)
        iWbemServices= await iWbemLevel1Login.NTLMLogin(self.namespace, 
                                                        NULL, NULL)
        iWbemServices.get_dce_rpc().set_auth_level(RPC_C_AUTHN_LEVEL_PKT_INTEGRITY)
        await iWbemLevel1Login.RemRelease()
        self.connection = await iWbemServices.ExecNotificationQuery(self.query, 48)

    async def __aenter__(self):
        await self.connect()

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.disconnect()
