"""
    ZIEM
    Камнев Сергей

    Класс Сендера

"""

from .prots import Prots

# Отправитьель    
class Sender:
    
    senders = {}
    
    def __init__(self, opt):
        
        self.name = opt['name'] # Название   
        self.prot = opt['prot'] # протокол отправки
        self.ip = opt['ip'] 
        self.port = int(opt['port'])
        self.enabled = opt.get('enabled', True)
        self.alerts = opt['alrs'] 
        self.events = opt['eves'] 
        self.incs = opt['incs'] 
        
        self.alerts['time'] = f'{self.name}_{self.prot}_alrs'
        self.events['time'] = f'{self.name}_{self.prot}_eves'
        self.incs['time'] = f'{self.name}_{self.prot}_incs'
        self.repr = f'{self.name} {self.prot} {hex(id(self))}'
        self.senders.update({self.name: self})
        
    async def __call__(self, col, data):
        return await getattr(Prots(), f'send_{self.prot}')(col, data, self)
    
    def __repr__(self):
        return repr(self.repr)