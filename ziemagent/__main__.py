"""
    Agent for remote control ZIEM

    Description:
        Argparser for ZIEM Agent
        Main menu and args to start

    Author:
        Bengart Zakhar
        Kamnev Sergey
"""

#!/opt/ziem/venv/bin/python
import os
import sys
import asyncio
import getpass
import argparse
import subprocess
import pkg_resources
import logging

from .agent import Ziemagent
from .conf import init
from .books import Booksreader


def main():
    
    if not os.getenv('ZIEM_FORMAT_LOG'):
        os.environ['ZIEM_FORMAT_LOG'] = '%(asctime)s ~ %(levelname)s ~ %(filename)s.%(funcName)s[%(lineno)d] ~ %(message)s'
        
    print(pkg_resources.get_distribution('ziemagent').version)
    print('Agent for remote control ZIEM\n')
    print(' ____  __  ____  _  _         \n'\
          '(__  )(  )(  __)( \/ )        \n'\
          ' / _/  )(  ) _) / \/ \        \n'\
          '(____)(__)(____)\_)(_/        \n'\
          '  __    ___  ____  __ _  ____ \n'\
          ' / _\  / __)(  __)(  ( \(_  _)\n'\
          '/    \( (_ \ ) _) /    /  )(  \n'\
          '\_/\_/ \___/(____)\_)__) (__) \n')
    parser = argparse.ArgumentParser(
        prog='ziemagent', 
        usage='%(prog)s [options]')
    parser.add_argument(
        "--run",
        help="Start ziemagent",
        action="store_true")
    parser.add_argument(
        "--setconfig",
        help="Set ziemagent config",
        action="store_true")
    parser.add_argument(
        "--showconfig",
        help="Show ziemagent config",
        action="store_true")
    parser.add_argument(
        "--init", 
        help="Initialization ziemagent", 
        action="store_true")
    parser.add_argument(
        "--connect", 
        help="Conect to ZIEM center", 
        action="store_true")
    parser.add_argument(
        "--port", 
        help="Port to ZIEM center",
        nargs="?",
        const="46000")
    parser.add_argument(
        "--bks",
        help="Start book reader",
        action="store_true")
    parser.add_argument(
        "--minutes",
        help="API books polling period",
        nargs="?",
        default="1440")
    args = parser.parse_args()

    agent = Ziemagent(args.port)
    bks = Booksreader(int(args.minutes)*60, agent.config)
    
    if args.run:
        async def run():
            await asyncio.gather(agent.run(), bks.run())
        asyncio.run(run());
    elif args.init:
        print('\n[*] Initialize config \n----------------')
        init(args.bks)
    elif args.bks:
        asyncio.run(bks.run())
    elif args.setconfig:
        agent.setconfig()
    elif args.showconfig:
        agent.showconfig()

    elif args.connect:
        print('\n[*] Connecting to ZIEMCC \n----------------')
        asyncio.run(agent.connect())
    else:
        print("Not enough arguments, type --help for info")
        sys.exit(1)
        
if __name__ == "__main__":
    main()