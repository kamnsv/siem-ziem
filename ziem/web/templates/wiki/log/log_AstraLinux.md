![logo](/static/images/logo.png)


> Процесс настройки аудита ОС "AstraLinux" и взаимодействия с ЗИЕМ.  
> Область применения:  
> -- устройства, способные отправлять логи по протоколу `syslog` или `rsyslog`.  
> -- операционные системы Linux с пакетами аудита: `auditd, audispd-plugins`  

## Содержание
[Описание](#menu_info)  
[Настройка Syslog](#menu_syslog)  
[Настройка Rsyslog](#menu_rsyslog)  
[Политика аудита](#menu_audit)  
[Скрипт настройки](#menu_conf)  

<a name="menu_info"/>  

## Описание  

</a>  

> Rsyslog - сервис управления логами, передача осуществляется средствами протокола Syslog.
> Протокол Syslog представляет собой передачу сообщений без установления соединения.  
> Подключение к источнику не требуется.
> Сервера Syslog и RSyslog работают протоколу *UDP* на порту `514`.  
> В настройках сервиса Syslog и RSyslog требуется указать IP адрес ЗИЕМ.
> Аудит и сервисы настроить можно при помощи скрипта. 

<hr class="pagebreak">

<a name="menu_syslog"/>  

## Настройка Syslog
</a>  

Все настройки Syslog находятся в файле конфигурации `/etc/syslog-ng/syslog-ng.conf` и в других конфигурационных файлах из `/etc/syslog-ng/conf.d` 

1\. Чтобы активировать передачу в ZIEM необходимо в конфигурационный файл добавить инструкцию:

```
destination d_ziem {
    udp("[ip_address_ziem]" port(514));
};

log {
    source(s_src); 
    destination(d_ziem);
};
```

2\. Необходимо перезапустит службу:

```
sudo systemctl restart syslog-ng
```



<a name="menu_rsyslog"/>  

## Настройка Rsyslog
</a>  

> Не во всех сборках ОС "AstraLinux" может быть предустановлена служба RSyslog.

Все настройки Rsyslog находятся в файле `/etc/rsyslog.conf` и в других конфигурационных файлах из `/etc/rsyslog.d.` 

1\. Чтобы активировать передачу в ЗИЕМ необходимо в конфигурационный файл добавить адрес получателя:

```
*.* @[ip_address_ziem]:514
```

Тем самым все указанные журналы будут отправлены в ZIEM.

2\. Необходимо перезапустит службу

```
sudo systemctl restart rsyslog
```

<hr class="pagebreak">

<a name="menu_audit"/>  

## Политика аудита  
</a>

1\. Внести изменения в конфигурационный файл `/etc/audit/auditd.conf`:

- Ограничение на размер файла протокола в  мегабайтах. 
- Действие, выполняемое при достижении размера файла максимального значения. 
- Минимум свободного пространства в мегабайтах
- При достижении объёмом свободного пространства на диске указанного минимума производится запись сообщения в SysLog

```
max_log_file 4096 
max_log_file_action rotate
space_left 256
space_left_action syslog
```

2\. Добавить правила в файл `/etc/audit/audit.rules`:

- Аудит доступа к файлам паролей и групп, а также попытки их изменения
- Отслеживать доступ к системным каталогам
- Отслеживать доступ к системному планировщику событий
- Отслеживать доступ к общим настройкам безопасности операционной системы
- Отслеживать использование механизма повышения привилегий
- Отслеживать операции выключения и перезагрузки 
- Отслеживать изменение параметров аудита

<hr class="pagebreak">

```
-w /etc/group -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/passwd -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/shadow -F auid!=4294967295 -k sysobj_access
-w /etc/login.defs -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/securetty -F auid!=4294967295 -k sysobj_access
-w /etc/sudoers  -p wa -F auid!=4294967295 -k sysobj_access
-w /boot/ -p wa -k system_obj_modification
-w /bin/ -p wa -k system_obj_modification
-w /sbin/ -p wa -k system_obj_modification
-w /usr/bin/ -p wa -k system_obj_modification
-w /usr/sbin/ -p wa -k system_obj_modification
-w /etc/cron.allow -p wa -k cron
-w /etc/cron.deny -p wa -k cron
-w /etc/cron.d/ -p wa -k cron
-w /etc/cron.daily/ -p wa -k cron
-w /etc/cron.hourly/ -p wa -k cron
-w /etc/cron.monthly/ -p wa -k cron
-w /etc/cron.weekly/ -p wa -k cron
-w /etc/crontab -p wa -k cron
-w /var/spool/cron/crontabs/ -k cron
-w /etc/hosts -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/sysctl.conf -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/ssh/sshd_config -F auid!=4294967295 -k sysobj_access
-w /etc/localtime -p wa -F auid!=4294967295 -k time-change
-a exit,always -F arch=b32 -S adjtimex -S settimeofday -S stime -S clock_settime -F uid!=ntp -F auid!=4294967295 -k time-change
-a exit,always -F arch=b64 -S adjtimex -S settimeofday -S clock_settime -F uid!=ntp -F auid!=4294967295 -k time-change
-a exit,always -F arch=b32 -S mknod -S mount -S umount -S umount2 -S ptrace -F auid!=4294967295 -k mount
-a exit,always -F arch=b64 -S mknod -S mount -S umount2 -S ptrace -F auid!=4294967295 -k mount
w /bin/su -p x -k priv_esc
-w /usr/bin/sudo -p x -k priv_esc
-w /etc/sudoers -p rw -k priv_esc
-w /sbin/shutdown -p x -k power
-w /sbin/poweroff -p x -k power
-w /sbin/reboot -p x -k power
-w /sbin/halt -p x -k power
-w /etc/audit/auditd.conf -p wa -F auid!=4294967295 -k audit_change
-w /etc/audit/audit.rules -p wa -F auid!=4294967295 -k audit_change
-w /etc/libaudit.conf -p wa -F auid!=4294967295 -k audit_change
-w /etc/audisp/plugins.d/syslog.conf -F auid!=4294967295 -k audit_change
-w /etc/audisp/audispd.conf -F auid!=4294967295 -k audit_change
-w /etc/rsyslog.conf -F auid!=4294967295 -k audit_change
-w /etc/init.d/auditd -p wa -F auid!=4294967295 -k audit_change
```

<hr class="pagebreak">

<a name="menu_conf">  

## Скрипт настройки  
</a>

> Скрип настраивает политику аудита и логирование syslog в ЗИЕМ.

[Загрузить скрипт](/static/bat/syslog-ziem.sh) автоматической настройки аудита.

- Будут внесены правки в конфигурационный файл `/etc/audit/auditd.conf`.
- Будет добавлен файл с правилами аудита `/etc/audit/rules.d/ziem.rules`.
- Будет добавлен файл с инструкцией отправки Syslog `/etc/syslog-ng/conf.d/ziem.conf`.
- Будут перезапущены службы `auditd` и `syslog-ng`.

**Запуск**

```sh
sudo chmod +x syslog-ziem.sh
sudo ./syslog-ziem.sh [ip_address_ziem]
```

> Было протестировано на: ОС "AstraLinux" 1.7.2.