import os
import sys

pip = 'sudo python3.9 -m pip' if 1 == len(sys.argv) else sys.argv[1] 

with open('requirements.txt') as f:
    required = f.read().splitlines()

for req in required:
    print(f'{req}:')
    os.system(f'{pip} download --no-deps -d dist ' + req)
