```json
[
    {
        "name": "ARM_LoginFail5",
        "desc": "5 неуспешных попыток входа в АРМ",
        "crit": "medium",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "user",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_LoginRemote",
        "desc": "Удаленный вход на АРМ",
        "crit": "high",
        "clas": "В6 Создание несанкционированного канала доступа в ЛВС",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 3600,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 1,
                "incfilter": [
                    {
                        "value": "3, 11",
                        "field": "privilege"
                    }
                ],
                "excfilter": [
                    {
                        "value": "ziem_user",
                        "field": "user"
                    }
                ]
            }
        ]
    },
    {
        "name": "ARM_LoginFail5Success",
        "desc": "5 неуспешных попыток и успешный вход в АРМ",
        "crit": "high",
        "clas": "Б2 Компрометация учетных данных",
        "uniq1": "alr_node",
        "uniq2": "user",
        "timer": 120,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            },
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_ProxyLolbas",
        "desc": "Запуск потенциально опасных процессов на АРМ",
        "crit": "medium",
        "clas": "Д4 Заражение вредоносным ПО",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 5,
                "incfilter": [
                    {
                        "value": "psexec.exe, schtasks.exe, rundll32.exe, regsvr32.exe, syncappvpublishingserver.exe, mavinject.exe, mshta.exe, msiexec.exe, odbcconf.exe, hh.exe, cmstp.exe, installutil.exe, regsvcs.exe, regasm.exe, winrm.exe, bitsadmin.exe",
                        "field": "process"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_Systeminfo",
        "desc": "Сбор информации о системе на АРМ",
        "crit": "medium",
        "clas": "Д11 Повышение привилегий",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 4,
                "incfilter": [
                    {
                        "value": "accesschk.exe, subinacl.exe, cacls.exe, icacls.exe, net.exe, netstat.exe, ipconfig.exe, nbtstat.exe, tasklist.exe, ping.exe, reg.exe, sc.exe, route.exe, systeminfo.exe, netsh.exe, w32tm.exe, whoami.exe, qwinsta.exe, netstat.exe, findstr.exe",
                        "field": "process"
                    }
                ],
                "excfilter": [
                    {
                        "value": "Администратор АРМ",
                        "field": "user"
                    }
                ]
            }
        ]
    },
    {
        "name": "ARM_Runas",
        "desc": "Запуск процесса от имени чужой записи на АРМ",
        "crit": "medium",
        "clas": "Б2 Компрометация учетных данных",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 0,
                "incfilter": [
                    {
                        "value": "runas.exe",
                        "field": "process"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_Utilman",
        "desc": "Изменение специальных возможностей ОС на АРМ",
        "crit": "low",
        "clas": "Д11 Повышение привилегий",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 0,
                "incfilter": [
                    {
                        "value": "utilman.exe",
                        "field": "process"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_WmiUse",
        "desc": "Зафиксировано использование WMI на АРМ",
        "crit": "medium",
        "clas": "Д6 Использование инструментария для проведения атак",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 0,
                "incfilter": [
                    {
                        "value": "wmic.exe, mofcomp.exe",
                        "field": "process"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_RemoteManagment",
        "desc": "Использование средств удаленного администрирования на АРМ",
        "crit": "high",
        "clas": "В2 Несанкционированное подключение устройств к ЛВС",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 0,
                "incfilter": [
                    {
                        "value": "radmin.exe, vncviewer.exe, teamviewer.exe, rserver.exe, winvnc.exe",
                        "field": "process"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_LoginNightTime",
        "desc": "Успешный вход в систему в нерабочее время на АРМ",
        "crit": "high",
        "clas": "Б1 Несанкционированное использование учетной записи",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 30,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 1,
                "incfilter": [
                    {
                        "value": "20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7",
                        "field": "alr_time"
                    },
                    {
                        "value": "Администратор АРМ, Куратор ИБ",
                        "field": "user"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_LoginStdUser",
        "desc": "Использование стандартной учетной записи на АРМ",
        "crit": "high",
        "clas": "Б1 Несанкционированное использование учетной записи",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [
                    {
                        "value": "Администратор,  Гость",
                        "field": "user"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ASO_LoginNightTime",
        "desc": "Успешный вход в нерабочее время в АСО",
        "crit": "high",
        "clas": "Б1 Несанкционированное использование учетной записи",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [
                    {
                        "value": "20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7",
                        "field": "alr_time"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ASO_LoginConsole",
        "desc": "Подключение консольным кабелем к АСО",
        "crit": "medium",
        "clas": "В3 Несанкционированное подключение устройств к СВТ",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [
                    {
                        "value": "CONSOLE, 0",
                        "field": "protocol"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ASO_Login5Fail",
        "desc": "5 неуспешных попыток входа в АСО",
        "crit": "medium",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ASO_LoginFail5Success",
        "desc": "5 неуспешных попыток и успешный вход в АСО",
        "crit": "high",
        "clas": "Б2 Компрометация учетных данных",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 30,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            },
            {
                "tax_main": "aso",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ASO_LoginUnregIP",
        "desc": "Подключение с неразрешенного IP к АСО",
        "crit": "high",
        "clas": "В2 Несанкционированное подключение устройств к ЛВС",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": [
                    {
                        "value": "CONSOLE",
                        "field": "protocol"
                    }
                ]
            }
        ]
    },
    {
        "name": "PLC_ProjectCrcChange",
        "desc": "Новая контрольная сумма проекта на ПЛК",
        "crit": "high",
        "clas": "В4 Несанкционированное внесение изменений в ИС",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "plc",
                "tax_object": "app",
                "tax_action": "check",
                "diff": "crc",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "PLC_PortUpLogin",
        "desc": "Порт стал Активен и подключение инженерным ПО к ПЛК",
        "crit": "high",
        "clas": "В2 Несанкционированное подключение устройств к ЛВС",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 600,
        "events": [
            {
                "tax_main": "plc",
                "tax_object": "port",
                "tax_action": "on",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            },
            {
                "tax_main": "plc",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "PLC_LoginUnregIP",
        "desc": "Подключение с неразрешенного IP к ПЛК",
        "crit": "high",
        "clas": "В2 Несанкционированное подключение устройств к ЛВС",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "plc",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "PLC_LoginFail5",
        "desc": "5 неуспешных попыток входа в ПЛК",
        "crit": "medium",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "plc",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "PLC_LoginFail5Success",
        "desc": "5 неуспешных попыток и успешный вход в ПЛК",
        "crit": "medium",
        "clas": "Б2 Компрометация учетных данных",
        "uniq1": "alr_node",
        "uniq2": "user",
        "timer": 30,
        "events": [
            {
                "tax_main": "plc",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            },
            {
                "tax_main": "plc",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "PLC_LoginNightTime",
        "desc": "Успешный вход в нерабочее время в ПЛК",
        "crit": "medium",
        "clas": "Б1 Несанкционированное использование учетной записи",
        "uniq1": "",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "plc",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [
                    {
                        "value": "20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7",
                        "field": "alr_time"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ASO_LoginFailUnregIP",
        "desc": "Неуспешное подключение с неразрешенного IP к АСО",
        "crit": "high",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 30,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": [
                    {
                        "value": "CONSOLE",
                        "field": "protocol"
                    }
                ]
            }
        ]
    },
    {
        "name": "ARM_LoginFail100",
        "desc": "100 неуспешных попыток входа в АРМ",
        "crit": "high",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "user",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 100,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_LoginRDP",
        "desc": "Удаленный вход по RDP на АРМ",
        "crit": "high",
        "clas": "В6 Создание несанкционированного канала доступа в ЛВС",
        "uniq1": "",
        "uniq2": "",
        "timer": 10,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 1,
                "incfilter": [
                    {
                        "value": "10",
                        "field": "privilege"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ASO_LoginFail100",
        "desc": "100 неуспешных попыток входа в АСО",
        "crit": "high",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "user",
        "timer": 300,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 100,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "PLC_LoginFail100",
        "desc": "100 неуспешных попыток входа в ПЛК",
        "crit": "high",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "plc",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 100,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_PsexecSchtask",
        "desc": "Запуск psexecsvc.exe затем schtask.exe",
        "crit": "high",
        "clas": "Д4 Заражение вредоносным ПО",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 2,
                "incfilter": [
                    {
                        "value": "schtasks.exe",
                        "field": "process"
                    }
                ],
                "excfilter": []
            },
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 2,
                "incfilter": [
                    {
                        "value": "psexesvc.exe, schtasks.exe",
                        "field": "process"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_ConfigChangeReboot",
        "desc": "Изменение конфигурации АРМ затем перезагрузка",
        "crit": "high",
        "clas": "В4 Несанкционированное внесение изменений в ИС",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 3600,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "os",
                "tax_action": "start",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            },
            {
                "tax_main": "arm",
                "tax_object": "conf",
                "tax_action": "change",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_FileMassDel",
        "desc": "Массовое удаление файлов",
        "crit": "medium",
        "clas": "Д12 Деструктивная активность",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 10,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "file",
                "tax_action": "del",
                "diff": "",
                "count": 10,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_TimeChange",
        "desc": "Изменение системного времени на АРМ",
        "crit": "high",
        "clas": "Г1 Несанкционированное внесение изменений в СЗИ",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 10,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "time",
                "tax_action": "change",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": [
                    {
                        "value": "LOCAL SERVICE",
                        "field": "user"
                    }
                ]
            }
        ]
    },
    {
        "name": "ARM_FWChange",
        "desc": "Изменение состояния межсетевого экрана",
        "crit": "medium",
        "clas": "Г1 Несанкционированное внесение изменений в СЗИ",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 30,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "fw",
                "tax_action": "change",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_ConfigChange",
        "desc": "Изменение параметров АРМ",
        "crit": "medium",
        "clas": "В4 Несанкционированное внесение изменений в ИС",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 30,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "conf",
                "tax_action": "change",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "RA_RemoteAccessLong",
        "desc": "Удаленный доступ включен более 8 часов подряд",
        "crit": "high",
        "clas": "В6 Создание несанкционированного канала доступа в ЛВС",
        "uniq1": "",
        "uniq2": "",
        "timer": 28800,
        "events": [
            {
                "tax_main": "ra",
                "tax_object": "port",
                "tax_action": "on",
                "diff": "",
                "count": 8,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_HWAdd",
        "desc": "Подключено новое устройство",
        "crit": "low",
        "clas": "В3 Несанкционированное подключение устройств к СВТ",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 10,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "hw",
                "tax_action": "add",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": [
                    {
                        "value": "hid, hasp",
                        "field": "interface"
                    }
                ]
            }
        ]
    },
    {
        "name": "ARM_Hacktool",
        "desc": "Запуск программ для взлома на АРМ",
        "crit": "high",
        "clas": "Д6 Использование инструментария для проведения атак",
        "uniq1": "",
        "uniq2": "",
        "timer": 60,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "start",
                "diff": "",
                "count": 1,
                "incfilter": [
                    {
                        "value": "crackmapexec.exe, psexec.exe, psexesvc.exe",
                        "field": "process"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_NetShareAccess",
        "desc": "Доступ к сетевой папке АРМ",
        "crit": "",
        "clas": "В6 Создание несанкционированного канала доступа в ЛВС",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "file",
                "tax_action": "access.net",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "PLC_ConnectionLost",
        "desc": "Ошибка подключения к ПЛК",
        "crit": "high",
        "clas": "Е1 Сбои и отказы технических и программных средств",
        "uniq1": "interface",
        "uniq2": "alr_node",
        "timer": 86400,
        "events": [
            {
                "tax_main": "plc",
                "tax_object": "port",
                "tax_action": "error",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_ConnectionLost",
        "desc": "Ошибка подключения к АРМ",
        "crit": "high",
        "clas": "Е2 Сбои и отказы в работе СЗИ",
        "uniq1": "interface",
        "uniq2": "alr_node",
        "timer": 86400,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "port",
                "tax_action": "error",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_UserChange",
        "desc": "Изменение учетной записи на АРМ",
        "crit": "high",
        "clas": "Б5 Нарушение правил разграничения доступа",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 15,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "user",
                "tax_action": "change",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_FIlePermChange",
        "desc": "Изменение прав доступа к объектам",
        "crit": "high",
        "clas": "Г1 Несанкционированное внесение изменений в СЗИ",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "file",
                "tax_action": "change",
                "diff": "",
                "count": null,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "SCD_LoginFail100",
        "desc": "100 неуспешных попыток входа в Скада",
        "crit": "high",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "scd",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 100,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "SCD_LoginFail5",
        "desc": "5 неуспешных попыток входа в АРМ",
        "crit": "medium",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "scd",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "SCD_LoginFail5Success",
        "desc": "5 неуспешных попыток и успешный вход в АРМ",
        "crit": "high",
        "clas": "Б2 Компрометация учетных данных",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 120,
        "events": [
            {
                "tax_main": "scd",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            },
            {
                "tax_main": "scd",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 0,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ASO_ConfigChange",
        "desc": "Изменение конфигурации АСО",
        "crit": "high",
        "clas": "В4 Несанкционированное внесение изменений в ИС",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 60,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "conf",
                "tax_action": "change",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ZIEM_ConnectionLost",
        "desc": "Ошибка подключения к источнику",
        "crit": "high",
        "clas": "Е1 Сбои и отказы технических и программных средств",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 86400,
        "events": [
            {
                "tax_main": "ziem",
                "tax_object": "port",
                "tax_action": "error",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ZIEM_NetflowError",
        "desc": "Отсутствуют сообщения от источника ",
        "crit": "high",
        "clas": "Е1 Сбои и отказы технических и программных средств",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 86400,
        "events": [
            {
                "tax_main": "ziem",
                "tax_object": "port",
                "tax_action": "down",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ZIEM_Errors",
        "desc": "Обнаружено множество ошибок в работе ZIEM",
        "crit": "high",
        "clas": "Е2 Сбои и отказы в работе СЗИ",
        "uniq1": "",
        "uniq2": "",
        "timer": 86400,
        "events": [
            {
                "tax_main": "ziem",
                "tax_object": "app",
                "tax_action": "error",
                "diff": "",
                "count": 10,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ZIEM_ConfigChange",
        "desc": "Изменение конфигурации ZIEM",
        "crit": "high",
        "clas": "Г1 Несанкционированное внесение изменений в СЗИ",
        "uniq1": "",
        "uniq2": "",
        "timer": 86400,
        "events": [
            {
                "tax_main": "ziem",
                "tax_object": "conf",
                "tax_action": "change",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ZIEM_LoginFail5",
        "desc": "5 неуспешных попыток входа в АРМ",
        "crit": "medium",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "ziem",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 5,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ZIEM_LoginFail100",
        "desc": "100 неуспешных попыток входа в АРМ",
        "crit": "medium",
        "clas": "Д5 Подбор учетных данных",
        "uniq1": "",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "ziem",
                "tax_object": "user",
                "tax_action": "login.fail",
                "diff": "",
                "count": 100,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ZIEM_LoginNightTime",
        "desc": "Успешный вход в ZIEM в нерабочее время ",
        "crit": "high",
        "clas": "Б1 Несанкционированное использование учетной записи",
        "uniq1": "",
        "uniq2": "",
        "timer": 30,
        "events": [
            {
                "tax_main": "ziem",
                "tax_object": "user",
                "tax_action": "login.succ",
                "diff": "",
                "count": 1,
                "incfilter": [
                    {
                        "value": "20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7",
                        "field": "alr_time"
                    }
                ],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_PortUp",
        "desc": "Поднятие сетевого интерфейса",
        "crit": "",
        "clas": "В2 Несанкционированное подключение устройств к ЛВС",
        "uniq1": "alr_node",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "port",
                "tax_action": "on",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_ExeRestrict",
        "desc": "Запуск запрещенного ПО",
        "crit": "high",
        "clas": "Д12 Деструктивная активность",
        "uniq1": "alr_ip",
        "uniq2": "",
        "timer": 0,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "app",
                "tax_action": "drop",
                "diff": "",
                "count": null,
                "incfilter": [],
                "excfilter": [
                    {
                        "value": "IAStorIcon.exe, OneDriveStandaloneUpdater.exe, {A6D608F0-0BDE-491A-97AE-5C4B05D86E01}.bat",
                        "field": "process"
                    }
                ]
            }
        ]
    },
    {
        "name": "ASO_MACRestrict",
        "desc": "Подключение незарегистрированного MAC",
        "crit": "high",
        "clas": "В2 Несанкционированное подключение устройств к ЛВС",
        "uniq1": "alr_ip",
        "uniq2": "",
        "timer": 3600,
        "events": [
            {
                "tax_main": "aso",
                "tax_object": "port",
                "tax_action": "drop",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    },
    {
        "name": "ARM_FSControl",
        "desc": "Нарушение контроля целостности",
        "crit": "high",
        "clas": "В4 Несанкционированное внесение изменений в ИС",
        "uniq1": "alr_ip",
        "uniq2": "",
        "timer": 300,
        "events": [
            {
                "tax_main": "arm",
                "tax_object": "fsctrl",
                "tax_action": "alert",
                "diff": "",
                "count": 1,
                "incfilter": [],
                "excfilter": []
            }
        ]
    }
]
```