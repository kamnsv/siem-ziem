![logo](/static/images/logo.png)

##  Настройка логера OPC UA 
> Описание процесса настройки источников для отправки сообщений в ZIEM  
Область применения:  
-- устройства, способные отправлять логи по протоколу `OPC UA`  

## Содержание  
[Описание](#info)  
[Настройка](#config)  
[Prosoft Regul](#prosoft)  

<a name="info"/>  

## Описание  
</a>  

> Протокол OPC UA представляет собой передачу сообщений `по подписке`  
> Требуется создать подписку к источнику   
> Настраиваются `учетные записи` для подключения к источнику  
> Указывается `IP адрес` и `порт` источника, а также `журналы`  

<a name="config"/>  

## Настройка  
</a>  

- Настроить клиента  
- Добавить клиента в ZIEM  


<a name="prosoft"/>  

## Prosoft Regul  
</a>  

- Подключиться через `Epsilon` к ПЛК  
- Добавить `маршрут` в файл `/etc/routes` 

```
# Route to Ziem OSN
-net 172.30.1.5 -netmask 255.255.255.255 <IP основного коммутатора ВУ>
# Route to Ziem REZ
-net 172.30.2.5 -netmask 255.255.255.255 <IP резервного коммутатора ВУ>
```

- Добавить исключение для OPCUA в файл `/etc/pf.conf`

```
# OPCUA Whitelist filtering example
table <opcua_ziem> const {172.30.1.5, 172.30.2.5}
block in quick proto tcp from !<opcua_ziem> to any port 48010
```   