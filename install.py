
if '__main__' == __name__:
    import sys
    import os
    
    py = '/usr/local/bin/python3' if 1 == len(sys.argv) else sys.argv[1]
    exe = '/usr/bin/ziem'
    path = os.getcwd() + '/src'
    pip = f'{py} -m pip'
    
    print('\n[+] Intall  requirements\n----------------')
    #os.system(f'{pip} install --no-index --find-links dist -r requirements.txt')
    
    with open('requirements.txt') as f:
    required = f.read().splitlines()

    for req in required:
        print(f'{req}:')
        os.system(f'{pip} install {req}')
    
    print('\n[+] Creat ZIEM link to /bin\n----------------')
    with open(exe, 'w') as f:
        f.write(f'''#!/bin/bash
source {path}/env.sh        
{py} {path} "$@"
''')
    os.system(f'chmod +x {exe}')