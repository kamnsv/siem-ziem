"""
    ZIEM
    
    Description:
        Module for quick viewing of system logs, with rotation support
    Author:
        Kamnev Sergey
"""

import json
import yaml
import time
import os
import tarfile
import linecache
import logging

import re

from datetime import datetime, timedelta

from flask import Blueprint, redirect, flash
from flask import render_template, request, session, url_for
from flask import send_file, jsonify, abort, Markup


from .authview import login_required

bp = Blueprint('jou', __name__)


if not os.getenv('ZIEM_PATH_LOGS'):
    os.environ["ZIEM_PATH_LOGS"] = '/var/log/ziem'
    
if not os.getenv('ZIEM_PATH_TMP'):
    os.environ["ZIEM_PATH_TMP"] = '/var/opt/ziem/tmp'
    
class Journal:
    
    datetime_format_web = os.getenv('ZIEM_DATETIME_FORMAT_WEB', '%Y-%m-%dT%H:%M')
    datetime_format_log = os.getenv('ZIEM_DATETIME_FORMAT_LOG', '%Y-%m-%d %H:%M')
    
    def __init__(self, fname, search=None, start=None, end=None):
        '''
        fname - Базовое имя файла лога
        search - Строка поиска в логах
        start, end - даты, интервал поиска
        '''
        self.fname = fname
        self.search = search
        self.a, self.b = 0, 0
        try:
            if start:
                self.a = datetime.strptime(start, self.datetime_format_web)
            if end:
                self.b = datetime.strptime(end, self.datetime_format_web)
        except Exception as e: 
            logging.error('Error parse datetime intervals: ' + repr(e))
         
        try:
            self.build_nav()
        except Exception as e: 
            self.nav = None
            logging.error('Log navigator building error: ' + repr(e))
        
    def build_nav(self):
        # Составление навигатора по логам
        j, b = 1, 0 
        self.nav = []
        fname = self.fname
        while os.path.isfile(fname):
            linecache.checkcache(fname)
            a = b
            b, mapping = self.get_mapping(fname)
            b = a + b
            schema = {
                'path': fname,
                'a': a,
                'b': b,
                'map': mapping
            }
            self.nav.append(schema)
            fname = self.fname + f'.{j}'
            j += 1

    def get_count_lines(self, fname):
        with open(fname, 'r') as f:
            for count, _ in enumerate(f): pass
        return count + 1
    
    def get_mapping(self, fname):
        count = 0
        mapping = {}
        with open(fname, 'r') as f:
            for i, line in enumerate(f):
                if self.a or self.b:
                    time = line.split(' ~ ')[0].strip()
                    if len(time) < 16: continue
                    try:
                        time = datetime.strptime(time[:16], self.datetime_format_log)
                    except: continue
                    
                if self.a and self.a > time:
                    continue
                    
                if self.b and self.b < time:
                    continue
                
                if self.search and self.search not in f'#{i+1} {fname} {line}':
                    continue
                    
                count += 1
                if self.search or self.a or self.b:
                    mapping[count] = i + 1
                    
        return count, mapping
    
    def get_count_pages(self, fname, per=25):
        lines = self.get_count_lines(fname)
        count = lines // per + (lines % per > 0)
        return count
    
    def get_line(self, fname, n):
        return f'{n} ' +os.path.basename(fname)+' '+linecache.getline(fname, n)
    
    def get_total_lines(self):
        return self.nav[-1]['b']
        
    def get_total_pages(self, per=25):
        lines = self.get_total_lines()
        total = lines // per + (lines % per > 0)
        return total
    
    def get_total_line(self, n, rev=True):
        for s in self.nav:
            if n >= s['a'] and n < s['b']:
                i = (s['b'] - n) if rev else (n + 1)
                if not len(s['map']):
                    return self.get_line(s['path'], i)
                else:
                    return self.get_line(s['path'], s['map'][i])
    
    def items(self, page=1, per=25):
        lines = []
        for i in range((page-1)*per, page*per):
            line = self.get_total_line(i)
            if line is None: continue
            lines.append(line)
        return lines        
  
    
    def save(self, fname):
        with open(fname, "w") as f:
            for i in range(self.get_total_lines()):
                line = self.get_total_line(i, rev=False)
                if line:
                    f.write(line)

                    
@bp.route('/jou/log_<string:log>/', methods=('GET', 'POST'))
@login_required
def log_journal(log):
    if not request.args.get('path'):
        fname = f'%s/{log}.log' % os.environ["ZIEM_PATH_LOGS"]
        
    else:
        fname = request.args.get('path')
        log = fname
        
    if not os.path.isfile(fname): 
        flash(f'Журнал "{log}" не найден')
        return render_template('base.html')
    
    
    page = 1 if not request.args.get('page') else int(request.args.get('page'))
    per = 25 if not request.args.get('per') else int(request.args.get('per'))
    search = '' if not request.args.get('s') else request.args.get('s')
    a = '' if not request.args.get('a') else request.args.get('a')
    b = '' if not request.args.get('b') else request.args.get('b')
    journal = Journal(fname, search, a, b)
    
    if journal.nav is None:
        flash(f'Ошибка чтения журнала "{log}"')
        return render_template('base.html')
    
    if page > journal.get_total_pages(per):
        page = 1
        
    return render_template('jou/index.html', 
                           total=journal.get_total_lines(),
                           pages=journal.get_total_pages(per),
                           items=journal.items(page, per),
                           page=page,
                           per=per,
                           search=search,
                           name=logs_dict().get(log, log.title()),
                           journal=log,
                           start=a,
                           end=b
                           )



@bp.route('/jou/save_<string:log>/')
@login_required
def save_journal(log):
    fname = f'%s/{log}.log' % os.environ["ZIEM_PATH_LOGS"]
    search = '' if not request.args.get('s') else request.args.get('s')
    a = '' if not request.args.get('a') else request.args.get('a')
    b = '' if not request.args.get('b') else request.args.get('b')
    journal = Journal(fname, search, a, b)
    time = datetime.now().strftime("%Y%m%d-%H_%M_%S")
    s = re.sub(r'[^\w\s-]', '', search.lower())
    s = re.sub(r'[-\s]+', '-', s).strip('-_')[:25]
    if search: s = '-'+s
    fname = f'{time}-{log}{s}'
    path = f"%s/{fname}.log" % os.environ["ZIEM_PATH_TMP"]
    tar_file = f"%s/{fname}.tar.bz2" % os.environ["ZIEM_PATH_TMP"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    journal.save(path)
    with tarfile.open(tar_file, 'w:bz2') as tar:
        tar.add(path, os.path.basename(fname)+'.log')
    return send_file(tar_file, as_attachment=True, attachment_filename=f'{fname}.tar.bz2')


def logs_dict():
    
    logs = {
            'bks':   'Обновления справочников',
            'agent': 'Работы агента ЗИЕМ',
            'user':  'WEB-запросов',
            'ziem':  'Работы ядра опроса',
            'post':  'Отправки инцидентов и сообщений',
            'web':   'Действий пользователя',
            }
    
    for k in list(logs):
        fname = f'%s/{k}.log' % os.environ["ZIEM_PATH_LOGS"]
        if not os.path.isfile(fname):
            del logs[k]
            
    return logs


def menu_logs():
    items = logs_dict()
    if not len(items): return ''
    menu = ''
    bp = 'jou'
    name = 'Журналы'
    icon = 'fa-solid fa-pen'
    for k, v in items.items():
        href = f'/{bp}/log_{k}/'
        menu += f'''
                <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                  <li>
                    <a 
                      class="nav-link rounded" 
                      href="{href}"
                      data-menu="{bp}"
                      aria-current="{href}">
                      {v}
                    </a>
                  </li>
                </ul>
                '''
    if '' == menu: return '';    
    return f'''<li class="mb-1">
              <button class="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse" data-bs-target="#{bp}-collapse" aria-expanded="false" id="{bp}">
                <i class="{icon} mx-3 fa-fw text-secondary"></i>
                {name}
              </button>
              <div class="collapse ps-2" id="{bp}-collapse">
                {menu}
              </div>
            </li>
            '''



def format_line(item):
    # 70737 user.log 10-25-2022 12:38:53~INFO~192.168.154.107 - - [25/Oct/2022 12:38:53] "GET /static/images/favicon.png HTTP/1.1" 200 -
    data = {'raw': item}
    try:# ['56076 post.log  ', ' 2022-10-25 11:56:14,572 ', ' ERROR ', ' 1203 ', ' POST-TRANSMITTER ', ' [335] post.run: Ошибка отправки в Sender : TimeoutError()\n']
        a = item.split('~')
        n, fname, date, time= a[0].split(' ')[:4]
        raw = ' '.join(a[2:])
        try: 
            raw = Markup(yaml.dump(json.loads(raw), allow_unicode=True).replace('\n', '<br/>').replace('\t', '    '))
        except: pass
        data = {
            'line': n.strip(),
            'log': fname.strip(),
            'date': date.strip(),
            'time': time.strip(),
            'lvl': a[1].strip().upper(),
            'raw': raw,
        }
        
    except Exception as e: 
        a = item.split(' ')
        data = {
            'line': a[0].strip(),
            'log': a[1].strip(),
            'raw': ' '.join(a[2:]),
        }
 
    return render_template ('jou/item.html', item=data) 
