"""
    ZIEM
    Камнев Сергей

    Модуль поиска node OPC Alarm & Event.
"""
# SEARCH OPC AE
if '__main__' == __name__:
    
    import asyncio
    from asyncua import Client, Node, ua
    import sys
    ip = sys.argv[1] if len(sys.argv) > 1 else input('ip: ')
    port = sys.argv[2] if len(sys.argv) > 2 else input('port: ')
    
    async def search_ae(root, ae):
        for ch in await root.get_children():
            if str(ch).endswith('.5000'): 
                try:
                    val = await ch.get_value()
                    # '{ ModuleId=(AeServer) Protocol=(OPCAE) Conditions=(Message) }'
                    if 'Protocol=(OPCAE)' in val:
                        ae.append(str(root))
                except: pass 
            await search_ae(ch, ae)
        
        
    async def get_opcae(ip, port, lgn=None, psw=None):
        url = 'opc.tcp://' + ip + ':' + port
        client = Client(url=url, timeout=30000)
        if lgn: client.set_user(lgn)
        if psw: client.set_password(psw)
        ae = []
        try:
            async with client as c:
                root = c.get_root_node()
                await search_ae(root, ae)
        except Exception as e:
            print('ОШИБКА: ', e)
        print(len(ae), '\n'.join(ae))
        return ae
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_opcae(ip, port)) 
     
    sys.exit(0)

