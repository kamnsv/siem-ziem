#!/bin/bash
rm -rf `find -type d -name .ipynb_checkpoints`
rm -rf `find -type d -name __python__`
python3 setup-ziem.py bdist_wheel --dist-dir=dist/ziem
python3 setup-agent.py bdist_wheel --dist-dir=dist/ziemagent
systemctl restart ziemwebd
rm -rf build