import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

for req in required:
    print(f'{req}:')
    os.system('sudo python3.9 -m pip download --no-deps -d dist ' + req)
