![logo](/static/images/logo.png)

##  Настройка FTP 
> Описание процесса настройки источников для отправки сообщений в ZIEM  
Область применения:  
-- устройства, способные отправлять логи по протоколу `FTP`  

##### Содержание  
[Описание](#info)  
[Prosoft](#prosoft)  

<a name="info"/>  

## Описание  
</a>  

> Протокол FTP представляет собой передачу сообщений через `файлы`  
> Требуется подключение к источнику   
> Настраиваются `учетные записи` FTP для подключения к источнику  
> Указывается `IP адрес` и `порт` источника, а также `журналы`  
> **Протокол FTP используется в крайних случаях!**  

<a name="prosoft"/>  

## Prosoft Regul  
</a>  

- Подключиться через `Epsilon` к ПЛК  
- Добавить в `runtime.cfg`
```
[PlcServices]
EnableFTP=1
```
- Настроить `пользователя` для подключения  
- Добавить `маршрут` в файл `/etc/routes`   

```
# Route to Ziem OSN
-net 172.30.1.5 -netmask 255.255.255.255 <IP основного коммутатора ВУ>
# Route to Ziem REZ
-net 172.30.2.5 -netmask 255.255.255.255 <IP резервного коммутатора ВУ>
```

- Добавить исключение для FTP, OPCUA в файл `/etc/pf.conf`

```
# FTP Whitelist filtering example
table <ftp_ziem> const {172.30.1.5, 172.30.2.5}
block in quick proto tcp from !<ftp_ziem> to any port 21
```