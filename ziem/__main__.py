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


from ziem.core import Core
from ziem.core import dropdb

from ziem.post import Poster

from ziem.web import start_app
from ziem.web import clearweb, dropweb, dropuser
from ziem.web.mainview import conf_install, get_version

from .conf import init, init_services, install_cert, init_nginx

def get_sudo():
    user = getpass.getuser()
    if user == 'zuser' or os.geteuid() == 0: return
    subprocess.call(['sudo', sys.executable, *sys.argv])
    sys.exit()    


def main():
    version = get_version()
    
    parser = argparse.ArgumentParser(
            prog='ziem', 
            usage='%(prog)s [options]',
            formatter_class=argparse.RawTextHelpFormatter,)
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
        help="Запуск POST. Отправка логов, отчет о работе ZIEM.", 
        action="store_true")
    parser.add_argument(
        "--confinstall", 
        help="Установка конфигурации из WEB в CORE.", 
        action="store_true")
    parser.add_argument(
        "--debug", 
        help="DEBUG режим. Использовать для WEB/CORE/CC.", 
        action="store_true")
    parser.add_argument(
        "--init", 
        help="Инициализация конфигурации системы.", 
        action="store_true")
    parser.add_argument(
        "--dropdb", 
        help="Очистка таблиц базы CORE: сообщения, события и инциденты.",
        action="store_true")
    parser.add_argument(
        "--dropinc", 
        help="Очистка инциденты из базы CORE.",
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
        "--ssl", 
        help="Запуск Flask с SSL-сертификатами.", 
        action="store_true")
    parser.add_argument(
        '-v',
        '--version', 
        action='version',
        version='%(prog)s ' + version, 
        help="Просмотр версии программы.")
    
    parser.add_argument('--host',
                        help='Хост для WEB-сервера, по умолчанию любой.',
                        default='0.0.0.0')
    
    parser.add_argument('--port',
                        help='Порт для WEB-сервера, по умолчанию 45000.',
                        default='45000')
    parser.add_argument(
        "--center", 
        '-cc',
        help='Параметр для запуска ZIEM CC.\n--init:  Установка ZIME CC.\n--debug: Гибридный режим.',
        action="store_true")
    
    parser.add_argument(
        "--services", 
        help="Обновление сервисов systemctl.", 
        action="store_true")
    
    parser.add_argument(
        "--certs", 
        help="Создать SSL сертификаты.", 
        action="store_true")   
    
    parser.add_argument(
        "--nginx", 
        help="Конфигурировать nginx.", 
        action="store_true")    
        
    parser._actions[0].help='Вызов данной справки.'
    #get_sudo()
    args = parser.parse_args()
    
    print('ZIEM {}\n'.format(version))

    
    if args.center:
        print(''' ______ _______ _______ _______   ______ ______ 
|__    |_     _|    ___|   |   | |      |      |
|__    |_|   |_|    ___|       | |   ---|   ---|
|______|_______|_______|__|_|__| |______|______|
                                
''')
    else:
        print('███████╗██╗███████╗███╗   ███╗\n'\
              '╚══███╔╝██║██╔════╝████╗ ████║\n'\
              '  ███╔╝ ██║█████╗  ██╔████╔██║\n'\
              ' ███╔╝  ██║██╔══╝  ██║╚██╔╝██║\n'\
              '███████╗██║███████╗██║ ╚═╝ ██║\n'\
              '╚══════╝╚═╝╚══════╝╚═╝     ╚═╝\n')
        
    if args.center and (not args.services and not args.init):
        os.environ["ZIEM_CENTER"] = '2' if args.debug else '1'
    else:  
        os.environ["ZIEM_CENTER"] = '0'
    
    if not os.getenv('ZIEM_FORMAT_LOG'):
        os.environ['ZIEM_FORMAT_LOG'] = '%(asctime)s ~ %(levelname)s ~ %(filename)s.%(funcName)s[%(lineno)d] ~ %(message)s'

    if args.core and not args.center:
        print('\n[*] Start ZIEM core\n----------------')
        uid = pwd.getpwnam('zuser')[2]
        os.setgid(uid)
        os.setuid(uid)
        core = Core()            
        asyncio.run(core.run(debug=args.debug))
    elif args.web or os.environ["ZIEM_CENTER"] == '1':
        print('\n[*] Start ZIEM web\n----------------')
        certs = None
        if args.ssl:
            certs = ('/etc/ssl/certs/nginx-selfsigned.crt', 
                     '/etc/ssl/private/nginx-selfsigned.key')
            for cert in certs:
                if not os.path.isfile(cert):
                    print(f'Сертификат "{cert}" не найден')
                    return
        start_app(args.host, args.port, certs, args.debug)
    elif args.post and not args.center:
        print('\n[*] Start ZIEM post\n----------------')
        uid = pwd.getpwnam('zuser')[2]
        os.setgid(uid)
        os.setuid(uid)
        poster = Poster()            
        poster.run(debug=args.debug)
    elif args.confinstall:
        print('\n[*] Installing WEB config to CORE \n----------------')
        conf_install()
    elif args.init:
        print('\n[*] Initialize config \n----------------')
        init(os.environ["ZIEM_CENTER"])
    elif args.dropdb:
        print('\n[*] Removed Database CORE\n----------------')
        asyncio.run(dropdb())
    elif args.dropinc:
        print('\n[*] Removed all incidents\n----------------')
        asyncio.run(dropdb(spec_col='incs'))
    elif args.clearweb:
        print('\n[*] Removed old data from WEB \n----------------')
        clearweb()
    elif args.dropweb:
        print('\n[*] Removed all data from WEB \n----------------')
        dropweb()
    elif args.dropuser:
        print('\n[*] Reset password for admin \n----------------')
        dropuser()
    elif args.services:
        init_services(args.center + args.debug if args.center else False)
        os.system('sudo systemctl restart ziemwebd')
    elif args.certs:
        install_cert()
    elif args.nginx:
        init_nginx(args.center + args.debug if args.center else False)
    else:
        parser.print_help()
        sys.exit(1)
        
if __name__ == "__main__":
    main()