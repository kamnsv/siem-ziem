![logo](logo.png)

## _Простой и быстрый SIEM для АСУТП_ 
### _Руководство администратора_  

![](https://img.shields.io/badge/version-1.5-blue)
![](https://img.shields.io/badge/python-3.9-blue)
![](https://img.shields.io/badge/debian-10-blue)

## Содержание  
[Важная информация](#important_info)  
[Зависимости](#dependencies)  
[Быстрая установка](#install_fast)  
[Установка из образа](#install_vm)  
[Установка из дистрибутива](#install_whl)  
[Инициализация](#init)  
[Запуск](#run)  
[Обновление](#update)  
[Ручное создание сервисов](#services)  
[Создание дистрибутива](#build)  
[Дополнительные команды](#commands)  
[Работа с Linux](#linux)  

<a name="important_info"/>

## Важная информация  
</a>  

> Данное руководство содержит необходимую информацию по установке и настройке системы  
> Система работает под управлением ОС `Debian 10`  
> Система написана на `Python3` и работает в виртуальной среде

<a name="dependencies"/>

## Зависимости

</a>

* MongoDB
* Python3.9

Для PostgreSQL 

`sudo apt install libpq-dev`


<a name="install_fast"/>

## Быстрая установка
</a>  

```sh
cd /opt
sudo git clone [zime]
cd ziem
sudo python3.9 install.py
sudo ziem --init
sudo reboot now
```



<a name="install_vm"/>

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
sudo python3.9 -m venv /opt/ziem/venv
```
- минимальная пропусктная способность канала состовляет 64 кбит/сек  

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

## Обновление
</a>  

> Обновление производится через локальный репозиторий на `zien-dev`  
> для этого необходим отдельный сервер Debian `ziem-dev` с установленным Python3  

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

<a name="init"/>

## Инициализация системы
</a>  

> Первоначально необходимо произвести `инициализацию` и `создать сервисы` системы  
> Создается дополнительный пользователь `zuser`, от которого работает ZIEM  
> Создаются каталоги для работы ZIEM:  
> /opt/ziem - виртуальная среда + исполняемый код, `root` запись, `other` чтение   
> /etc/opt/ziem - конфигурационные файлов, `root` запись, `zuser` чтение  
> /var/opt/ziem - временные файлов, `zuser` запись  
> /var/log/ziem - логи, `zuser` запись   
 
- Инициализация системы  
```
sudo /opt/ziem/venv/bin/python -m ziem --init
```
- Создание сервисов  
```
sudo /opt/ziem/venv/bin/python -m ziem --install
```
<a name="run"/>

## Запуск
</a>

```sh
└─$ ziem
ZIEM 1.5.54 Simple and fast SIEM for ICS
Copyright (c) 2020 CPA - Transneft Upper Volga, JSC
This program comes with ABSOLUTELY NO WARRANTY
This is free software, and you are welcome to redistribute it
under certain conditions; type `--license` for details.

 ___________ ______ __  __ 
|___  /_   _|  ____|  \/  |
   / /  | | | |__  | \  / |
  / /   | | |  __| | |\/| |
 / /__ _| |_| |____| |  | |
/_____|_____|______|_|  |_|

usage: ziem [options]

optional arguments:
  -h, --help  Вызов данной справки
  -c, --core  Запуск CORE. Сбор, нормализация, корреляция событий.
  -w, --web   Запуск WEB. Работа в DEBUG режиме, только для проверки!
  --debug     DEBUG режим. Использовать для CORE.
  --init      Инициализация конфигурации системы
  --dropdb    Очистка базы CORE. Удаление всех сообщений, событий, инцидентов.
  --clearweb  Очистка базы WEB. Удаление источников и правил.
  --dropweb   Очистка базы WEB. Удаление всех настроек.
  --dropuser  Сброс пароля пользователю admin для входа в WEB.
  --version   Просмотр версии программы и дополнительной информации.
  --license   Просмотр лицензионного соглашения.
```
<a name="services"/>

## Ручное создание сервисов
</a>

- сервис ядра `ziemcored.service`
```sh
sudo nano /etc/systemd/system/ziemcored.service
```

- сервис WSGI сервера `ziemwebd.service`
```sh
sudo nano /etc/systemd/system/ziemwebd.service 
```

- сервис WEB сервера  
    - установка [nginx](https://www.nginx.com/)  
    ```sh
    sudo apt install nginx-light
    sudo rm /etc/nginx/sites-enabled/default
    ```
    - создание сертификатов
    ```sh
    sudo openssl req -x509 -nodes -days 10950 -newkey rsa:2048 \
      -keyout /etc/ssl/private/nginx-selfsigned.key \
      -out /etc/ssl/certs/nginx-selfsigned.crt
    ```
    - настройка конфигурации `nginx.conf`
    ```sh
    sudo nano /etc/nginx/nginx.conf
    ```

- включение сервисов
```sh
sudo systemctl enable nginx.service ziemcored.service ziemwebd.service
sudo reboot
```

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
    req_dir = ('dist/' + req.split('==')[0]).lower()
    os.makedirs(req_dir, exist_ok=True)
    os.system('python -m pip download --no-deps -d ' + req_dir + ' ' + req)
```

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
rsync -avzP -e 'ssh -p 44444' tuser@ziem-dev:/opt/ziem/* ~/ziem/ziem-project --delete
```

- скопировать файл по ssh
```sh
scp -P 44444 config.conf  tuser@192.168.154.15:~/
```

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
<a name="changelog"/>

## Changelog
</a>

- необходимо писать commits в формате
```sh
type(category): description

types
    feat: A new feature
    fix: A bug fix
    docs: Changes to documentation
    style: Formatting, missing semi colons, etc; no code change
    refactor: Refactoring production code
    test: Adding tests, refactoring test; no production code change
    chore: Updating build tasks, package manager configs, etc; no production code change
```

- установить автогенератор лога
```sh
pip install auto-changelog
```

- генерация chengelog.md
```sh
cd /opt/ziem
/$HOME/.local/bin/auto-changelog -u
    -u unrealesed
```