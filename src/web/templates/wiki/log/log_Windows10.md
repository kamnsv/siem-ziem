![logo](/static/images/logo.png)

##  Настройка ОС Windows 
> Описание процесса настройки ОС Windows для отправки сообщений в ZIEM  
> Область применения:  
> -- Windows 10  
> -- Windows Server 2016, 2019  

## Содержание  
[Описание](#menu_info)  
[Настройка Пользователя](#menu_user)  
[Настройка WMI](#menu_wmi)  
[Настройка DCOM](#menu_dcom)  
[Настройка Брандмауера](#menu_fw)  
[Настройка Политики аудита](#menu_audit)  
[Настройка Сети](#menu_net)  
[Скрипт настройки](#menu_script)  

<hr class="pagebreak">

<a name="menu_info"/>  

## Описание  
</a>  

> Получения журналов Windows происходит при помощи WMI  
> WMI в свою очередь использует протокол DCOM  
> На источнике необходимо создать `пользователя` для подключения  
> Предоставить ему `права` и настроить `Брандмауэр`  
> Также для генерации сообщений необходимо настроить `аудит`
> Необходимо перезагрузить АРМ в конце настройки  


<a name="menu_user"/>  

## Настройка Пользователя  

</a>  

- Создаeм пользователя (при использовании скрипта делать не надо)   
```cmd
net user /add ziem_user *
```
- Добавляем группы пользователю (при использовании скрипта делать не надо)  
```cmd
net localgroup "Пользователи DCOM" ziem_user /add
net localgroup "Пользователи журналов производительности" ziem_user /add
net localgroup "Читатели журнала событий" ziem_user /add
```
- Делаем учетную запись технологической, без интерактивного входа  
-- запускаем `secpol.msc`  
-- выбираем `Локальные политики / Назначение прав пользователя`  
-- добавляем `ziem_user` в следующие списки  
*Запретить локальный вход*  
*Запретить вход в систему через службу удаленных рабочих столов*  
*Вход в качестве службы*  
*Доступ к компьютеру из сети*  

<hr class="pagebreak">

<a name="menu_dcom"/>  

## Настройка DCOM  
</a>  

- Запускаем `dcomcnfg`  
- Правый-щелчок `Службы компонентов \ Компьютеры \ Мой компьютер \ Настройка DCOM \ Windows Management and Instrumentation`, выбираем `свойства`   
- Выбираем вкладку `Безопасность`  
- В поле `Разрешения на запуск` нажимаем `Настроить \ Изменить`  
- Добавляем пользователя `ziem_user` c `разрешениями`  
-- *Удаленный запуск, Удаленная активация*  
- В поле `Разрешение на доступ` нажимаем `Настроить \ Изменить`  
- Добавляем пользователя `ziem_user` c `разрешениями`  
-- *Удаленный доступ*  

<a name="menu_wmi"/>  

## Настройка WMI  
</a>  

- Запускаем `wmimgmt.msc`  
- Правый-щелчок `Элемент управления WMI`, выбираем `свойства`  
- Вкладка `Безопасность`  
- Выбираем `CIMV2`, нажимаем `Безопасность`  
- Нажимаем `добавить`  
- Добавляем пользователя `ziem_user` c `разрешениями`  
-- *Выполнение методов, Включить учетную запись, Включить удаленно, Прочесть безопасность*  

<hr class="pagebreak">

<a name="menu_fw"/>  

## Настройка Брандмауера  
</a>  

- Добавляем правила для WMI (при использовании скрипта делать не надо)
```cmd
netsh advfirewall firewall add rule ^
    name="ZIEM-RPC-135" dir=in action=allow ^
    protocol=TCP localport=135 ^
    program="%SystemRoot%\system32\svchost.exe" enable=yes
netsh advfirewall firewall add rule ^
    name="ZIEM-RPC-dynamic" dir=in action=allow ^
    protocol=TCP localport=RPC ^
    program="%SystemRoot%\system32\svchost.exe" enable=yes
```

<a name="menu_audit"/>  

## Настройка политики аудита  
</a>  

- Настройка осуществляется через `audipol` (при использовании скрипта делать не надо)  
```
del C:\Windows\security\audit\audit.csv
del C:\Windows\System32\GroupPolicy\Machine\Microsoft\WindowsNT\Audit\audit.csv
del C:\Windows\System32\GroupPolicy\gpt.ini

rem Вход учетной записи 
auditpol /set /subcategory:"Другие события входа учетных записей" /success:enable
auditpol /set /subcategory:"Проверка учетных данных" /success:enable

rem Управление учетными записями
auditpol /set /subcategory:"Управление учетными записями" /success:enable /failure:enable
auditpol /set /subcategory:"Управление группой безопасности" /success:enable /failure:enable

rem Подробное отслеживание
auditpol /set /subcategory:"Создание процесса" /success:enable
auditpol /set /subcategory:"Самонастраиваемые события" /success:enable

rem Вход/выход
auditpol /set /subcategory:"Вход в систему" /success:enable /failure:enable
auditpol /set /subcategory:"Другие события входа и выхода" /success:enable /failure:enable
auditpol /set /subcategory:"Специальный вход" /success:enable
auditpol /set /subcategory:"Выход из системы" /success:enable

rem Доступ к объектам
auditpol /set /subcategory:"Файловая система" /success:enable
auditpol /set /subcategory:"Другие события доступа к объекту" /success:enable
auditpol /set /subcategory:"Общий файловый ресурс" /success:enable
auditpol /set /subcategory:"Объект-задание" /success:enable

rem Изменение политики
auditpol /set /subcategory:"Аудит изменения политики" /success:enable
auditpol /set /subcategory:"Изменение политики правила уровня MPSSVC" /success:enable
auditpol /set /subcategory:"Изменение политики проверки подлинности" /success:enable

rem Система
auditpol /set /subcategory:"Изменение состояния безопасности" /success:enable
auditpol /set /subcategory:"Другие системные события" /success:enable
```

- Проверить применение настроек политики
```
auditpol /get /category:*
```

<a name="menu_net"/>  

## Настройка сети  
</a>  

- При необходимости создать `маршруты` для доступа к ZIEM


<a name="menu_script"/>  

## Скрипт настойки  
</a>  

- Необходимо скачать [файл](/static/bat/log_windows10.bat) и запустить с правами администратора  


