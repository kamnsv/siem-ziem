![logo](/static/images/logo.png)

##  Настройка Syslog 
> Описание процесса настройки источников для отправки сообщений в ZIEM  
> Область применения:  
> -- устройства, способные отправлять логи по протоколу `Syslog`  

## Содержание  
[Описание](#menu_info)  
[Cisco](#menu_cisco)  
[Poligon](#menu_poligon)  
[Eltex](#menu_eltex)  
[Moxa](#menu_moxa)  
[Huawei](#menu_huawei)  

<a name="menu_info"/>  
## Описание  
</a>  

> Протокол Syslog представляет собой передачу сообщений без установления соединения  
> Подключение к источнику не требуется  
> Сервер Syslog на ZIEM работает на стандартном порту `UDP 514`  
> Требуется лишь указать на источнике IP адрес ZIEM

<hr class="pagebreak">

<a name="menu_cisco"/>  

## Cisco  
</a> 

- Подключиться по SSH и ввести команды  
```sh  
router#conf t  
Router(config)#logging on  
Router(config)#logging host x.x.x.x  
Router(config)#logging traps informational  
```

<a name="menu_poligon"/>  

## Poligon Inzer  
</a> 

- Подключиться по SSH и ввести команды  
```sh  
router#conf t  
Router(config)#logging on
Router(config)#logging host 1 x.x.x.x  
Router(config)#logging level informational 1
Router(config)#logging file level notice
Router(config)#logging file sd:///log.txt
```

<a name="menu_eltex"/>  

## Eltex  
</a> 

через WEB
- зайти на WEB интерфейс `https://x.x.x.x/`  
- перейти на вкладку `System / Logs / Servers`  
- добавить `IP адрес`, `port` сервера, указать `Facility Local 7`, `Severity Informational` 

через SSH
```
logging on
logging host x.x.x.x port 514
logging cli-commands
logging origin-id hostname
```
<hr class="pagebreak">

<a name="menu_moxa"/>  

## Moxa  
</a> 

- зайти на WEB интерфейс `https://x.x.x.x/`  
- перейти на вкладку `System / Warning Notification / Syslog Server Settings`  
- поставить галочку `Syslog 1` и задать `IP адрес`  
- проверить, что стоят все галки `Syslog` в поле `Action` на следующих вкладках  
-- `System Event Settings`
-- `Port Event Settings`

<a name="menu_huawei"/>  

## Huawei  
</a> 

- зайти на WEB интерфейс `https://x.x.x.x:8443/`
- перейти на вкладку `Log Configuration / Log Configuration`
- задать `IP адрес` в поле `Log Host IP Address`
- перейти на вкладку `Log Configuration / Syslog Template`
- создать `Template` со всеми включенными `Field`
