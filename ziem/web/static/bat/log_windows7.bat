@echo off

rem Проверка прав
net session >nul 2>&1
    if %errorLevel% == 0 (
        echo [*] Добавление пользователя
        net user /add ziem_user *
        net localgroup "Пользователи DCOM" ziem_user /add
        net localgroup "Пользователи журналов производительности" ziem_user /add
        net localgroup "Читатели журнала событий" ziem_user /add

        echo [*] Настройка Брандмауера
        netsh advfirewall firewall add rule ^
            name="ZIEM-RPC-135" dir=in action=allow ^
            protocol=TCP localport=135 ^
            program="%SystemRoot%\system32\svchost.exe" enable=yes
        netsh advfirewall firewall add rule ^
            name="ZIEM-RPC-dynamic" dir=in action=allow ^
            protocol=TCP localport=RPC ^
            program="%SystemRoot%\system32\svchost.exe" enable=yes

        echo [*] Настройка аудита
        del C:\Windows\security\audit\audit.csv
        del C:\Windows\System32\GroupPolicy\Machine\Microsoft\WindowsNT\Audit\audit.csv
        del C:\Windows\System32\GroupPolicy\gpt.ini
        gpupdate /force

        echo Вход учетной записи
        auditpol /set /subcategory:"Другие события входа учетных записей" /success:enable
        auditpol /set /subcategory:"Проверка учетных данных" /success:enable

        echo Учетные записи
        auditpol /set /subcategory:"Управление учетными записями" /success:enable
        auditpol /set /subcategory:"Управление группой безопасности" /success:enable

        echo Подробное отслеживание
        auditpol /set /subcategory:"Создание процесса" /success:enable

        echo Вход/выход
        auditpol /set /subcategory:"Вход в систему" /success:enable /failure:enable
        auditpol /set /subcategory:"Другие события входа и выхода" /success:enable /failure:enable
        auditpol /set /subcategory:"Специальный вход" /success:enable
        auditpol /set /subcategory:"Выход из системы" /success:enable

        echo Доступ к объектам
        auditpol /set /subcategory:"Файловая система" /success:enable
        auditpol /set /subcategory:"Другие события доступа к объекту" /success:enable
        auditpol /set /subcategory:"Файловый ресурс общего доступа" /success:enable
        auditpol /set /subcategory:"Объект-задание" /success:enable

        echo Изменение политики
        auditpol /set /subcategory:"Аудит изменения политики" /success:enable
        auditpol /set /subcategory:"Изменение политики проверки подлинности" /success:enable
        auditpol /set /subcategory:"Изменение политики правила уровня MPSSVC" /success:enable

        echo Система
        auditpol /set /subcategory:"Изменение состояния безопасности" /success:enable
        auditpol /set /subcategory:"Другие системные события" /success:enable

    ) else (
        echo [-] Ошибка: запустите скрипт с правами администратора
    )
    pause >nul
