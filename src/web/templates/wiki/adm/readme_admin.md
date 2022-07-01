![logo](/static/images/logo.png)

### _Руководство администратора_  

> Данное руководство содержит необходимую информацию по установке и настройке системы  

##### Содержание  

[Важная информация](#link_info)  
[Установка из образа](#link_vm)  
[Установка из дистрибутива](#link_install)  
[Инициализация](#link_init)  
[Запуск](#link_run)  
[Ручное создание сервисов](#link_services)  
[Создание дистрибутива](#link_build)  
[Дополнительные команды](#link_commands)  
[Работа с Linux](#link_linux)  

<a name="link_info"/>

## Важная информация  
</a>  

> Система работает под управлением ОС `Debian 11`  
> Система написана на `Python3` и работает в виртуальной среде [venv](https://docs.python.org/3/library/venv.html)  
> Система распространяется в виде образа `виртуальной машины`, а также в виде `дистрибутива`  

<a name="link_vm"/>

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

<a name="link_install"/>

## Установка\обновление из дистрибутива
</a>  

> Установка возможна через `файл` (необходим интернет),  
> `локальный репозиторий` и `локальный дистрибутив`  
> Обновление ничем не отличается от установки,  
> поэтому далее все что связано с установкой применимо и для обновления  

### Предварительная установка  

- Настройка сетеввых интерфейсов
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
sudo python3 -m venv /opt/ziem/venv
```

### Установка из репозитория (необходим интернет)
> Необходим только установочный файл ziem и интернет

- скачать установочный файл `ziem-xxx.whl`
- запустить установку из той же папки
```sh
sudo /opt/ziem/venv/bin/python -m pip install ziem-xxx.whl
```

### Установка из локального репозитория  
> Для этого необходим отдельный сервер Debian `ziem-dev` с установленным Python3

- на `ziem-dev` клонировать `репозиторий` ziem  
- на `ziem-dev` запустить репозиторий pip  
```sh
python3 -m http.server --directory dist
```
- теперь на целевой системе установить с помощью pip
```sh
sudo /opt/ziem/venv/bin/python -m pip install \
  --trusted-host ziem-dev \
  --index-url http://ziem-dev:8000 ziem -U
```

### Установка из локального дистрибутива
> Для этого необходим полный ахив дистрибутива со всеми зависимостями

- скачать архив дистрибутива `dist-ziem-xxx.tar.bz2`
- скопировать архив в систему
- распаковать архив
```sh
tar -xf dist-ziem-1.5.54.tar.bz2
```
- запустить установку
```sh
sudo /opt/ziem/venv/bin/python -m pip install --no-index --find-links=dist ziem -U 
```

<a name="link_init"/>

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
<a name="link_run"/>

## Запуск
</a>

```sh
└─$ ziem                                                                                                            130 ⨯
ZIEM 2.0.13

███████╗██╗███████╗███╗   ███╗
╚══███╔╝██║██╔════╝████╗ ████║
  ███╔╝ ██║█████╗  ██╔████╔██║
 ███╔╝  ██║██╔══╝  ██║╚██╔╝██║
███████╗██║███████╗██║ ╚═╝ ██║
╚══════╝╚═╝╚══════╝╚═╝     ╚═╝

usage: ziem [options]

optional arguments:
  -h, --help     Вызов данной справки
  -c, --core     Запуск CORE. Сбор, нормализация, корреляция событий.
  -w, --web      Запуск WEB. Работа в DEBUG режиме, только для проверки!
  -p, --post     Запуск POST. Отправка логов, отчет о работе ZIEM
  --confinstall  Установка конфигурации из WEB в CORE.
  --debug        DEBUG режим. Использовать для CORE.
  --install      Создание сервисов CORE, WEB-интерфейса и WEB-сервера.
  --init         Инициализация конфигурации системы
  --dropdb       Очистка базы CORE. Удаление всех сообщений, событий, инцидентов.
  --clearweb     Очистка базы WEB. Удаление источников и правил.
  --dropweb      Очистка базы WEB. Удаление всех настроек.
  --dropuser     Сброс пароля пользователю admin для входа в WEB.
  --version      Просмотр версии программы и дополнительной информации.
```
<a name="link_services"/>

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
    sudo openssl req -x509 -nodes -days 10950 -newkey rsa:2048  
      -keyout /etc/ssl/private/nginx-selfsigned.key   
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

<a name="link_build"/>

## Создание дистрибутива
</a>

> Создается установочный файл в формате whl  
> Обновляется репозиторий для устновки через http  
> Возможно создание полного дистрибутива для локальной устновки  

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

### Обновление репозитория  

- обновить пакеты в `локальном репозитории`  
```py
python
import os
with open('/opt/ziem/requirements.txt') as f:
    required = f.read().splitlines()
for req in required:
    req_dir = ('/opt/ziem/dist/' + req.split('==')[0]).lower()
    os.makedirs(req_dir, exist_ok=True)
    os.system('python -m pip download --no-deps -d ' + req_dir + ' ' + req)
exit()
```

### Обновление дистрибитва  

- обновить пакеты дистрибутива в папке `dist_local`  
```sh
python -m pip wheel --wheel-dir=dist_local ziem-XX.XX.XX-py3-none-any.whl
```

<a name="link_commands"/>

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

<a name="link_linux"/>

## Работа с Linux
</a>

- работа с `nano`
```sh
Ctrl+O сохранить
Ctrl+X выход
  
Alt+A  выделить текст 
Alt+6  копировать
Ctrl+K вырезать
Ctrl+U вставить
Ctrl+6 отмена выделения
Ctrl+K вырезать строку

Alt+U  отмена 
Alt+E  повтор 

Ctrl+W поиск
Alt+W  поиск далее
Ctrl+\ заменить

Ctrl+H Delete
Ctrl+D Backspace

Ctrl+B/F     вперед/назад
Ctrl+P/N     вверх/вниз
Ctrl+UP/Down переход между блоками
Ctrl+Y/V     PgUp/PgDn
Ctrl+A/E     начало/конец строки
Alt+G        перейти на строку
Ctrl+C       информации о курсоре
Alt+3        комментировать строку

```
- сведения о жестком диске
```sh
df -h
mount
sudo nano /etc/fstab
```

- сведения о загрузке системы
```sh
top
vmstat -n 5
```

- хосты
```sh
sudo nano /etc/hosts
sudo nano /etc/hosts.allow
sudo nano /etc/hosts.deny
```

- просмотр ip
```sh
ip a
```

- изменение IP адреса
```sh
sudo nano /etc/network/interfaces

auto eth0
iface eth0 inet static
  address 192.168.154.15
  post-up ip route add 192.168.233.0/24 via 172.30.1.6 dev eth0
  #gateway 192.168.154.254
  #nameserver 8.8.8.8
```

- DNS
```sh
sudo nano /resolv.conf
```

- просмотр активных соединений
```sh
sudo ss -antp
sudo ss -anup
```

- просмотр правил МСЭ
```sh
sudo iptables -L -n
```

- открыть порт
```sh
iptables -A INPUT -p tcp --dport 44444 -m state --state NEW -j ACCEPT
iptables -A INPUT -p udp --dport 44444 -m state --state NEW -j ACCEPT
iptables -A INPUT -p icmp -m state --state NEW,ESTABLISHED -j ACCEPT
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
