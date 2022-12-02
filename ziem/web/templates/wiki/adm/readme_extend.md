![logo](/static/images/logo.png)


## Содержание  
[Установка из образа](#install_vm)  
[Установка из дистрибутива](#install_whl)  
[Обновление через репозиторий](#update)  
[Ручное создание сервисов](#services)  
[Создание дистрибутива](#build)  
[Дополнительные команды](#commands)  
[Работа с Linux](#linux)  

<a name="install_vm">
## Установка из образа
</a>  

> Система распространяется в виде архива образа вирульной машины Hyper-V

- скачать образ виртуальной машины
- распаковать архив
- запустить `Hyper-V Manager`
- на панели `Actions` выбрать `Import Virtual Machine`
- указать папку с образом виртуальной машины
- выбрать виртуальную машину `__SHIB_ZIEM_Debian-Prod`
- указать `Copy the virtual machine (Create a new unique ID)`
- выбрать папки для хранения файлов новой виртуальной машины
- выбрать папку для хранения жесткого диска
- нажать завершить  
- после завершения импорта зайти в `Settings` виртуальной машины
- произвести настройку `Сетевых адаптеров`

<hr>
<a name="install_whl"/>

## Установка из дистрибутива
</a>  

> Установка возможно либо через `локальный файл`,   
> либо через локальный репозиторий.  
> Для этого необходим отдельный сервер Debian `ziem-dev` с установленным Python3  

### Предварительная установка  

- Настройка сетевых интерфейсов
```sh
sudo nano /etc/network/interfaces
sudo systemctl restart networking
```
- установить [MongoDB](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/)  

- установить `pip`
```sh
sudo apt install python3-pip
```
- установить `виртуальную среду` python
```sh
sudo mkdir /opt/ziem
sudo python -m venv /opt/ziem/venv
```
### Установка из локального дистрибутива
- скачать установочный файл `ziem-xxx.whl`
- запустить установку из той же папки
```sh
sudo /opt/ziem/venv/bin/python -m pip install ziem-xxx.whl
```
### Установка из репозитория  
- на `ziem-dev` клонировать `репозиторий` ziem  
- на `ziem-dev` запустить репозиторий pip  
```sh
python3 -m http.server --directory ziem/dist
```
- теперь на целевой системе установить с помощью pip
```sh
sudo /opt/ziem/venv/bin/python -m pip install \
  --trusted-host ziem-dev \
  --index-url http://ziem-dev:8000 ziem -U
```
<a name="update"/>

## Обновление через репозиторий
</a>  

> Обновление производится через локальный репозиторий на `zien-dev`  
> для этого необходим отдельный сервер Debian `ziem-dev` с установленным Python3  

- на `ziem-dev` клонировать `репозиторий` ziem  
- на `ziem-dev` запустить репозиторий pip  
```sh
python -m http.server --directory ziem/dist
```
- теперь на целевой системе установить с помощью pip
```sh
sudo /opt/ziem/venv/bin/python -m pip install \
  --trusted-host ziem-dev \
  --index-url http://ziem-dev:8000 ziem -U
```

<a name="services"/>
## Ручное создание сервисов
</a>

- сервис ядра **ziemcored**


```sh
sudo nano /etc/systemd/system/ziemcored.service
```


```sh
[Unit]
Description=ZIEM CORE Service
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/ziem --core
User=zuser
Group=zuser
Restart=always
RestartSec=60
[Install]
WantedBy=multi-user.target
```


- сервис WSGI сервера **ziemwebd**


```sh
sudo nano /etc/systemd/system/ziemwebd.service 
```


```sh
[Unit]
Description=ZIEM CORE Service
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/ziem --web
User=zuser
Group=zuser
Restart=always
RestartSec=60
[Install]
WantedBy=multi-user.target
```

- сервис отправки `ziempostd`

```sh
sudo nano /etc/systemd/system/ziempostd.service 
```

```sh
[Unit]
Description=ZIEM CORE Service
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/ziem --post
User=zuser
Group=zuser
Restart=always
RestartSec=60
[Install]
WantedBy=multi-user.target
```

- включение сервисов

```sh
sudo systemctl enable ziemcored ziemwebd ziempostd
sudo reboot now
```

<hr>
<a name="build"/>

## Создание дистрибутива
</a>

- перейти в каталог с репозиторием ziem

```sh
cd /opt/ziem
```
- активировать виртуальную среду  

```sh
source venv/bin/activate
```

- обновить файл `requirements.txt`

```sh
python -m pip freeze --exclude-editable > requirements.txt
```

- отредактировать файл `setup.py` , изменить версию  

```sh
nano setup.py
```

- создать дистрибутив, файлы сохраняются в `dist/ziem`

```sh
pip install wheel
python setup.py bdist_wheel --dist-dir=dist/ziem
rm -rf build instance
```

- обновить репозиторий

```
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

for req in required:
    rdir = ('dist/' + req.split('==')[0]).lower()
    os.makedirs(rdir, exist_ok=True)
    os.system(f'python -m pip download --no-deps -d {rdir} {req}')
```

<hr>
<a name="commands"/>
## Дополнительные команды
</a>

- активация виртуальной среды 

```sh
source /opt/ziem/venv/bin/activate
```
- работа с `pip`

```sh
pip install -e .
pip uninstall ziem
pip list
pip freeze --exclude-editable > requirements.txt
```

- работа с `git`

```sh
git clone git@xxx
git pull
git add .
git commit -m "Update code"
git push
```

- синхронизация папок
```sh
rsync -avzP -e 'ssh -p 44444' 
    tuser@ziem-dev:/opt/ziem/* ~/ziem/ziem-project --delete
```

- скопировать файл по ssh
```sh
scp -P 44444 config.conf  tuser@192.168.154.15:~/
```

<hr>
<a name="linux"/>

## Работа с Linux
</a>

- хосты
```sh
sudo nano /etc/hosts
sudo nano /etc/hosts.allow
```

- просмотр ip
```sh
ip a
```

- изменение IP адреса
```sh
sudo nano /etc/network/interfaces
```

- просмотр активных соединений
```sh
sudo ss -antp
```

- просмотр правил МСЭ
```sh
sudo iptables -L -n
```

- открыть порт
```sh
iptables -A INPUT -p tcp --dport 44444 -m state --state NEW -j ACCEPT
iptables-save > /etc/iptables.up.rules
```

- работа с сервисами
```sh
sudo systemctl restart ziemcored
sudo journalctl -u ziemcored -f
```

- обновление системы  
```sh
sudo nano /etc/apt/sources.list
sudo apt update
sudo apt upgrade
```

- сведения о жестком диске
```sh
df -h
mount
sudo nano /etc/fstab
```

- журналирование rsyslog
```sh
sudo nano /etc/rsyslog.conf
sudo nano /etc/systemd/journald.conf
sudo nano /etc/logrotate.conf
```
- аудит audit
```sh
sudo cat /etc/audit/audit.rules
sudo /etc/audit/rules.d/audit.rules
sudo nano /etc/audit/rules.d/99-finalize.rules
```

- sudo
```sh
sudo visudo
```
