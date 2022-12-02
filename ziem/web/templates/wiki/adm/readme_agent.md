![logo](/static/images/logo.png)

# Инструкция по настройки централизованного управления 3IEM

## Порядок действий на ВМ 
[3IEM CC (ОСТ)](#vm_ziemcc)  
[Sender (сервер ДМЗ)](#vm_sender)  
[3IEM (сервер ИБ)](#vm_ziem)  


<a name="vm_ziemcc">
##  3IEM CC
</a>

*В WEB-интерфейсе:*

1. Добавьте в объектах агент 3IEM. 
2. Введите уникальное название на латинице, например `3IEM_XXX`.
3. Введите описание на русском языке.
4. Введите IP-адрес АПКШ площадки.
5. Введите и **запомните** временный пароль для "рукопожатия" систем.

> При повторном сохранении формы пароль сбрасывается (нужно вводить снова).

<hr class="pagebreak">

<a name="vm_sender">
    
## Sender (сервер ДМЗ)
    
</a>

### Nginx

* Добавьте конфигурацию прокси-сервера в директории `nginx`:

`/etc/nginx/sites-available/ziemcc.conf`

```
server {
	listen              	46000 ssl;
	server_name         	ziemcc;
	ssl_certificate 		/etc/ssl/certs/nginx-selfsigned.crt;
	ssl_certificate_key 	/etc/ssl/private/nginx-selfsigned.key;
	location / {
		proxy_pass 			https://[IP_ADDR_ZIEM_CC]:46000/;
		proxy_set_header 	Upgrade	$http_upgrade;
		proxy_set_header 	Connection keep-alive;
		proxy_set_header 	Host $host;
		proxy_set_header 	X-Forwarded-For	$proxy_add_x_forwarded_for;
		proxy_set_header 	X-Forwarded-Proto $scheme;
		proxy_http_version	1.1;
		proxy_cache_bypass	$http_upgrade;
	}
}
```

> IP_ADDR_ZIEM_CC - адрес виртуальной машины централизованной системы управления 3IEM в ККС.


* Создайте символическую ссылку на конфигурацию:

```
sudo ln -s /etc/nginx/sites-available/ziemcc.conf /etc/nginx/sites-enabled/ziemcc
```

* Перезапустите службу `sudo systemctl restart nginx`

### Network

* Добавьте маршруты:

`/etc/network/interfaces`

```
auto eth1
iface eth1 inet static
    address 10.254.1.25/30
    netmask 255.255.255.0
    post-up ip rout add 10.0.0.0/8 via 10.254.1.26
```

> На объектах, где не используется NAT IP-адреса могут отличаться.

<hr class="pagebreak">

### Hosts

* Добавьте разрешение на доступ к внутренним ресурсам:

`/etc/hosts.allow`

```
ALL: 172.31.254.0/24
```

### IPTABLES

* Добавьте разрешение на входящие соединения:

`/etc/iptables.up.rules`

```
-A INPUT -p tcp -m tcp --dport 46000 -m state --state NEW -j ACCEPT
```

**Перезапустите виртуальную машину Sender `sudo reboot`.**

<a name="vm_ziem">
## 3IEM (сервер ИБ)
</a>

1\. В WEB-интерфейсе 3IEM `Настройки -> Экспорт/Импорт` сохраните текущую конфигурацию в файл для резерва.

2\. Перейдите в директорию 3IEM `cd /opt/ziem`. 

3\. Создайте резервную копию текущeй версии 3IEM:

`sudo cp -r venv venv_reserv`

4\. Создайте новую виртуальную среду:

`sudo python3 -m venv venv`

5\. Добавьте конфигурацию для инсталлятора python:

`sh
sudo nano venv/pip.conf
`

```
[global]
trusted-host=172.29.1.25
index-url=https://172.29.1.25:46000/pypirepo
no-cache-dir=false
```

> Здесь IP-адрес сендера и должен быть на всех ДМЗ ТСПД 2.0 одинаковым *172.29.1.25*

5\. Установите 3IEM и компоненты:

`sudo /opt/ziem/venv/bin/pip install ziem ziemagent gunicorn`

<hr class="pagebreak">

6\. Выполнить инициализацию агента:

`sudo /opt/ziem/venv/bin/ziemagent --init`

7\. Введите параметры подключения:

`sudo /opt/ziem/venv/bin/ziemagent --set`

- Название 3IEM как в 3IEM CC.
- IP адрес 3IEM CC (в нашем случае SENDERa 172.29.1.25)

8\. Произведите подключение к 3IEM CC

`sudo /opt/ziem/venv/bin/ziemagent --con`

> Введите введённый ранее в 3IEM CC **временный пароль**.

9\. Проверьте конфигурацию (там должен быть токен)

`sudo /opt/ziem/venv/bin/ziemagent --show`

```
Current ziemagent config
{
    "name": "ZIEM_XXX",
    "ziemcc_ip": "xxx.xxx.xxx.xxx",
    "obj_id": "qwertyuiop",
    "token": "qwertyuiopASDFGHJKLZZXCVBNM"
}
```

> Поля **token**, **obj_id** должны быть не пустыми. 

10\. Перезапустите виртуальную машину ZIEM `sudo reboot`.

