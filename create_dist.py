import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

for req in required:
    req_dir = ('dist/' + req.split('==')[0]).lower()
    os.makedirs(req_dir, exist_ok=True)
    if len(os.listdir(req_dir)) == 0:
        os.system('python3 -m pip download --no-deps -d ' + req_dir + ' ' + req)
        print(req_dir)