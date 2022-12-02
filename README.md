![logo](ziem/web/static/images/logo.png)

## _Простой и быстрый SIEM для АСУТП_ 
### _Руководство администратора_  

![](https://img.shields.io/badge/version-3.13-green)
![](https://img.shields.io/badge/debian-10-blue)
![](https://img.shields.io/badge/astra-1.6-blue)
![](https://img.shields.io/badge/python-3.9-blue)
![](https://img.shields.io/badge/flask-2.0.3-red)
![](https://img.shields.io/badge/pymongo-3.12.3-red)
![](https://img.shields.io/badge/motor-2.5.1-red)

> Данное руководство содержит необходимую информацию по установке и настройке системы  

##### Содержание  

[Информация](#info)  
    [Минимальные системные требования](#tth)  
    [Зависимости](#dep)  
[Установка](#inst)  
    [Обновление](#update)  
    [Инициализация](#init)  
    [Запуск](#run)  

<a name=info>

## Информация 

</a>

* 3IEM работает под системами ОС `Astra Linux` или `Debian >= 11`.  
* Разработан на скриптовом языке `Python3.9`.  
* Распространяется в виде образа `виртуальной машины`, а также в виде `дистрибутива`.
* Ведутся работы по контейнеризации продукта.

<a name=tth>

### Минимальные системные требования

</a>

* пропускная способность канала: 64 кбит/сек  
* свободно место на диске: 500 Гб

<a name=dep>

### Зависимости

</a>

**Окружение**

* nginx
* MongoDB
* Python==3.9


**Значимы версии пакетов python**

```
Flask==2.0.3
pymongo==3.12.3
motor==2.5.1
```

> С более новыми версиями пакетов модули ЗИЕМ требуют значительную модификацию кода.


<a name=inst>

## Установка

</a>

```sh
cd /opt
sudo git clone [zime]
cd ziem
sudo python3 -m venv venv
sudo venv/bin/pip install dist/*
```
**Акивация виртуальной среды**

`source venv/bin/activate`

### Инициализация

</a>

`(venv) sudo ziem --init`

* Создается дополнительный пользователь `zuser`, от имени которого работает ZIEM.  
* Создаются сервисы:
    - `zimecored` ядро опроса активов.
    - `zimewebd` web-сервер настройки.
    - `zimepostd` сервис отправки.
* Создаются каталоги для работы ZIEM:
    - /etc/opt/ziem - конфигурационные файлов, `root` запись, `zuser` чтение  
    - /var/opt/ziem - временные файлов, `zuser` запись  
    - /var/log/ziem - логи, `zuser` запись   
* Портируется конфигурация nginx для работы wsgi сервера gunicorn с Flask.
* Создается bin-ярлык для запуска ZIEM без активации виртуальной среды.

### Установка Control Center

`(venv) sudo ziem --init -cc`

* Флаг `-cc` задает параметр запуска WEB-модуля с параметром `center`
* Не будут создаваться сервисы CORE, POST.
* Не будет создаваться bin-ярлык

<hr>

<a name=run>

### Запуск

</a>

```sh
└─$ sudo venv/bin/ziem                                                                                                            
ZIEM 3.2

███████╗██╗███████╗███╗   ███╗
╚══███╔╝██║██╔════╝████╗ ████║
  ███╔╝ ██║█████╗  ██╔████╔██║
 ███╔╝  ██║██╔══╝  ██║╚██╔╝██║
███████╗██║███████╗██║ ╚═╝ ██║
╚══════╝╚═╝╚══════╝╚═╝     ╚═╝

usage: ziem [options]

optional arguments:
  -h, --help       Вызов данной справки
  -c, --core       Запуск CORE. Сбор, нормализация, корреляция событий.
  -w, --web        Запуск WEB. Работа в DEBUG режиме, только для проверки!
  -p, --post       Запуск POST. Отправка логов, отчет о работе ZIEM
  --confinstall    Установка конфигурации из WEB в CORE.
  --debug          DEBUG режим. Использовать для WEB/CORE.
  --init           Инициализация конфигурации системы
  --dropdb DROPDB  Очистка таблиц(ы) базы CORE. ALL - все таблицы
  --clearweb       Очистка базы WEB. Удаление источников и правил.
  --dropweb        Очистка базы WEB. Удаление всех настроек.
  --dropuser       Сброс пароля пользователю admin для входа в WEB.
  --ssl            Запуск Flask с SSL-сертификатами
  -v, --version    Просмотр версии программы.
  --host HOST      Хост для WEB-сервера, по умолчанию любой.
  --port PORT      Порт для WEB-сервера, по умолчанию 45000.
  --center, -cc    Запуск ZIEM CC. --init -cc: Установка ZIME CC
  --services       Обновление сервисов systemctl
  ```