import os
import time
import random
import string
import asyncio
from cryptography.fernet import Fernet

def init(bks=False):
    init_crypto()
    install_sudo()
    install_agentservice('bks' if bks else 'run')
    with open('/var/log/ziem/agent.k', 'w') as f:
        f.write('')
    os.system('sudo chown zuser:zuser /var/log/ziem/agent.k')

    # Логи
    logs = ['agent1', 'bks1']
    for log in logs:
        flog = f'/var/log/ziem/{log}.log'
        if not os.path.isfile(flog):
            with open(flog, 'w') as f:
                f.write('')
        os.system(f'sudo chown zuser:zuser {flog}')
        
    os.system('sudo systemctl enable ziemagentd.service')
    os.system("systemctl restart ziemagentd")
    print('\n\n[+] Installation complete. Please reboot')

def init_crypto():
    print('\n[*] Creating main crypto key\n----------------')
    print('/etc/opt/ziem/agent.k')
    fern_key = Fernet.generate_key()
    with open('/etc/opt/ziem/agent.k', 'wb') as f:
        f.write(fern_key)

def install_agentservice(run='run'):
    print('\n[*] Write ZIEM Agent systemd service\n----------------')
    service = (
        '[Unit]\n'
        'Description=ZIEM Agent Service\n'
        'After=network.target\n'
        '[Service]\n'
        'Type=simple\n'
        f'ExecStart=/opt/ziem/venv/bin/ziemagent --{run}\n'
        'User=zuser\n'
        'Group=zuser\n'
        'Restart=always\n'
        'RestartSec=60\n'
        '[Install]\n'
       'WantedBy=multi-user.target\n')
    with open('/etc/systemd/system/ziemagentd.service', 'w') as f:
        f.write(service)
    print(service)

def install_sudo():
    with open('/etc/sudoers', 'r') as f:
        lines = f.readlines()
    lines = [ x for x in lines if 'ziemagent' not in x ]
    cmds = ['zuser ALL=(ALL:ALL) NOPASSWD: /bin/systemctl restart ziemagentd',
            'zuser ALL=(ALL:ALL) NOPASSWD: /opt/ziem/venv/bin/pip']
    for cmd in cmds:
        if cmd not in lines:    
            cmd_run = 'echo "' + cmd + '" >> /etc/sudoers'
            os.system(cmd_run)
