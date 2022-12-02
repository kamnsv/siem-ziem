"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
        Kamnev Sergey
"""

import json
import time
import os
import tarfile
#import importlib.metadata
import pkg_resources
from bson.objectid import ObjectId

import psutil
from re import search
from time import sleep
from datetime import datetime
from datetime import timedelta
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from flask import send_file

from .setview import col_backup, get_colllection
from .authview import login_required
from .baseview import get_col, write_log, get_rawdb, get_choice
from .mainform import SearchForm

from bson.json_util import dumps
from flask import jsonify
import pkg_resources

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    
    if '1' == os.environ["ZIEM_CENTER"]:
        return redirect(url_for('obj.rule'))
    
    return redirect(url_for('main.status', period='minute'))

@bp.route('/main/status/<string:period>')
@login_required
def status(period):
    # информация о системе
    data = {}
    query = {"$and":[{'obj':'main'},{'active':True}]}
    data['log_count'] = get_col('log_rule').find(query).count()
    data['version'] = get_version()#pkg_resources.get_distribution('ziem').version
    check_logerror(data)
    status = os.popen('systemctl is-active ziemcored').read().strip() # без \n

    data['status'] = {
        'inactive': 'Не активен',
        'activating': 'Ошибка активации',
        'active': 'Активен',
    }.get(status, status) 
    
    return render_template('main/status.html', data=data)

def check_logerror(data):
    with open('/var/log/ziem/ziem.log', 'r') as f:
        data_raw = f.readlines()
    data_raw.reverse()    
    error_count = 0
    flow_control = {}
    grouped_errors = {}
    for d_raw in data_raw:
        if 'core started' in d_raw:
            break
        elif d_raw:
            d = d_raw.split(' ~ ')
            if len(d) > 4:
                if 'ERROR' == d[1]:
                    error_count += 1
                if '1212' == d[2]:
                    if d[3] in flow_control:
                        flow_control[d[4]] += 1
                    else:
                        flow_control[d[4]] = 1
                if d[4] in grouped_errors:
                    grouped_errors[d[4]] += 1
                else:
                    grouped_errors[d[4]] = 1
    data['flow_control'] = flow_control
    data['grouped_errors'] = grouped_errors
    data['error_count'] = error_count
    
@bp.route('/main/get_stats')
@login_required
def get_stats():
    period = 'minute'
    data = {
        'label': [],
        'inc_data': [],
        'event_data': [],
        'alert_data': [],
    }
    col = get_col('report')
    days = '1' if request.args.get('days') is None else request.args.get('days')
    days = int(days) if days.isdigit() else 1
    time = datetime.now() - timedelta(days=days)
    pipeline = get_pipeline(period, time)
    reports = col.aggregate(pipeline)
    raw_data = check_dataraw(reports, period)
    for d in raw_data:
        data['label'].append(d['_id']['date']['control'])
        data['inc_data'].append(d['inc'])
        data['event_data'].append(d['event'])
        data['alert_data'].append(d['alert'])
    return json.dumps(data, default=str, ensure_ascii=False)

@bp.route('/main/get_statscpu')
@login_required
def get_statscpu():
    period = 'minute'
    data = {
        'label': [],
        'cpu_data': [],
        'mem_data': [],
        'hdd_data': [],
    }
    col = get_col('report')
    days = '1' if request.args.get('days') is None else request.args.get('days')
    days = int(days) if days.isdigit() else 1
    time = datetime.now() - timedelta(days=days)
    pipeline = get_pipeline(period, time)
    reports = col.aggregate(pipeline)
    raw_data = check_dataraw(reports, period)
    for d in raw_data:
        data['label'].append(d['_id']['date']['control'])
        data['cpu_data'].append(d['cpu'])
        data['mem_data'].append(d['mem'])
        data['hdd_data'].append(d['hdd'])
    return json.dumps(data, default=str, ensure_ascii=False)

def get_pipeline(period, time):
    pipeline = [
        {
            '$match': { 
                'time': {'$gte': time}
            }
        },
        {
            '$project': {
                'date': {
                    '$dateToParts': { 
                        'date': '$time',
                     }
                },
                'ziem_mem': 1,
                'cpu_load': 1,
                'hdd_load': 1,
                'mem_load': 1,
                'count_alert': 1,
                'count_event': 1,
                'count_inc': 1,
                'count_error': 1,
            }
        },
        {
            '$group': {
                '_id': {
                    'date': {
                       'year': '$date.year',
                       'month': '$date.month',
                       'day': '$date.day',
                       'control': '$date.hour',
                    }
                },
                'ziem_mem': { '$avg': '$ziem_mem' },
                'cpu': { '$avg': '$cpu_load' },
                'hdd': { '$avg': '$hdd_load' },
                'mem': { '$avg': '$mem_load' },
                'alert': { '$sum': '$count_alert' },
                'event': { '$sum': '$count_event' },
                'inc': { '$sum': '$count_inc' },
                'error': { '$sum': '$count_error' },
            }
        },
        {
            '$sort' : { 
                '_id.date' : 1
            }
        },
    ]
    return pipeline

def check_dataraw(reports, period):
    data = []
    data_raw = [ x for x in reports]
    #print(data_raw)
    if len(data_raw) > 0:
        i = data_raw[0]['_id']['date']['control']
        #raw = { x for x in data_raw[0] }
        for d in data_raw:
            # search empty values, add '0' if no value at time
            if d['_id']['date']['control'] != i:
                while d['_id']['date']['control'] != i:
                    rep_clear = {}
                    rep_clear['_id'] = {}
                    rep_clear['_id']['date'] = { 
                        k:v for k,v in data_raw[0]['_id']['date'].items() 
                    }
                    rep_clear['ziem_mem'] = 0
                    rep_clear['cpu'] = 0
                    rep_clear['hdd'] = 0
                    rep_clear['mem'] = 0
                    rep_clear['alert'] = 0
                    rep_clear['event'] = 0
                    rep_clear['inc'] = 0
                    rep_clear['error'] = 0
                    rep_clear['_id']['date']['control'] = i
                    data.append(rep_clear)
                    i = inc_i(i, period, d)
            data.append(d)
            i = inc_i(i, period, d)
    return data

def inc_i(i, period, d):
    if period == 'minute':
        if i == 59:
            i = 0
        else:
            i += 1
    elif period == 'hour':
        if i == 23:
            i = 0
        else:
            i += 1
    elif period == 'day':
        if d['_id']['date']['month'] in [ 1, 3, 5, 6, 8, 10, 12] :
            days_month = 31
        elif d['_id']['date']['month'] == 2:
            days_month = 28
        else:
            days_month = 30
        if i == days_month:
            i = 0
        else:
            i += 1    
    return i

@bp.route('/main/service_control/<string:action>', methods=('GET', 'POST'))
@login_required
def service_control(action):
    try:
        if action == 'restart':
            os.system('sudo systemctl restart ziemcored')
            os.system('sudo systemctl restart ziempostd')
            time.sleep(3)
            write_log(2119, src='MAIN')
    except Exception as e:
        print(e)
        pass
    return ('Система перезапущена', 200)

@bp.route('/main/install')
@login_required
def install():
    try:
        conf_install()
        col_backup()
        os.system('sudo systemctl restart ziemcored')
        time.sleep(3)
        write_log(2107, src='MAIN')
        write_log(2119, src='MAIN')
    except Exception as e:
        print(e)
        return ('Ошибка установки правил:'+repr(e), 200)
    return ('Правила установлены', 200)

def conf_install():
    db = get_rawdb()
    col = db['log_rule']
    data = []
    data_raw = [ x for x in col.find({'obj':'main'}) ]
    col = db['log_cred']
    for d in data_raw:
        if 'active' in d:
            if d['active']:
                del d['_id']
                del d['pubdate']
                if d['login']:
                    cred = col.find_one({'name': d['login']})
                    if cred:
                        if 'pswd' in cred:
                            d['pswd'] = cred['pswd']
                d['logs'] = [ x['logname'] for x in d['logs'] ]
                data.append(d)
    file = '/var/opt/ziem/conf/log_rule.json'
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    col = db['nor_rule']
    data = [ x for x in col.find({'obj':'main'}) ]
    for d in data:
        del d['_id']
        del d['pubdate']
        d['alr_norm'] = 'NORm_1'
        for event in d['events']:
            regex = { x['field']:x['value'] for x in event['regex'] }
            event['regex'] = regex
        d['logs'] = []
        col = db['log_rule']
        for log_rule in col.find({'obj':'main'}):
            if 'active' not in log_rule:
                continue
            if log_rule['active']:
                for log in log_rule['logs']:
                    if log['normrule'] == d['name']:
                        if log['logname']:
                            d['logs'].append(log_rule['name'] + '-' + log['logname'])
                        else:
                            d['logs'].append(log_rule['name'] + '-' + log_rule['name'])
    file = '/var/opt/ziem/conf/nor_rule.json'
    data = [ d for d in data if d['logs'] or d['name'] == 'ZIEM_ZIEM']
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    col = db['cor_fastrule']
    data = [ x for x in col.find({'obj':'main'}) ]
    for d in data:
        del d['_id']
        del d['pubdate']
    file = '/var/opt/ziem/conf/cor_fastrule.json'
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    col = db['cor_deeprule']
    data = [ x for x in col.find({'obj':'main'}) ]
    for d in data:
        del d['_id']
        del d['pubdate']
    file = '/var/opt/ziem/conf/cor_deeprule.json'
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    col = db['opt_bks']
    for book in col.find():
        name = book['name']
        bks = db[f'bks_{name}']
        data = [ x for x in bks.find() ]
        for d in data:
            del d['_id']
        file = f'/var/opt/ziem/conf/bks_{name}.json'
        with open(file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

@bp.route('/main/logerror')
@login_required
def get_logerror():
    with open('/var/log/ziem/ziem.log', 'r') as f:
        data_raw = f.readlines()
    data_raw.reverse()    
    data = {}
    for d_raw in data_raw:
        if 'core started' in d_raw:
            break
        elif len(d_raw) > 1:
            d = d_raw.split(' ~ ')
            if len(d) > 4:
                if d[1] == 'ERROR':
                    error = d[3] + ' ' + d[4]
                    if error in data:
                        data[error] += 1
                    else:
                        data[error] = 1
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/main/get_flow')
@login_required
def get_flow():
    with open('/var/log/ziem/ziem.log', 'r') as f:
        data_raw = f.readlines()
    data_raw.reverse()    
    data = {}
    for d_raw in data_raw:
        if 'core started' in d_raw:
            break
        elif len(d_raw) > 1:
            d = d_raw.split(' ~ ')
            if len(d) > 4:
                    if d[2] == '1212':
                        log = d[4].split(':')[-1]
                        #print(d)
                        if log in data:
                            data[log] += 1
                        else:
                            data[log] = 1
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/main/get_dataerror')
@login_required
def get_dataerror():
    with open('/var/log/ziem/ziem.log', 'r') as f:
        data_raw = f.readlines()
    data_raw.reverse()    
    data = {}
    for d_raw in data_raw:
        if 'core started' in d_raw:
            break
        elif len(d_raw) > 1:
            d = d_raw.split(' ~ ')
            if len(d) > 4:
                if d[1] == 'ERROR':
                    if d[3] in data:
                        data[d[3]] += 1
                    else:
                        data[d[3]] = 1
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/main/get_protocols')
@login_required
def get_protocols():
    data = {}
    query = {"$and":[ 
        {'obj':'main'}, 
        {'active': True}, 
    ]}    
    protocols = [ x['protocol'] for x in get_col('log_rule').find(query) ]
    for protocol in protocols:
        if protocol in data:
            data[protocol] += 1
        else:
            data[protocol] = 1
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/main/get_incs')
@login_required
def get_incs():
    data = {}
    time = datetime.now() - timedelta(days=1)
    query = {'inc_time': {'$gte': time}}
    incs = [ x['inc_name'] for x in get_col('incs').find(query).limit(15) ]
    for inc in incs:
        if inc in data:
            data[inc] += 1
        else:
            data[inc] = 1
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/main/diag/')
@login_required
def diag():
    # информация о системе
    col = get_col('report')
    data = {}
    time = datetime.now() - timedelta(days=1)
    period='minute'
    pipeline = get_pipeline(period, time)
    reports = col.aggregate(pipeline)
    data['data_chart'] = check_dataraw(reports, period)
    data['mem'] = get_mem()
    data['hdd'] = get_hdd()
    data['cpu'] = get_cpu()
    data['version'], data['nameos'] = get_os()
    
    get_dbsize(data)
    return render_template('main/diag.html', data=data)

def get_os():
    v = os.popen('cat /etc/*release | grep VERSION_ID').read()
    if 'VERSION_ID' in v: v = v.split('=')[1][0:-1]
    n = os.popen('cat /etc/*release | grep ^NAME=').read()
    if 'NAME' in n: n = n.split('=')[1][1:-2]
    return v, n      

def get_dbsize(data):
    cmd = 'du -shS /var/lib/mongodb 2>/dev/null | cut -d "/" -f1'
    data['db_size'] = os.popen(cmd).read()
    data['count_alert'] = get_col('alerts').count()
    data['count_event'] = get_col('events').count()
    data['count_inc'] = get_col('incs').count()

@bp.route('/main/get_proc/')
@login_required
def get_proc():
    procs = list()
    for proc in psutil.process_iter():
        proc_data = proc.as_dict(attrs=['name', 'cpu_percent'])
        procs.append(proc_data)
    procs_sorted = sorted(procs, key=lambda proc: proc['cpu_percent'],
                          reverse=True)[:15]
    return { x['name']: x['cpu_percent']  for x in procs_sorted }

@bp.route('/main/get_parthdd/')
@login_required
def get_parthdd():
    return {
        'root': psutil.disk_usage('/').used,
        'home': psutil.disk_usage('/home').used,
        'var': psutil.disk_usage('/var').used,
        'var/log': psutil.disk_usage('/var/log').used,
        'var/log/audit': psutil.disk_usage('/var/log/audit').used,
        'tmp': psutil.disk_usage('/tmp').used,    }

@login_required
def get_cpu():
    # информация о процессоре
    return int(psutil.getloadavg()[2] / psutil.cpu_count() * 100)

@login_required
def get_mem():
    # информация о памяти
    mem = psutil.virtual_memory()
    return int((mem.total - mem.available)/mem.total * 100) 

@login_required
def get_hdd():
    # информация о жестком
    hdd_root = psutil.disk_usage('/')
    hdd_home = psutil.disk_usage('/home')
    hdd_var = psutil.disk_usage('/var')
    used = hdd_root.used + hdd_home.used + hdd_var.used
    total = hdd_root.total + hdd_home.total + hdd_var.total
    return int(used/total*100)

def get_version():
    return pkg_resources.get_distribution('ziem').version
    owd = os.getcwd()
    os.chdir('/opt/ziem')
    v = os.popen('git tag').read()
    os.chdir(owd)
    return v.strip()