```json
[
    {
        "name": "ARM_MSWindows-7",
        "desc": "Windows 7+, Windows Server 2008+",
        "profile": "MSWindows",
        "tax_main": "arm",
        "logs": [],
        "events": [
            {
                "string": "4688",
                "alr_msg": "Запуск процесса",
                "tax_object": "app",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "5",
                        "field": "process"
                    },
                    {
                        "value": "1",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "4625",
                "alr_msg": "Неуспешный вход пользователя",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "10",
                        "field": "privilege"
                    },
                    {
                        "value": "5",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "4624",
                "alr_msg": "Успешный вход пользователя",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "8",
                        "field": "privilege"
                    },
                    {
                        "value": "5",
                        "field": "user"
                    },
                    {
                        "value": "18",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "1074",
                "alr_msg": "Перезагрузка системы",
                "tax_object": "os",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "10",
                        "field": "privilege"
                    },
                    {
                        "value": "5",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "4672",
                "alr_msg": "Вход с правами администратора",
                "tax_object": "user",
                "tax_action": "login.adm",
                "regex": [
                    {
                        "value": "4",
                        "field": "privilege"
                    },
                    {
                        "value": "1",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "4720",
                "alr_msg": "Создана новая учетная запись",
                "tax_object": "user",
                "tax_action": "add",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "4738",
                "alr_msg": "Изменена учетная запись",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "4724",
                "alr_msg": "Сброс пароля пользователю",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "4",
                        "field": "user"
                    },
                    {
                        "value": "0",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "4732",
                "alr_msg": "Добавлена группа безопасности пользователю",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "6",
                        "field": "user"
                    },
                    {
                        "value": "2",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "4659",
                "alr_msg": "Удален файл",
                "tax_object": "file",
                "tax_action": "del",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    },
                    {
                        "value": "8",
                        "field": "file"
                    }
                ]
            },
            {
                "string": "5140",
                "alr_msg": "Доступ к сетевой папке",
                "tax_object": "file",
                "tax_action": "access.net",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    },
                    {
                        "value": "5",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "5145",
                "alr_msg": "Доступ к сетевой папке",
                "tax_object": "file",
                "tax_action": "access.net",
                "regex": []
            },
            {
                "string": "4698",
                "alr_msg": "Создание нового задания планировщика",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "20221",
                "alr_msg": "Запуск VPN подключения",
                "tax_object": "port",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    },
                    {
                        "value": "4",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "1102",
                "alr_msg": "Очистка журнала системы",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "4697",
                "alr_msg": "Установлена новая служба в системе",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "6416",
                "alr_msg": "Подключено USB устройство",
                "tax_object": "hw",
                "tax_action": "add",
                "regex": []
            },
            {
                "string": "4726",
                "alr_msg": "Удалена учетная запись",
                "tax_object": "user",
                "tax_action": "del",
                "regex": []
            },
            {
                "string": "4950",
                "alr_msg": "Изменение состояния МСЭ",
                "tax_object": "fw",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "0",
                        "field": "interface"
                    },
                    {
                        "value": "2",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "4947",
                "alr_msg": "Изменение правила МСЭ",
                "tax_object": "fw",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "2",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "4948",
                "alr_msg": "Удалено правило МСЭ",
                "tax_object": "fw",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "2",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "4946",
                "alr_msg": "Добавлено правило МСЭ",
                "tax_object": "fw",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "2",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "4704",
                "alr_msg": "Добавлены права пользователю",
                "tax_object": "user",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "4719",
                "alr_msg": "Изменена политика аудита",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "104",
                "alr_msg": "Произошла очистка журнала",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "20005",
                "alr_msg": "Подключено запрещенное устройство",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "0",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "865",
                "alr_msg": "Запуск запрещенного ПО",
                "tax_object": "app",
                "tax_action": "drop",
                "regex": [
                    {
                        "value": "0",
                        "field": "process"
                    }
                ]
            },
            {
                "string": "4634",
                "alr_msg": "Выход пользователя",
                "tax_object": "user",
                "tax_action": "logout",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    },
                    {
                        "value": "4",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "1502",
                "alr_msg": "Изменение групповой политики",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "4670",
                "alr_msg": "Изменение прав доступа к объекту",
                "tax_object": "file",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    },
                    {
                        "value": "6",
                        "field": "file"
                    }
                ]
            },
            {
                "string": "4616",
                "alr_msg": "Измененено системное время",
                "tax_object": "time",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    },
                    {
                        "value": "7",
                        "field": "process"
                    }
                ]
            },
            {
                "string": "7045",
                "alr_msg": "Установлена новая служба",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "0",
                        "field": "process"
                    },
                    {
                        "value": "1",
                        "field": "file"
                    }
                ]
            },
            {
                "string": "20003",
                "alr_msg": "Установлено новое устройство",
                "tax_object": "hw",
                "tax_action": "add",
                "regex": [
                    {
                        "value": "2",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "20006",
                "alr_msg": "Подключено запрещенное сетевое устройство",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "2013",
                "alr_msg": "Жесткий диск заполнен",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": [
                    {
                        "value": "1",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "41",
                "alr_msg": "Нештатное завершение работы системы",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "11707",
                "alr_msg": "Установка нового ПО",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "-1",
                "alr_msg": "Ошибка подключения к системе",
                "tax_object": "port",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "20222",
                "alr_msg": "Подключение к VPN",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    },
                    {
                        "value": "3",
                        "field": "reason"
                    }
                ]
            }
        ]
    },
    {
        "name": "ASO_CiscoASA-9",
        "desc": "Cisco ASA v.9",
        "profile": "CiscoASA",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "411003",
                "alr_msg": "Административное включение порта",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "Interface %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "611102",
                "alr_msg": "Неуспешная аутентификация",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "Uname: %s",
                        "field": "user"
                    },
                    {
                        "value": "address: %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "611101",
                "alr_msg": "Успешная аутентификация",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "IP address: %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "IP address: %s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "502103",
                "alr_msg": "Вход в привилегированный режим",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "Uname: %s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "111010",
                "alr_msg": "Выполнена команда",
                "tax_object": "app",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "User %s",
                        "field": "user"
                    },
                    {
                        "value": "executed %s",
                        "field": "process"
                    },
                    {
                        "value": "from IP %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "running %s",
                        "field": "protocol"
                    }
                ]
            },
            {
                "string": "111001",
                "alr_msg": "Изменение конфигурации",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "Begin configuration:",
                        "field": "src_ip"
                    },
                    {
                        "value": "writing to %s",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "502101",
                "alr_msg": "Создана новая учетная запись",
                "tax_object": "user",
                "tax_action": "add",
                "regex": [
                    {
                        "value": "Uname: %s",
                        "field": "user"
                    },
                    {
                        "value": "Priv: %s",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "502103",
                "alr_msg": "Повышение привилегий",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "Uname: %s",
                        "field": "user"
                    },
                    {
                        "value": "To: %s",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "411001",
                "alr_msg": "Физичечкое поднятие порта",
                "tax_object": "port",
                "tax_action": "on",
                "regex": []
            },
            {
                "string": "106023",
                "alr_msg": "Срабатывание запрещающего правила МСЭ",
                "tax_object": "fw",
                "tax_action": "drop",
                "regex": [
                    {
                        "value": "src %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "by access-group %s",
                        "field": "reason"
                    },
                    {
                        "value": "dst %s",
                        "field": "dst_ip"
                    }
                ]
            },
            {
                "string": "104003",
                "alr_msg": "Сбой работы",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "106100",
                "alr_msg": "Срабатывание запрещающего правила МСЭ",
                "tax_object": "fw",
                "tax_action": "drop",
                "regex": [
                    {
                        "value": "access-list %s",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "199001",
                "alr_msg": "Перезагрузка АСО",
                "tax_object": "os",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "111111",
                "alr_msg": "Сбой работы",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "76900",
                "alr_msg": "Загрузка нового встроенного ПО",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "735002",
                "alr_msg": "Сбой работы вентилятора",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "735004",
                "alr_msg": "Сбой работы блока питания",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "735007",
                "alr_msg": "Критическая температура CPU",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "106016",
                "alr_msg": "Блокировка IP",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "to %s",
                        "field": "dst_ip"
                    },
                    {
                        "value": "on interface %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "308004",
                "alr_msg": "Установлен enable password",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "user %s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "11003",
                "alr_msg": "Очистка конфигурации",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "%s Erase",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "322001",
                "alr_msg": "Блокировка MAC",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "address %s",
                        "field": "mac"
                    }
                ]
            }
        ]
    },
    {
        "name": "ASO_PoligonInzer-1.10",
        "desc": "Poligon Inzer 2240, 2208GE v.1.10",
        "profile": "Syslog",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "SYS-BOOTING",
                "alr_msg": "Произошла перезагрузка АСО",
                "tax_object": "os",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "made a %s",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "SYS-5-CONFIG_SAVE",
                "alr_msg": "Изменение конфигурации АСО",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "using %s",
                        "field": "protocol"
                    },
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "GigabitEthernet %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "HTTP",
                "alr_msg": "Использование запрещённого сервиса на АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "TELNET",
                "alr_msg": "Использование запрещённого сервиса на АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "LINK-UPDOWN: Interface Vlan",
                "alr_msg": "Состояние Vlan изменилось в АСО",
                "tax_object": "port",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "LOOP_PROTECTION-UPDOWN",
                "alr_msg": "Состояние порта АСО изменилось на Активен",
                "tax_object": "port",
                "tax_action": "on",
                "regex": []
            },
            {
                "string": "AAA-6-SUCCESS",
                "alr_msg": "Успешная аутентификация в АСО",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "successful for \\\"%s",
                        "field": "user"
                    },
                    {
                        "value": "with privilege %s",
                        "field": "privilege"
                    },
                    {
                        "value": "by address %s",
                        "field": "mac"
                    },
                    {
                        "value": "using %s",
                        "field": "protocol"
                    },
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "AAA-5-FAILURE",
                "alr_msg": "Неуспешная аутентификация в АСО",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "successful for \\\"%s",
                        "field": "user"
                    },
                    {
                        "value": "with privilege %s",
                        "field": "privilege"
                    },
                    {
                        "value": "by address %s",
                        "field": "mac"
                    },
                    {
                        "value": "using %s",
                        "field": "protocol"
                    },
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "ACCESS_MGMT-ACCESS_DENIED",
                "alr_msg": "Подключение с незарегистрированного IP в АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "filter reject %s",
                        "field": "protocol"
                    },
                    {
                        "value": "IP address %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "SYS-FIRMWARE: New firmware",
                "alr_msg": "Загрузка нового встроенного ПО в АСО",
                "tax_object": "os",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "active: %s",
                        "field": "version"
                    }
                ]
            },
            {
                "string": "ALARM-TEMP",
                "alr_msg": "Высокая температура АСО",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "state to up.",
                "alr_msg": "Физичечкое поднятие порта АСО",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "Interface %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "state to administratively up.",
                "alr_msg": "Административное включение порта АСО",
                "tax_object": "port",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "Interface %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "PORT_SEC-2-VIOLATION",
                "alr_msg": "Подключения незарегистрированного MAC в АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "by address %s",
                        "field": "mac"
                    }
                ]
            }
        ]
    },
    {
        "name": "ASO_CiscoIOS-15",
        "desc": "Cisco IOS v.15",
        "profile": "Syslog",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "SEC_LOGIN-5-LOGIN_SUCCESS",
                "alr_msg": "Успешная аутентификация",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "user: %s",
                        "field": "user"
                    },
                    {
                        "value": "Source: %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "SEC_LOGIN-4",
                "alr_msg": "Неуспешная аутентификация",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "user: %s",
                        "field": "user"
                    },
                    {
                        "value": "Source: %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "administratively up",
                "alr_msg": "Административное включение порта",
                "tax_object": "port",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "changed state to up",
                "alr_msg": "Физичечкое поднятие порта",
                "tax_object": "port",
                "tax_action": "on",
                "regex": []
            },
            {
                "string": "SYS-5-RESTART",
                "alr_msg": "Перезагрузка АСО",
                "tax_object": "os",
                "tax_action": "start",
                "regex": []
            },
            {
                "string": "SYS-6-CLOCKUPDATE",
                "alr_msg": "Изменение времени",
                "tax_object": "time",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "SYS-5-LOGGING_STOP",
                "alr_msg": "Выключение логгирования",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "HARDWARE-2-FAN_ERROR",
                "alr_msg": "Сбой работы вентилятора",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "HARDWARE-2-THERMAL_WARNING",
                "alr_msg": "Критическая температура",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "STORM_CONTROL-3-FILTERED",
                "alr_msg": "Обнаружен шторм пакетов",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "Configured from",
                "alr_msg": "Изменение конфигурации",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "Privilege level set to",
                "alr_msg": "Повышение привилегий",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": []
            },
            {
                "string": "WARMUPGRADE-3",
                "alr_msg": "Загрузка нового встроенного ПО",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "PORT_SECURITY-2-PSECURE_VIOLATION",
                "alr_msg": "Блокировка MAC",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "PORT_SECURITY-2-INELIGIBLE",
                "alr_msg": "Ошибка работы Port Security",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "address %s",
                        "field": "mac"
                    }
                ]
            }
        ]
    },
    {
        "name": "ARM_FSControl-1.0",
        "desc": "FSControl v.1.0",
        "profile": "MSWindows",
        "tax_main": "arm",
        "logs": [],
        "events": [
            {
                "string": "1",
                "alr_msg": "Нарушение КЦ файл изменен",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "2",
                "alr_msg": "Нарушение КЦ файл создан",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "3",
                "alr_msg": "Нарушение КЦ файл удален",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "4",
                "alr_msg": "Нарушение КЦ файл переименован",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "0",
                        "field": "file"
                    }
                ]
            },
            {
                "string": "5",
                "alr_msg": "Запущена проверка КЦ",
                "tax_object": "fsctrl",
                "tax_action": "start",
                "regex": []
            },
            {
                "string": "6",
                "alr_msg": "Запущена фиксация эталонных значений КЦ",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "7",
                "alr_msg": "Изменение контрольной суммы проекта ПЛК",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "8",
                "alr_msg": "Фиксация контрольной суммы проекта ПЛК",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "9",
                "alr_msg": "Событие КЦ",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "regex": []
            }
        ]
    },
    {
        "name": "ARM_KasperskyKES-11",
        "desc": "KES v.11",
        "profile": "MSWindows",
        "tax_main": "arm",
        "logs": [],
        "events": [
            {
                "string": "218",
                "alr_msg": "Настройки антивируса изменены",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "4",
                        "field": "user"
                    },
                    {
                        "value": "5",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "236",
                "alr_msg": "Антивирус отключен",
                "tax_object": "avz",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "3",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "209",
                "alr_msg": "Автозапуск антивируса отключен",
                "tax_object": "avz",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "3",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "207",
                "alr_msg": "Базы сильно устарели",
                "tax_object": "avz",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "302",
                "alr_msg": "Обнаружен вредоносный файл",
                "tax_object": "avz",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "4",
                        "field": "user"
                    },
                    {
                        "value": "1",
                        "field": "process"
                    }
                ]
            },
            {
                "string": "802",
                "alr_msg": "Подключено запрещенное устройство",
                "tax_object": "hw",
                "tax_action": "drop",
                "regex": [
                    {
                        "value": "4",
                        "field": "user"
                    }
                ]
            }
        ]
    },
    {
        "name": "ASO_Eltex-4.0",
        "desc": "Eltex MES3324 v.4.0",
        "profile": "Syslog",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "LINK-I-Up:",
                "alr_msg": "Физическое поднятие порта АСО",
                "tax_object": "port",
                "tax_action": "on",
                "regex": []
            },
            {
                "string": "LINK-I-Up: Vlan",
                "alr_msg": "Поднятие Vlan в АСО",
                "tax_object": "port",
                "tax_action": "on",
                "regex": []
            },
            {
                "string": "AAA-I-CONNECT",
                "alr_msg": "Успешная аутентификация в АСО",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": []
            },
            {
                "string": "AAA-W-REJECT",
                "alr_msg": "Неуспешная аутентификация в АСО",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": []
            },
            {
                "string": "SYSLOG-N-NEWSYSLOGSERVER",
                "alr_msg": "Изменение конфигурации syslog сервера АСО",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "COPY-I-FILECPY",
                "alr_msg": "Запись новой конфигурации в АСО",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "New http",
                "alr_msg": "Использование запрещённого сервиса HTTP на АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "telnet",
                "alr_msg": "Использование запрещённого сервиса Telnet на АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "%INIT-I-Startup",
                "alr_msg": "Старт АСО",
                "tax_object": "os",
                "tax_action": "start",
                "regex": []
            }
        ]
    },
    {
        "name": "RA_AlphaServer",
        "desc": "Удаленный доступ Ethercut AlphaServer",
        "profile": "OPCUA",
        "tax_main": "ra",
        "logs": [],
        "events": [
            {
                "string": "RA_ENABLE:True",
                "alr_msg": "Удаленный доступ на площадку включен",
                "tax_object": "app",
                "tax_action": "on",
                "regex": []
            },
            {
                "string": "RA_ENABLE:False",
                "alr_msg": "Удаленный доступ на площадку выключен",
                "tax_object": "app",
                "tax_action": "off",
                "regex": []
            }
        ]
    },
    {
        "name": "ASO_NAS",
        "desc": "Synology",
        "profile": "Syslog",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "logged in successfully",
                "alr_msg": "Успешный вход пользователя",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "User %s",
                        "field": "user"
                    },
                    {
                        "value": "via %s",
                        "field": "protocol"
                    },
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "failed to log in",
                "alr_msg": "Неуспешный вход пользователя",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "User %s",
                        "field": "user"
                    },
                    {
                        "value": "via %s",
                        "field": "protocol"
                    },
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "System started to boot up",
                "alr_msg": "Старт АСО",
                "tax_object": "os",
                "tax_action": "start",
                "regex": []
            }
        ]
    },
    {
        "name": "ARM_MSWindows-XP",
        "desc": "WindowsXP, Windows Server 2003",
        "profile": "MSWindows",
        "tax_main": "arm",
        "logs": [],
        "events": [
            {
                "string": "517",
                "alr_msg": "Произошла очистка журнала",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "3",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "592",
                "alr_msg": "Запуск процесса",
                "tax_object": "app",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "3",
                        "field": "user"
                    },
                    {
                        "value": "1",
                        "field": "process"
                    }
                ]
            },
            {
                "string": "529",
                "alr_msg": "Неуспешный вход пользователя",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    },
                    {
                        "value": "2",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "538",
                "alr_msg": "Успешный вход пользователя",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    },
                    {
                        "value": "3",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "6006",
                "alr_msg": "Перезагрузка системы",
                "tax_object": "os",
                "tax_action": "start",
                "regex": []
            },
            {
                "string": "576",
                "alr_msg": "Вход с правами администратора",
                "tax_object": "user",
                "tax_action": "login.adm",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    },
                    {
                        "value": "3",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "624",
                "alr_msg": "Создана новая учетная запись",
                "tax_object": "user",
                "tax_action": "add",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "642",
                "alr_msg": "Изменена учетная запись",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "628",
                "alr_msg": "Сброс пароля пользователю",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "636",
                "alr_msg": "Добавлена группа безопасности пользователю",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "1",
                        "field": "user"
                    },
                    {
                        "value": "2",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "602",
                "alr_msg": "Создание нового задания планировщика",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "601",
                "alr_msg": "Установлена новая служба в системе",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "630",
                "alr_msg": "Удалена учетная запись",
                "tax_object": "user",
                "tax_action": "del",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    },
                    {
                        "value": "3",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "853",
                "alr_msg": "Изменение состояния МСЭ",
                "tax_object": "fw",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "851",
                "alr_msg": "Изменение правила МСЭ",
                "tax_object": "fw",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "612",
                "alr_msg": "Изменена политика аудита",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "538",
                "alr_msg": "Выход пользователя",
                "tax_object": "user",
                "tax_action": "logout",
                "regex": [
                    {
                        "value": "0",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "612",
                "alr_msg": "Изменение политики Аудит",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "643",
                "alr_msg": "Изменение политики Учетные записи",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "608",
                "alr_msg": "Изменение политики",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "609",
                "alr_msg": "Изменение политики",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "618",
                "alr_msg": "Изменение политики",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "520",
                "alr_msg": "Измененено системное время",
                "tax_object": "time",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "2",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "0",
                "alr_msg": "Потеряна связь с АРМ",
                "tax_object": "port",
                "tax_action": "error",
                "regex": []
            }
        ]
    },
    {
        "name": "ARM_KasperskyKICS-2.6",
        "desc": "KICS v.2.6",
        "profile": "KICS",
        "tax_main": "arm",
        "logs": [],
        "events": [
            {
                "string": "8269",
                "alr_msg": "Запрет запуска ПО",
                "tax_object": "avz",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "user_name=\\\"%s",
                        "field": "user"
                    },
                    {
                        "value": "fileName=\\\"%s",
                        "field": "file"
                    }
                ]
            },
            {
                "string": "8481",
                "alr_msg": "Нарушение контроля целостности ПО",
                "tax_object": "avz",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "user_name=\\\"%a\\\"",
                        "field": "user"
                    },
                    {
                        "value": "path=\\\"%a\\\"",
                        "field": "file"
                    }
                ]
            }
        ]
    },
    {
        "name": "ASO_CiscoIOS-16",
        "desc": "Cisco IOS XE v.16",
        "profile": "Syslog",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "SEC_LOGIN-4-LOGIN_FAILED",
                "alr_msg": "Неуспешная аутентификация",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "user: %s",
                        "field": "user"
                    },
                    {
                        "value": "Source: %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "localport: %s",
                        "field": "dst_port"
                    },
                    {
                        "value": "Reason: %a]",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "SEC_LOGIN-5-LOGIN_SUCCESS",
                "alr_msg": "Успешная аутентификация",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "user: %s",
                        "field": "user"
                    },
                    {
                        "value": "Source: %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "localport: %s",
                        "field": "protocol"
                    }
                ]
            },
            {
                "string": "AUTHMGR-5-SECURITY_VIOLATION",
                "alr_msg": "Заблокирована авторизация с неразрешенного IP",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "interface %s",
                        "field": "interface"
                    },
                    {
                        "value": "MAC address %s",
                        "field": "mac"
                    }
                ]
            },
            {
                "string": "SEC_LOGIN-1-QUIET_MODE_ON",
                "alr_msg": "Учетная запись заблокирована",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "user: %s",
                        "field": "user"
                    },
                    {
                        "value": "Source: %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "localport: %s",
                        "field": "src_port"
                    },
                    {
                        "value": "Reason: %a]",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "AAA-5-USER_LOCKED",
                "alr_msg": "Учетная запись заблокирована",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "User %s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "SEC_LOGIN-5-QUIET_MODE_OFF",
                "alr_msg": "Учетная запись разблокирована автоматически",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "AAA-5-USER_UNLOCKED",
                "alr_msg": "Учетная запись разблокирована администратором",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "User %s",
                        "field": "user"
                    },
                    {
                        "value": "unlocked by %s",
                        "field": "reason"
                    },
                    {
                        "value": "on %a",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "SYS-5-PRIV_AUTH_PASS",
                "alr_msg": "Повышение прилегий (вход режим enable)",
                "tax_object": "user",
                "tax_action": "login.adm",
                "regex": [
                    {
                        "value": "set to %s",
                        "field": "privilege"
                    },
                    {
                        "value": "by %s",
                        "field": "user"
                    },
                    {
                        "value": "on %a",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "SYS-5-RELOAD",
                "alr_msg": "Перезагрузка",
                "tax_object": "os",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "requested %a",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "SYS-5-RESTART",
                "alr_msg": "Перезагрузка",
                "tax_object": "os",
                "tax_action": "start",
                "regex": []
            },
            {
                "string": "SYS-5-CONFIG_I",
                "alr_msg": "Выход из режима конфигурации",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "from %s",
                        "field": "interface"
                    },
                    {
                        "value": "by %s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "SYS-5-CONFIG_NV_I",
                "alr_msg": "Произошла замена загрузочной конфигурации",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "by %s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "AUTHMGR-0-CONFIG_CORRUPT",
                "alr_msg": "Нарушение конфигурации интерфейсов",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "EXPRESS_SETUP-6-CONFIG_IS_RESET",
                "alr_msg": "Сброс конфигурации в начальное состояние",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "LINEPROTO-5-UPDOWN: Line protocol on Interface Gig",
                "alr_msg": "Физичечкое включение/выключение порта",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "Interface %s",
                        "field": "interface"
                    },
                    {
                        "value": "state to %s",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "LINK-5-CHANGED",
                "alr_msg": "Административное изменение состояния порта",
                "tax_object": "port",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "Interface %s",
                        "field": "interface"
                    },
                    {
                        "value": "state to %s",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "PORT_SECURITY-2-PSECURE_VIOLATION",
                "alr_msg": "Подключено неразрешенноe устройтсво",
                "tax_object": "port",
                "tax_action": "drop",
                "regex": [
                    {
                        "value": "port %a",
                        "field": "interface"
                    },
                    {
                        "value": "address %s",
                        "field": "mac"
                    }
                ]
            },
            {
                "string": "FW-4-ALERT_ON",
                "alr_msg": "Превышение пропускной способности, DOS-атака",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "ARP-3-ARPINT",
                "alr_msg": "Нарушение таблицы ARP",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "IP-4-DUPADDR",
                "alr_msg": "В сети зарегистрированы одинаковые IP",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "address %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "on %s",
                        "field": "interface"
                    },
                    {
                        "value": "by %s",
                        "field": "mac"
                    }
                ]
            },
            {
                "string": "AUTHMGR-5-MACMOVE",
                "alr_msg": "В сети зарегистрированы одинаковые MAC",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "address %s",
                        "field": "mac"
                    },
                    {
                        "value": "Interface %s",
                        "field": "interface"
                    },
                    {
                        "value": "to Interface %s",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "MAC_MOVE-SP-4-NOTIF",
                "alr_msg": "В сети зарегистрированы одинаковые MAC",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "Host %s",
                        "field": "mac"
                    }
                ]
            },
            {
                "string": "SYS-6-CLOCKUPDATE",
                "alr_msg": "Изменение времени",
                "tax_object": "time",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "configured from %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "WARMUPGRADE-3",
                "alr_msg": "Загрузка нового встроенного ПО",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "logged command:username",
                "alr_msg": "Изменение пользователя",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "User:%s",
                        "field": "user"
                    },
                    {
                        "value": "logged command:username %a",
                        "field": "reason"
                    }
                ]
            }
        ]
    },
    {
        "name": "ASO_Huawei-500",
        "desc": "Huawei USG6500 v.V500",
        "profile": "Syslog",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "SSH/4/SSH_FAIL",
                "alr_msg": "Неуспешная аутентификация SSH",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "IP=%s",
                        "field": "src_ip"
                    },
                    {
                        "value": "UserName=%s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "HTTPD/5/FAIL",
                "alr_msg": "Неуспешная аутентификация HTTP",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": ":User %s",
                        "field": "user"
                    },
                    {
                        "value": "IP:%s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "HTTPD/6/PASS",
                "alr_msg": "Успешная аутентификация HTTP",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": ":User %s",
                        "field": "user"
                    },
                    {
                        "value": "IP:%s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "SHELL/5/LOGIN",
                "alr_msg": "Успешная аутентификация SSH",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "UserName=%s",
                        "field": "user"
                    },
                    {
                        "value": "Ip=%s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "DS/4/DATASYNC_CFGCHANGE:",
                "alr_msg": "Изменение конфигурации",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "Command=\"bind manager-user",
                "alr_msg": "Изменение пользователя",
                "tax_object": "user",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "manager-user %s",
                        "field": "user"
                    },
                    {
                        "value": "role %s",
                        "field": "privilege"
                    }
                ]
            },
            {
                "string": "Command=\"system-view\"",
                "alr_msg": "Вход в привилегированный режим",
                "tax_object": "user",
                "tax_action": "login.adm",
                "regex": [
                    {
                        "value": "UserName=%s",
                        "field": "user"
                    },
                    {
                        "value": "Ip=%s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "CMD/4/REBOOT",
                "alr_msg": "Перезагрузка системы",
                "tax_object": "os",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "User=%s",
                        "field": "user"
                    },
                    {
                        "value": "Ip=%s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "ENTEXT/4/DEVCFGRECOVERED",
                "alr_msg": "Перезагрузка системы",
                "tax_object": "os",
                "tax_action": "start",
                "regex": []
            },
            {
                "string": "Command=\"clock datetime",
                "alr_msg": "Время изменено",
                "tax_object": "time",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "command:set view ",
                "alr_msg": "Административное изменение состояния порта",
                "tax_object": "port",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "PHY/4/STATUSDOWN",
                "alr_msg": "Физичечкое включение/выключение порта",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "Ethernet%s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "CFM/4/SAVE",
                "alr_msg": "Сохранение конфигурации",
                "tax_object": "conf",
                "tax_action": "copy",
                "regex": []
            },
            {
                "string": "HTTPD/5/DOWNLOADSUCC",
                "alr_msg": "Сохранение конфигурации",
                "tax_object": "conf",
                "tax_action": "copy",
                "regex": []
            },
            {
                "string": "Command=\"startup saved-configuration",
                "alr_msg": "Произошла замена загрузочной конфигурации",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            }
        ]
    },
    {
        "name": "ASO_Moxa",
        "desc": "Moxa",
        "profile": "Syslog",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "INFO:Configuration change activated",
                "alr_msg": "Изменение конфигурации АСО",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "link on",
                "alr_msg": "Физическое включение порта АСО",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "Port %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "auth. success",
                "alr_msg": "Успешная аутентификация в АСО",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "Account '%s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "auth. fail",
                "alr_msg": "Неуспешная аутентификация в АСО",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "Account %s",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "mac-sticky-violation",
                "alr_msg": "Подключения незарегистрированного MAC в АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "mac:%s",
                        "field": "mac"
                    },
                    {
                        "value": "port:%s",
                        "field": "src_port"
                    }
                ]
            },
            {
                "string": "Warm start by Firmware Upgrade",
                "alr_msg": "Изменение прошивки",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            }
        ]
    },
    {
        "name": "PLC_ProsoftRegul-1.6",
        "desc": "Prosoft Regul v.1.6",
        "profile": "ProsoftRegul",
        "tax_main": "plc",
        "logs": [],
        "events": [
            {
                "string": "Start application done",
                "alr_msg": "Старт проекта ПЛК",
                "tax_object": "app",
                "tax_action": "start",
                "regex": []
            },
            {
                "string": "Stop application done",
                "alr_msg": "Стоп проекта ПЛК",
                "tax_object": "app",
                "tax_action": "stop",
                "regex": [
                    {
                        "value": "application done %a\"",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "link::1",
                "alr_msg": "Физическое включение порта ПЛК",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "@%s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "link::0",
                "alr_msg": "Физическое выключение порта ПЛК",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "@%s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "Board started",
                "alr_msg": "Старт ПЛК",
                "tax_object": "os",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "boot reason - %a",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "Firmware version:",
                "alr_msg": "Версия прошивки ПЛК",
                "tax_object": "os",
                "tax_action": "check",
                "regex": [
                    {
                        "value": "version: %s",
                        "field": "version"
                    }
                ]
            },
            {
                "string": "LoadBootprojectDone",
                "alr_msg": "Проверка загрузочного проект на ПЛК",
                "tax_object": "app",
                "tax_action": "check",
                "regex": [
                    {
                        "value": "crc=%s",
                        "field": "crc"
                    }
                ]
            },
            {
                "string": "Accept connection from address",
                "alr_msg": "Подключение к ПЛК",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "<ipaddress>%a</ipaddress",
                        "field": "src_ip"
                    },
                    {
                        "value": "<port>%a</port",
                        "field": "src_port"
                    }
                ]
            },
            {
                "string": "M=\"Key",
                "alr_msg": "Изменение переключателя на лицевой панели ПЛК",
                "tax_object": "hw",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "CreateBootprojectDone",
                "alr_msg": "Изменение загрузочного проекта на ПЛК",
                "tax_object": "app",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "loaded via [",
                "alr_msg": "Загрузка нового проекта на ПЛК",
                "tax_object": "app",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "The first initialization",
                "alr_msg": "Первоначальная инициализация ПЛК",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "No free space available",
                "alr_msg": "Закончилось свободное место на ПЛК",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "end: restore/",
                "alr_msg": "Восстановление резервной копии ПЛК",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "end: backup",
                "alr_msg": "Создание резервной копии ПЛК",
                "tax_object": "os",
                "tax_action": "copy",
                "regex": []
            },
            {
                "string": "end: etc/pf.conf",
                "alr_msg": "Изменение настроек Межсетевого экрана на ПЛК",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "update/RegulFw.fwe",
                "alr_msg": "Обновление прошивки ПЛК",
                "tax_object": "os",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "Switch RUN/STOP changed to RUN",
                "alr_msg": "Ручной старт с помощью переключателя",
                "tax_object": "hw",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "Switch RUN/STOP changed to STOP",
                "alr_msg": "Ручной стоп с помощью переключателя",
                "tax_object": "hw",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "PLC Connection error",
                "alr_msg": "Ошибка подключения к системе",
                "tax_object": "port",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "end: etc/routes",
                "alr_msg": "Изменение настроек сети",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "end: etc/runtime.cfg",
                "alr_msg": "Изменение настроек сервисов",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "end: etc/ntp.conf",
                "alr_msg": "Изменение настроек времени",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "end: etc/pf.conf",
                "alr_msg": "Изменение настроек межсетевого экрана",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "<<<Filetransfer",
                "alr_msg": "Запись файла на ПЛК",
                "tax_object": "",
                "tax_action": "",
                "regex": [
                    {
                        "value": "end: %a\\\"",
                        "field": "file"
                    }
                ]
            }
        ]
    },
    {
        "name": "NET_Netmap",
        "desc": "События от мониторинга сети",
        "profile": "Netmap",
        "tax_main": "net",
        "logs": [],
        "events": [
            {
                "string": "up",
                "alr_msg": "Актив стал доступен",
                "tax_object": "port",
                "tax_action": "on",
                "regex": []
            },
            {
                "string": "down",
                "alr_msg": "Актив стал недоступен",
                "tax_object": "port",
                "tax_action": "off",
                "regex": []
            }
        ]
    },
    {
        "name": "ASO_PoligonInzer-1.14",
        "desc": "Poligon Inzer 2240, 2208GE v.1.14",
        "profile": "Syslog",
        "tax_main": "aso",
        "logs": [],
        "events": [
            {
                "string": "SYS-BOOTING",
                "alr_msg": "Произошла перезагрузка АСО",
                "tax_object": "os",
                "tax_action": "start",
                "regex": [
                    {
                        "value": "made a %s",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "SYS-5-CONFIG_SAVE",
                "alr_msg": "Изменение конфигурации АСО",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "using %s",
                        "field": "protocol"
                    },
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    },
                    {
                        "value": "GigabitEthernet %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "HTTP",
                "alr_msg": "Использование запрещённого сервиса на АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "TELNET",
                "alr_msg": "Использование запрещённого сервиса на АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": []
            },
            {
                "string": "AAA-6-SUCCESS",
                "alr_msg": "Успешная аутентификация в АСО",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "successful for \\'%s",
                        "field": "user"
                    },
                    {
                        "value": "with privilege %s",
                        "field": "privilege"
                    },
                    {
                        "value": "by address %s",
                        "field": "mac"
                    },
                    {
                        "value": "using %s",
                        "field": "protocol"
                    },
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "AAA-5-FAILURE",
                "alr_msg": "Неуспешная аутентификация в АСО",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "failed for \\'%s",
                        "field": "user"
                    },
                    {
                        "value": "with privilege %s",
                        "field": "privilege"
                    },
                    {
                        "value": "by address %s",
                        "field": "mac"
                    },
                    {
                        "value": "using %s",
                        "field": "protocol"
                    },
                    {
                        "value": "from %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "ACCESS_MGMT-ACCESS_DENIED",
                "alr_msg": "Подключение с незарегистрированного IP в АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "filter reject %s",
                        "field": "protocol"
                    },
                    {
                        "value": "IP address %s",
                        "field": "src_ip"
                    }
                ]
            },
            {
                "string": "SYS-FIRMWARE: New firmware",
                "alr_msg": "Загрузка нового встроенного ПО в АСО",
                "tax_object": "os",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "active: %s",
                        "field": "version"
                    }
                ]
            },
            {
                "string": "ALARM-TEMP",
                "alr_msg": "Высокая температура АСО",
                "tax_object": "hw",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "LINK-UPDOWN: Interface GigabitEthernet",
                "alr_msg": "Состояние сетевого порта изменилось в АСО",
                "tax_object": "port",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "Interface %a,",
                        "field": "interface"
                    },
                    {
                        "value": "changed state to %s",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "state to administratively up.",
                "alr_msg": "Административное включение порта АСО",
                "tax_object": "port",
                "tax_action": "change",
                "regex": [
                    {
                        "value": "Interface %s",
                        "field": "interface"
                    }
                ]
            },
            {
                "string": "PORT_SEC-2-VIOLATION",
                "alr_msg": "Подключения незарегистрированного MAC в АСО",
                "tax_object": "sec",
                "tax_action": "alert",
                "regex": [
                    {
                        "value": "by address %s",
                        "field": "mac"
                    }
                ]
            }
        ]
    },
    {
        "name": "SCD_WinCC",
        "desc": "WinCC",
        "profile": "WinCC",
        "tax_main": "scd",
        "logs": [],
        "events": [
            {
                "string": "Неуспешная попытка входа",
                "alr_msg": "Неуспешная аутентификация в СКАДА",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": [
                    {
                        "value": "5",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "Регистрация в СДКУ",
                "alr_msg": "Успешная аутентификация в СКАДА",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": [
                    {
                        "value": "6",
                        "field": "user"
                    }
                ]
            },
            {
                "string": "Открытие",
                "alr_msg": "Открытие экранной формы",
                "tax_object": "form",
                "tax_action": "on",
                "regex": [
                    {
                        "value": "6",
                        "field": "user"
                    },
                    {
                        "value": "3",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "Закрытие ЭФ",
                "alr_msg": "Зарытие экранной формы",
                "tax_object": "form",
                "tax_action": "off",
                "regex": [
                    {
                        "value": "6",
                        "field": "user"
                    },
                    {
                        "value": "3",
                        "field": "reason"
                    }
                ]
            },
            {
                "string": "Выгрузка информации",
                "alr_msg": "Выгрузка информации из СКАДА",
                "tax_object": "file",
                "tax_action": "copy",
                "regex": [
                    {
                        "value": "6",
                        "field": "user"
                    },
                    {
                        "value": "3",
                        "field": "reason"
                    }
                ]
            }
        ]
    },
    {
        "name": "ZIEM_ZIEM",
        "desc": "ZIEM 1.5",
        "profile": "ZIEM",
        "tax_main": "ziem",
        "logs": [],
        "events": [
            {
                "string": "2100",
                "alr_msg": "Вход пользователя",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": []
            },
            {
                "string": "1211",
                "alr_msg": "Ошибка подключения к источнику",
                "tax_object": "port",
                "tax_action": "error",
                "regex": [
                    {
                        "value": "node",
                        "field": "alr_node"
                    },
                    {
                        "value": "ip",
                        "field": "alr_ip"
                    }
                ]
            },
            {
                "string": "1212",
                "alr_msg": "Отсутствуют сообщения от источника",
                "tax_object": "port",
                "tax_action": "down",
                "regex": [
                    {
                        "value": "node",
                        "field": "alr_node"
                    },
                    {
                        "value": "ip",
                        "field": "alr_ip"
                    }
                ]
            },
            {
                "string": "1200",
                "alr_msg": "Ошибка модуля",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1201",
                "alr_msg": "Ошибка перезапуска задачи",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1202",
                "alr_msg": "Ошибка записи данных в БД",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1203",
                "alr_msg": "Ошибка отправки в Sender",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1204",
                "alr_msg": "Ошибка отправки в OPC сервер",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1205",
                "alr_msg": "Ошибка задачи Отчета о работе ZIEM",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1206",
                "alr_msg": "Ошибка задачи Контроля потока сообщений",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1207",
                "alr_msg": "Ошибка обработки данных",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1208",
                "alr_msg": "Ошибка задачи",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1209",
                "alr_msg": "Ошибка чтения файла",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "1210",
                "alr_msg": "Ошибка задачи Мониторинга сети",
                "tax_object": "app",
                "tax_action": "error",
                "regex": []
            },
            {
                "string": "2100",
                "alr_msg": "Вход пользователя",
                "tax_object": "user",
                "tax_action": "login.succ",
                "regex": []
            },
            {
                "string": "2101",
                "alr_msg": "Выход пользователя",
                "tax_object": "user",
                "tax_action": "logout",
                "regex": []
            },
            {
                "string": "2102",
                "alr_msg": "Пользователь изменил пароль",
                "tax_object": "user",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2103",
                "alr_msg": "Добавлено правило",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2104",
                "alr_msg": "Изменено правило",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2105",
                "alr_msg": "Скопировано правило",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2106",
                "alr_msg": "Удалено правило",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2107",
                "alr_msg": "Правила установлены в ядро ZIEM",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2108",
                "alr_msg": "Правила экспортированы",
                "tax_object": "conf",
                "tax_action": "",
                "regex": []
            },
            {
                "string": "2109",
                "alr_msg": "Добавлена УЗ для подлключения к источнику",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2110",
                "alr_msg": "Изменена УЗ для подлключения к источнику",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2111",
                "alr_msg": "Удалена УЗ для подключения к источнику",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2112",
                "alr_msg": "Базовые настройки изменены",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2113",
                "alr_msg": "Настройки добавлены через импорт данных",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2114",
                "alr_msg": "Настройки изменены через импорт данных",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2115",
                "alr_msg": "Настройки экспортированы",
                "tax_object": "conf",
                "tax_action": "",
                "regex": []
            },
            {
                "string": "2116",
                "alr_msg": "Добавлен параметр",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2117",
                "alr_msg": "Изменен параметр",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2118",
                "alr_msg": "Удален параметр",
                "tax_object": "conf",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2119",
                "alr_msg": "Перезапуск ядра ZIEM",
                "tax_object": "app",
                "tax_action": "start",
                "regex": []
            },
            {
                "string": "2120",
                "alr_msg": "Обновление ZIEM",
                "tax_object": "app",
                "tax_action": "change",
                "regex": []
            },
            {
                "string": "2121",
                "alr_msg": "Неуспешный вход пользователя",
                "tax_object": "user",
                "tax_action": "login.fail",
                "regex": []
            }
        ]
    },
    {
        "name": "RA_ProsoftRegul",
        "desc": "Удаленный доступ Ethercut ProsoftRegul R200",
        "profile": "OPCUA",
        "tax_main": "ra",
        "logs": [],
        "events": [
            {
                "string": "Application.GVL.gloobRA:True",
                "alr_msg": "Удаленный доступ на площадку включен",
                "tax_object": "port",
                "tax_action": "on",
                "regex": []
            },
            {
                "string": "Application.GVL.gloobRA:False",
                "alr_msg": "Удаленный доступ на площадку выключен",
                "tax_object": "port",
                "tax_action": "off",
                "regex": []
            }
        ]
    }
]
```