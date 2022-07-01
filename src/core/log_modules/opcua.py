"""
    ZIEM
    Бенгарт Захар

    Модуль сбора сообщений с источника по протоколу OPC UA.
"""

import asyncio
from datetime import datetime
from asyncua import Client, Node, ua

if '__main__' != __name__:
    from ..db import log_error
    
class SubscriptionHandler:
    def __init__(self, ip, src_node, queue_alerts=None, queue_rep=None):
        self.ip = ip
        self.src_node = src_node
        self.queue_alerts = queue_alerts
        self.queue_rep = queue_rep

    def datachange_notification(self, node: Node, val, data):
        message = str(node) + ':' + str(val)
        #print('get sub change', message)
        alert = {
            'alr_time': datetime.now(),
            'alr_ip': self.ip,
            'alr_node': self.src_node,
            'alr_log': str(node),
            'alr_raw': message,
        }
        if self.queue_alerts is None:
            print(alert)
        else:
            self.queue_alerts.put_nowait(alert)
            self.queue_rep.put_nowait(alert)

async def opcua(agent, queue_alerts, queue_rep):
    try:
        ip = agent['ip']
        port = agent['port']
        node = agent['name']
        logs = agent['logs']
        url = 'opc.tcp://' + ip + ':' + port
        
        client = Client(url=url)
        #client.set_user(agent['login'])
        #client.set_password(agent['pswd'])
        
        # Успешное подключение
        raw = {
            'code': '1311',
            'ip': ip,
            'node': node,
            'desc': 'Успешное подключения к источнику'
        }
        alert = {
            'alr_ip': '127.0.0.1',
            'alr_node': 'ZIEM_ZIEM',
            'alr_time': datetime.now(),
            'alr_log' : 'ZIEM_ZIEM',
            'alr_raw' : raw,
            'ping': {'name': node, 'active': True, 'time': datetime.now()},
        }
        queue_alerts.put_nowait(alert)
        queue_rep.put_nowait(alert)
        while True:
            async with client as c:
                handler = SubscriptionHandler(ip, node, queue_alerts, queue_rep)
                subscription = await c.create_subscription(1000, handler)
                 #sub_nodes = [
                 #    'ns=2;s=RA_ENABLE',
                 #    'ns=2;s=ARM_OSN.test_int8.test_int8_1 102',
                 #    'ns=2;s=Application.GVL.gloobRA',
                 #]
                nodes = []
                sub_nodes = logs
                for s in sub_nodes:
                    nodes.append(
                        c.get_node(s),
                    )
                await subscription.subscribe_data_change(nodes)
                await asyncio.sleep(358000)
                #var = c.get_node("ns=2;s=ARM_OSN.test_int8.test_int8_1 102")
                #var = c.get_node("i=2254")
                #v = await var.read_value()
                #v = await var.write_value("test_ze")
    except Exception as e:
        # Успешное подключение
        raw = {
            'code': '1211',
            'ip': ip,
            'node': node,
            'desc': 'Ошибка подключения к источнику OPCUA'
        }
        alert = {
            'alr_ip': '127.0.0.1',
            'alr_node': 'ZIEM_ZIEM',
            'alr_time': datetime.now(),
            'alr_log' : 'ZIEM_ZIEM',
            'alr_raw' : raw,
            'ping': {'name': node, 'active': False, 'time': datetime.now()},
        }
        queue_alerts.put_nowait(alert)
        queue_rep.put_nowait(alert)
        log_error(e, '1208')
        
# TEST OPC UA

async def print_tree_node(node, fname, lvl=0):
    ch = await node.get_children()
    val = None
    try:
         val = await node.get_value()
    except: pass        
    
    if val is not None:
        v  = str(val).replace('\n', '  '*(1+lvl) )
        with open(fname, 'a') as f:
            f.write('  '*lvl + 'value: >\n' + '  '*(1+lvl) + v + '\n')
            
    for i in ch:
        with open(fname, 'a') as f:
            f.write('  '*lvl + f'{i}:\n')
            
        await print_tree_node(i, fname, lvl+1)

async def print_node(root, node, count=0):
    for ch in await root.get_children():
        count += 1
        if node in str(ch):
            try:
                val = await ch.get_value()
                print('\n\n', count, str(ch),':\n' , val)
            except: pass
        await print_node(ch, node, count+1)
      

async def test_opcua(ip, port, node):
    url = 'opc.tcp://' + ip + ':' + port
    client = Client(url=url, timeout=30000)
    try:
        async with client as c:
            root = c.get_root_node()
            if '' == node:
                with open('out_tree_node.yml', 'w') as f:
                    f.write('')
                await print_tree_node(root, 'out_tree_node.yml')
            else:
                await print_node(root, node)
    except Exception as e:
        print('ОШИБКА: ', e)
        
if '__main__' == __name__:
    
    
    import sys
    ip = sys.argv[1] if len(sys.argv) > 1 else input('ip: ')
    port = sys.argv[2] if len(sys.argv) > 2 else input('port: ')
    node = sys.argv[3] if len(sys.argv) > 3 else input('node: ')
                
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_opcua(ip, port, node))