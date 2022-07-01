"""
    ZIEM

    Description:

    Author:
        Bengart Zakhar
"""

#!/opt/ziem/venv/bin/python

import os
import sys
#if 'ziem' not in sys.path:
 #   sys.path.append('ziem')

import pwd
import time
import string
import random
import asyncio
import getpass
import argparse
import subprocess
import pkg_resources

from core import Core
from core import dropdb

from post import Poster

from web import start_app
from web import clearweb, dropweb, dropuser
from web.mainview import conf_install, get_version

from conf import init

def get_sudo():
    subprocess.call(['sudo', sys.executable, *sys.argv])
    sys.exit()    

if __name__ == "__main__":
    user = getpass.getuser()
    if user != 'zuser':
        if os.geteuid() != 0:
            get_sudo()
    version = get_version()#pkg_resources.get_distribution('ziem').version
    print('ZIEM {}\n'.format(version))
    print('███████╗██╗███████╗███╗   ███╗\n'\
          '╚══███╔╝██║██╔════╝████╗ ████║\n'\
          '  ███╔╝ ██║█████╗  ██╔████╔██║\n'\
          ' ███╔╝  ██║██╔══╝  ██║╚██╔╝██║\n'\
          '███████╗██║███████╗██║ ╚═╝ ██║\n'\
          '╚══════╝╚═╝╚══════╝╚═╝     ╚═╝\n')
    parser = argparse.ArgumentParser(
        prog='ziem', 
        usage='%(prog)s [options]')
    parser.add_argument(
        "-c", 
        "--core", 
        help="Запуск CORE. Сбор, нормализация, корреляция событий.", 
        action="store_true")
    parser.add_argument(
        "-w", 
        "--web", 
        help="Запуск WEB. Работа в DEBUG режиме, только для проверки!", 
        action="store_true")
    parser.add_argument(
        "-p", 
        "--post", 
        help="Запуск POST. Отправка логов, отчет о работе ZIEM", 
        action="store_true")
    parser.add_argument(
        "--confinstall", 
        help="Установка конфигурации из WEB в CORE.", 
        action="store_true")
    parser.add_argument(
        "--debug", 
        help="DEBUG режим. Использовать для CORE.", 
        action="store_true")
    parser.add_argument(
        "--init", 
        help="Инициализация конфигурации системы", 
        action="store_true")
    parser.add_argument(
        "--dropdb", 
        help="Очистка базы CORE. Удаление всех сообщений, событий, инцидентов.", 
        action="store_true")
    parser.add_argument(
        "--clearweb", 
        help="Очистка базы WEB. Удаление источников и правил.", 
        action="store_true")
    parser.add_argument(
        "--dropweb", 
        help="Очистка базы WEB. Удаление всех настроек.", 
        action="store_true")
    parser.add_argument(
        "--dropuser", 
        help="Сброс пароля пользователю admin для входа в WEB.", 
        action="store_true")
    parser.add_argument(
        '--version', 
        action='version',
        version='%(prog)s ' + version, 
        help="Просмотр версии программы и дополнительной информации.")
    parser.add_argument('--port',
                        help='port of the web server',
                        default='45000')
    parser._actions[0].help='Вызов данной справки'
    args = parser.parse_args()
    if args.core:
        print('\n[*] Start ZIEM core\n----------------')
        uid = pwd.getpwnam('zuser')[2]
        os.setgid(uid)
        os.setuid(uid)
        core = Core()            
        if args.debug:
            asyncio.run(core.run(debug=True))
        else:
            asyncio.run(core.run())
    elif args.web:
        print('\n[*] Start ZIEM web\n----------------')
        start_app(args.port)
    elif args.post:
        print('\n[*] Start ZIEM post\n----------------')
        uid = pwd.getpwnam('zuser')[2]
        os.setgid(uid)
        os.setuid(uid)
        poster = Poster()            
        if args.debug:
            poster.run(debug=True)
        else:
            poster.run()
    elif args.confinstall:
        print('\n[*] Installing WEB config to CORE \n----------------')
        conf_install()
    elif args.init:
        print('\n[*] Initialize config \n----------------')
        init()
    elif args.install:
        print('\n[*] Install services \n----------------')
        install()
    elif args.dropdb:
        print('\n[*] Remove all data from Database \n----------------')
        asyncio.run(dropdb())
    elif args.clearweb:
        print('\n[*] Remove old data from WEB \n----------------')
        clearweb()
    elif args.dropweb:
        print('\n[*] Remove all data from WEB \n----------------')
        dropweb()
    elif args.dropuser:
        print('\n[*] Reset password for admin \n----------------')
        dropuser()
    else:
        parser.print_help()
        sys.exit(1)
