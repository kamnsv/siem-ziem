import os
import time
import random
import string
import asyncio
from cryptography.fernet import Fernet
from ziem.web import dropuser
from ziem.core import dropdb


def init(center=0):
    if center == True: center = 1
    if type(center) == str and center.isdigit(): 
        center = int(center)
        
    init_user()
    init_dirs()
    key = init_crypto()
    init_web(key)
    init_mongo(key)
    init_right()
    asyncio.run(dropdb())
    path = os.path.dirname(os.path.abspath(__file__))
    venv_path = path.split("/lib/")[0]
    
    os.system('chown -R root ' + venv_path)
    os.system('chgrp -R root ' + venv_path)
    os.system('chmod u=rwx,g=rx,o=rx ' + venv_path)
    if center in (0, 2): install_bin()
    init_nginx(center)
    install_cert()
    init_services(center)
    os.system('ziemcored.service ziemwebd.service ziempostd.service mongod') 
    install_sudo()
    
    os.system("systemctl enable ziemwebd")
    
    if not center:
        os.system("systemctl enable ziemcored")
        os.system("systemctl enable ziempostd")
    
    print('\n\n[+] Installation complete. Please reboot')

    
    
def init_services(center=0):
    
    install_webservice(center)
    
    if center in (0, 2):
        install_coreservice()
        install_postservice()
    else:
        print('Remove ziemcored, ziempostd')
        os.system('sudo rm /etc/systemd/system/ziemcored.service')
        os.system('sudo rm /etc/systemd/system/ziempostd.service')
        
    os.system('sudo systemctl daemon-reload')
    
def init_user():
    print('\n[*] Add system user\n----------------')
    print('zuser')
    os.system("useradd -r -s /bin/false zuser")

def init_dirs():
    print('\n[*] Creating dirs\n----------------')
    dirs = [
        '/etc/opt/ziem/',
        '/var/opt/ziem/status',
        '/var/opt/ziem/conf',
        '/var/opt/ziem/cor/diff',
        '/var/opt/ziem/cert',
        '/var/log/ziem/',
    ]
    os.system("rm -rf /etc/opt/ziem/")
    os.system("rm -rf /var/opt/ziem/")
    os.system("rm -rf /var/log/ziem/")
   
    for d in dirs:
        os.system("mkdir -p " + d)
        print(d)
    
    with open('/var/log/ziem/ziem.log', 'w') as f:
        f.write('')    
        
def init_crypto():
    print('\n[*] Creating main crypto key\n----------------')
    print('/etc/opt/ziem/ziem.k')
    fern_key = Fernet.generate_key()
    with open('/etc/opt/ziem/ziem.k', 'wb') as f:
        f.write(fern_key)
    return fern_key

def init_web(key):
    print('\n[*] Creating web crypto key\n----------------')
    print('/etc/opt/ziem/web.k')
    web_key = os.urandom(16)
    fern_key = Fernet(key)
    with open('/etc/opt/ziem/web.k', 'wb') as f:
        f.write(fern_key.encrypt(web_key))    
    
def init_mongo(key):
    print('\n[*] Creating cfg mongo\n----------------')
    print('zuser')
    conf = ('storage:\n'
            '  dbPath: /var/lib/mongodb\n'
            '  journal:\n'
            '   enabled: true\n'
            'systemLog:\n'
            '  destination: file\n'
            '  logAppend: true\n'
            '  path: /var/log/mongodb/mongod.log\n'
            'net:\n'
            '  port: 27017\n'
            '  bindIp: 127.0.0.1\n'
            'processManagement:\n'
            '  timeZoneInfo: /usr/share/zoneinfo\n')
    with open('/etc/mongod.conf', 'w') as f:
        f.write(conf)
    os.system("systemctl restart mongod")    
    time.sleep(1)
    
    print('\n[*] Drop user mongo\n----------------')
    
    mongo_cmd = 'db.getSiblingDB("ziem").dropUser("zuser")'
    os.system("mongo --eval '" + mongo_cmd + "'")
    
    mongo_cmd = 'db.dropUser("repl")'
    os.system("mongo --eval '" + mongo_cmd + "'")

    print('\n[*] Creating mongo user\n----------------')
    pwd = ''.join(random.choices(string.ascii_letters + string.digits, k = 16))   
    mongo_cmd = 'db.getSiblingDB("ziem").createUser({user:"zuser",pwd:"'\
                + pwd + '", roles:[{role:"readWrite",db:"ziem"}]})'
    os.system("mongo --eval '" + mongo_cmd + "'")
   
    mongo_cmd = 'db.createUser({user:"repl",pwd:"'+pwd+'",roles:[{role:"clusterManager",db:"admin"},{role:"dbOwner", db:"adminsblog"},{role:"readWrite", db:"departmentblog"},{role:"read", db:"otherblog"}]})'
    os.system("mongo --eval '" + mongo_cmd + "'")
    
    print('\n[*] Creating rep_key mongo\n----------------')
    os.system("openssl rand -base64 756 > /etc/opt/ziem/rep_key")
    os.system("chown mongodb /etc/opt/ziem/rep_key")
    os.system("chmod 400 /etc/opt/ziem/rep_key")
    
    print('\n[*] Add cfg mongo \n----------------')
    conf += ('security:\n'
             '  authorization: enabled\n'
         #    '  keyFile: /etc/opt/ziem/rep_key\n'
         #    'replication:\n'
         #    '  replSetName: zrepl\n'
    )
    with open('/etc/mongod.conf', 'w') as f:
        f.write(conf)
    os.system("systemctl restart mongod")
    time.sleep(1)
    os.system("systemctl status mongod")
    
    print('\n[*] Initiate replication mongo \n----------------')
    #mongo_cmd = f'mongo --eval "db.auth(\'repl\', \'{pwd}\'); rs.initiate()"'
    #print(mongo_cmd)
    #print(os.popen(mongo_cmd).read())
    print(pwd)
    print('\n[*] Put crypto key for mongo \n----------------')
    conn_str = 'mongodb://zuser:'\
               + pwd + '@localhost/?authSource=ziem&authMechanism=SCRAM-SHA-256'
    connweb_str = 'mongodb://zuser:'\
               + pwd + '@localhost/ziem?authSource=ziem&authMechanism=SCRAM-SHA-256'
    fern_key = Fernet(key)
    
    with open('/etc/opt/ziem/db', 'w') as f:
        f.write(fern_key.encrypt(conn_str.encode()).decode())
    with open('/etc/opt/ziem/db_web', 'w') as f:
        f.write(fern_key.encrypt(connweb_str.encode()).decode())
    dropuser()
        
def init_right():
    print('\n[*] Chown zuser to dirs\n----------------')
    dirs = [
        '/var/log/ziem/', 
        '/var/opt/ziem/'
    ]
    for d in dirs:
        os.system("chown -R zuser " + d)
        print(d)
    print('\n[*] Change priv to dir\n----------------')
    print('/etc/opt/ziem')
    os.system("chgrp -R zuser /etc/opt/ziem")
    os.system("chmod -R o-r /etc/opt/ziem")
    print('\n[*] Set port 514 to unprivileged mode"\n----------------')
    lines = []
    with open('/etc/sysctl.conf', 'r') as f:
        lines = f.readlines()
    if 'net.ipv4.ip_unprivileged_port_start=514' not in lines:
        os.system("sudo echo net.ipv4.ip_unprivileged_port_start=514 | sudo tee -a /etc/sysctl.conf ") 
    os.system("sysctl net.ipv4.ip_unprivileged_port_start=514")

def init_cron():
    print('\n[*] Add cron job\n----------------')
    job = ('#!/bin/bash\n'
        '/usr/bin/ziem --cleardb')
    print(job)
    with open('/etc/cron.monthly/ziem_cleardb', 'w') as f:
        f.write(job)
    os.system("chmod 700 /etc/cron.monthly/ziem_cleardb")


      

def install_service(name, desc, cmd):
    print(f'\n[*] Write {desc}\n----------------')
    service = (
        '[Unit]\n'
        f'Description={desc}\n'
        'After=network.target\n'
        '[Service]\n'
        'Type=simple\n'
        f'ExecStart={cmd}\n'
        'User=zuser\n'
        'Group=zuser\n'
        'Restart=always\n'
        'RestartSec=60\n'
        '[Install]\n'
   'WantedBy=multi-user.target\n')
    with open(f'/etc/systemd/system/{name}.service', 'w') as f:
        f.write(service)
    print(service)

    
def install_coreservice():
    venv = '/opt/ziem/venv/bin/ziem --core'    
    # '/usr/local/bin/python3 /opt/ziem/zeim --core'
    install_service('ziemcored', 
                    'ZIEM Core Service', 
                    '/usr/bin/ziem --core')
    
    
    
def install_webservice(center):
    #/usr/local/bin/python3 -m gunicorn --bind unix:/opt/ziem/ziemweb.sock "web:create_app()" --chdir /opt/ziem/src
    venv = f'/opt/ziem/venv/bin/gunicorn --bind unix:/var/opt/ziem/ziemweb.sock "ziem.web:create_app({center})"'
    install_service('ziemwebd', 
                    'ZIEM Web Service', 
                     venv)
    

    
def install_postservice():
    venv = '/opt/ziem/venv/bin/ziem --post'  
    install_service('ziempostd', 
                    'ZIEM Core Service', 
                    '/usr/bin/ziem --post')

    
    
def install_sudo():
    with open('/etc/sudoers', 'r') as f:
        lines = f.readlines()
    cmds = [
        'zuser ALL=(ALL:ALL) NOPASSWD: /bin/systemctl restart ziemcored',
        'zuser ALL=(ALL:ALL) NOPASSWD: /bin/systemctl stop ziemcored',
        'zuser ALL=(ALL:ALL) NOPASSWD: /bin/systemctl start ziemcored',
        'zuser ALL=(ALL:ALL) NOPASSWD: /bin/systemctl restart ziemwebd',
        'zuser ALL=(ALL:ALL) NOPASSWD: /bin/systemctl restart ziempostd',
      # 'zuser ALL=(ALL:ALL) NOPASSWD: /opt/ziem/venv/bin/python -m pip',
        ]
    for cmd in cmds:
        if cmd not in lines:    
            cmd_run = 'echo "' + cmd + '" >> /etc/sudoers'
            os.system(cmd_run)
           
        
        
def init_nginx(center):
    print('\n[*] Write nginx config\n----------------')
    fname = 'nginx-cc' if center else 'nginx-agent'
    os.system(f'sudo cp /opt/ziem/cfg/{fname}.conf /etc/nginx/nginx.conf')    
    print('\n[*] Delete default nginx sites\n----------------')
    os.system('rm /etc/nginx/sites-enabled/default')
    os.system('sudo systemctl restart nginx')    
    
def install_cert(fkey='/etc/ssl/private/nginx-ziem.key', fcrt='/etc/ssl/certs/nginx-ziem.crt'):
    print('\n[*] Create ssl cert\n----------------')
    os.system('openssl req -x509 -nodes -days 10950 -newkey rsa:2048 \\'\
              f'-keyout {fkey} \\'\
              f'-out {fcrt}')
    
def install_bin():
    print('\n[+] Creat ZIEM link to /usr/bin\n----------------')
    venv_path = 'source /opt/ziem/venv/bin/activate\n'
    link = ('#!/bin/bash\n' 
            + venv_path 
            + 'python -m ziem "$@"')
    with open('/usr/bin/ziem', 'w') as f:
        f.write(link)
    os.system("chmod +x /usr/bin/ziem")
    print(link)
