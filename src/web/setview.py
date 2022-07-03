"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
"""

import json
import time
import os
import tarfile
#import importlib.metadata
from bson.objectid import ObjectId

from re import search
from time import sleep
from datetime import datetime
from datetime import timedelta
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from flask import send_file

from .authview import login_required
from .baseview import get_col, write_log, get_rawdb, get_choice
from .setform import SettingForm, JsonForm, SearchForm, MapsearchForm

from bson.json_util import dumps
from flask import jsonify

bp = Blueprint('set', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('set.status', period='minute'))

@bp.route('/set/setting/', methods=('GET', 'POST'))
@login_required
def setting():
    col = get_col('set')
    doc = col.find_one({'name': 'setting'})
    form = SettingForm(data=doc)
    version_cur = 3#importlib.metadata.version('ziem')
    return render_template('set/setting.html', form=form, version=version_cur)

@bp.route('/set/setting/post', methods=('GET', 'POST'))
@login_required
def post_setting():
    col = get_col('set')
    doc = col.find_one({'name': 'setting'})
    form = SettingForm()
    if form.validate_on_submit():
        data = form.data
        data['name'] = 'setting'
        del data['csrf_token']
        msg = {} 
        for k, v in data.items():
            if doc:
                if k in doc:
                    if v != doc[k]:
                        msg[k] = [doc[k], v]
        col.replace_one(
            {'name': 'setting'}, 
            data,
            upsert=True)
        write_log(2112, src='SET', msg=msg)
        del data['name']
        with open('/var/opt/ziem/conf/settings.json', "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return 'Настройки сохранены', 200

@bp.route('/set/log_system/', methods=('GET', 'POST'))
@login_required
def log_system():
    data = []
    form = SearchForm()
    with open('/var/log/ziem/ziem.log', 'r') as f:
        data_raw = f.readlines()
    for d_raw in data_raw:
        if len(d_raw) > 1:
            if d_raw[0] == ' ':
                d = d_raw.split(' ~ ')
                if len(d) > 5:
                    if d[2] == 'ERROR':
                        data.append({
                            'time': d[1],
                            'code': d[3],
                            'src': d[4],
                            'raw': d[5],
                        })
    data.reverse()    
    return render_template('set/log_system.html', form=form, data=data)


@bp.route('/set/save_logsystem/')
@login_required
def save_logsystem():
    LOG = "/var/log/ziem/ziem.log"
    #with open(LOG, 'r') as f:
    #    data = f.read()
    PATH = "/var/opt/ziem/tmp/rep"
    file = PATH + "/logziem.log"
    tar_file = PATH + "/save.tar.bz2"
    os.makedirs(PATH, exist_ok=True)
    with tarfile.open(tar_file, 'w:bz2') as tar:
        tar.add(LOG, os.path.basename(file))
    return send_file(tar_file, as_attachment=True, attachment_filename='logziem.tar.bz2')

@bp.route('/set/log_post/', methods=('GET', 'POST'))
@login_required
def log_post():
    data = []
    form = SearchForm()
    with open('/var/log/ziem/post.log', 'r') as f:
        data_raw = f.readlines()
    for d_raw in data_raw:
        if len(d_raw) > 1:
            if d_raw[0] == ' ':
                d = d_raw.split(' ~ ')
                if len(d) > 5:
                    if d[2] == 'ERROR':
                        data.append({
                            'time': d[1],
                            'code': d[3],
                            'src': d[4],
                            'raw': d[5],
                        })
    data.reverse()    
    return render_template('set/log_post.html', form=form, data=data)

@bp.route('/set/save_post/')
@login_required
def save_post():
    LOG = "/var/log/ziem/post.log"
    #with open(LOG, 'r') as f:
    #    data = f.read()
    PATH = "/var/opt/ziem/tmp/rep"
    file = PATH + "/logpost.log"
    tar_file = PATH + "/save.tar.bz2"
    os.makedirs(PATH, exist_ok=True)
    with tarfile.open(tar_file, 'w:bz2') as tar:
        tar.add(LOG, os.path.basename(file))
    return send_file(tar_file, as_attachment=True, attachment_filename='logpost.tar.bz2')

@bp.route('/set/log_user/')
@login_required
def log_user():
    time_end = datetime.now() + timedelta(hours=1)
    time_start = datetime.now() - timedelta(days=1)
    form = SearchForm(date_start=time_start)
    return render_template('set/log_user.html', form=form)

@bp.route('/set/get_loguser/', methods=('GET', 'POST'))
@login_required
def get_loguser():
    data = []
    form = SearchForm()
    meta_field = form.meta_field.data
    date_start = form.date_start.data
    date_end = form.date_end.data
    if not date_start:
        date_start = datetime.now() - timedelta(days=1)
    if not date_end:
        date_end = datetime.now() + timedelta(hours=1)
    max_count = 1000
    col = get_col('logweb')
    query = {"$and":[ 
        {'time': {'$gte': date_start}}, 
        {'time': {'$lte': date_end}} 
    ]}
    if meta_field:
        query["$and"].append({'src': meta_field})
    data = [ x for x in col.find(query).sort('time',-1).limit(max_count) ]
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/set/status/<string:period>')
@login_required
def status(period):
    # информация о системе
    col = get_col('report')
    if period == 'minute':
        time = datetime.now() - timedelta(hours=12)
    elif period == 'hour':
        time = datetime.now() - timedelta(days=1)
    elif period == 'day':
        time = datetime.now() - timedelta(days=60)
    pipeline = get_pipeline(period, time)
    reports = col.aggregate(pipeline)
    data = check_dataraw(reports, period)
    stat = {
        'log': get_col('log_rule').count(),
        'nor': get_col('nor_rule').count(),
        'corfast': get_col('cor_fastrule').count(),
        'cordeep': get_col('cor_deeprule').count(),
        'tax': get_col('opt_tax').count(),
        'protocol': get_col('opt_protocol').count(),
        'profile': get_col('opt_profile').count(),
        'field': get_col('opt_field').count(),
    }
    status = False
    return render_template('set/status.html', data=data, 
                           stat=stat, status=status)

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
    if period == 'minute':
        pipeline[2]['$group']['_id']['date']['day'] = '$date.day'
        pipeline[2]['$group']['_id']['date']['hour'] = '$date.hour'
        pipeline[2]['$group']['_id']['date']['control'] = '$date.minute'
    elif period == 'hour':
        pipeline[2]['$group']['_id']['date']['day'] = '$date.day'
        pipeline[2]['$group']['_id']['date']['control'] = '$date.hour'
    elif period == 'day':
        pipeline[2]['$group']['_id']['date']['control'] = '$date.day'
    return pipeline

def check_dataraw(reports, period):
    data = []
    data_raw = [ x for x in reports]
    if len(data_raw) > 1:
        i = data_raw[0]['_id']['date']['control']
        raw0 = { x for x in data_raw[0] }
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

@bp.route('/set/service_control/<string:action>', methods=('GET', 'POST'))
@login_required
def service_control(action):
    try:
        if action == 'restart':
            os.system('sudo systemctl restart ziemwebd')
            write_log(2119, src='SET')
    except:
        pass
    return ('', 204)

@bp.route('/set/json/', methods=('GET', 'POST'))
@login_required
def set_json():
    data = get_currentconf()
    form = JsonForm(data={'jdata': data})
    form.backup.choices = get_choice('backup')
    if form.validate_on_submit():
        db = get_rawdb()
        data = json.loads(form.jdata.data)
        for col_name, data_col in data.items():
            col = get_col(col_name)
            data_old = {}
            for data in col.find():
                data_old[data['name']] = data
            db[col_name].drop()
            for d in data_col:
                msg = {
                    'module': col_name, 
                    'rule': d['name'],
                }
                if d['name'] in data_old:
                    for k, v in d.items():
                        if k in data_old[d['name']]:
                            doc_old = data_old[d['name']]
                            if v != doc_old[k]:
                                if isinstance(v, list):
                                    for val in v:
                                        if val not in doc_old[k]:
                                            msg['new_value'] = val
                                            msg['old_list'] = doc_old[k]
                                else:
                                    msg[k] = [doc_old[k], v]
                                write_log(2114, src='SET', msg=msg)
                else:
                    msg['new_value'] = d
                    write_log(2113, src='SET', msg=msg)
                d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                col.insert_one(d)
        col_backup()
        return redirect(url_for('set.index'))
    return render_template('set/set_json.html', form=form)

def get_currentconf():
    cols = get_colllection()
    data = {}
    for k,v in cols.items():
        data_col = [ x for x in v.find() ]
        for d in data_col:
            if '_id' in d:
                del d['_id']
            if 'pubdate' in d:
                del d['pubdate']
        data[k] = data_col
    return json.dumps(data, indent=4, ensure_ascii=False)

@bp.route('/set/get_backup/<string:id>')
@login_required
def get_backup(id):
    if id == 'current':
        return get_currentconf()
    else:
        col = get_col('backup')
        doc = col.find_one({ '_id': ObjectId(id) })['conf']
        for value in doc.values():
            for d in value:
                if '_id' in d:
                    del d['_id']
                if 'pubdate' in doc:
                    del d['pubdate']
        return json.dumps(doc, indent=4, ensure_ascii=False)

@bp.route('/set/get_conf/<string:id>')
@login_required
def get_conf(id):
    if id == 'set':
        return get_currentconf()
    else:
        col = get_col('backup')
        doc = col.find_one({ '_id': ObjectId(id) })['conf']
        for value in doc.values():
            for d in value:
                if '_id' in d:
                    del d['_id']
                if 'pubdate' in doc:
                    del d['pubdate']
        return json.dumps(doc, indent=4, ensure_ascii=False)

@bp.route('/set/rule/save')
@login_required
def set_save():
    cols = get_colllection()
    data = {}
    PATH_set = "/var/opt/ziem/tmp"
    os.makedirs(PATH_set, exist_ok=True)
    file_set = PATH_set + '/' + 'ziem.json'
    tar_file = PATH_set + '/ziem_conf.tar.bz2'
    with tarfile.open(tar_file, 'w:bz2') as tar:
        for k,v in cols.items():
            data_col = [ x for x in v.find() ]
            file = PATH_set + '/' + k + '.json'
            for d in data_col:
                if '_id' in d:
                    del d['_id']
                if 'pubdate' in d:
                    del d['pubdate']
            with open(file, "w") as f:
                json.dump(data_col, f, indent=4, ensure_ascii=False)
            tar.add(file, k + '.json')
            data[k] = data_col
        with open(file_set, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        tar.add(file_set, 'ziem.json')
    file_name = 'ziem_' + datetime.now().strftime('%Y-%m-%d') + '.tar.bz2'
    write_log(2115, src='SET')
    return send_file(tar_file, as_attachment=True, attachment_filename=file_name)

def get_colllection():
    return {
        'log_rule': get_col('log_rule'),
        'nor_rule': get_col('nor_rule'),
        'cor_fastrule': get_col('cor_fastrule'),
        'cor_deeprule': get_col('cor_deeprule'),
        'opt_profile': get_col('opt_profile'),
        'opt_protocol': get_col('opt_protocol'),
        'opt_taxmain': get_col('opt_taxmain'),
        'opt_taxobject': get_col('opt_taxobject'),
        'opt_taxaction': get_col('opt_taxaction'),
        'opt_field': get_col('opt_field'),
        'opt_crit': get_col('opt_crit'),
        'opt_clas': get_col('opt_clas'),
        'set': get_col('set'),
    }    

@bp.route('/set/get_objcolllection/<string:obj>')
@login_required
def get_objcolllection(obj):
    cols = get_colllection()
    data = {}
    for k, v in cols:
        if 'opt_' in k:
            data_col = [ x for x in v.find() ]
            for d in data_col:
                del d[k]
    data = {
        'log_rule': [ x for x in get_col('log_rule').find({'obj':obj}) ],
        'nor_rule': [ x for x in get_col('nor_rule').find({'obj':obj}) ],
        'cor_fastrule': [ x for x in get_col('cor_fastrule').find({'obj':obj}) ],
        'cor_deeprule': [ x for x in get_col('cor_deeprule').find({'obj':obj}) ],
        'opt_profile': [ x for x in get_col('opt_profile').find() ],
        'opt_protocol': [ x for x in get_col('opt_protocol').find() ],
        'opt_taxset': [ x for x in get_col('opt_taxset').find() ],
        'opt_taxobject': [ x for x in get_col('opt_taxobject').find() ],
        'opt_taxaction': [ x for x in get_col('opt_taxaction').find() ],
        'opt_field': [ x for x in get_col('opt_field').find() ],
        'opt_crit': [ x for x in get_col('opt_crit').find() ],
        'opt_clas': [ x for x in get_col('opt_clas').find() ],
        'set': [ x for x in get_col('set').find({'obj':obj}) ],
    }    
    return json.dumps(data, indent=4, ensure_ascii=False)


def col_backup():
    col = get_col('backup')
    cols = get_colllection()
    data = { 
        'time': datetime.now().strftime("%Y-%m-%d"),
        'conf': {},
    }
    for k, v in cols.items():
        data['conf'][k] = [ x for x in v.find() ]
    col.insert_one(data)
    if col.count() > 30:
        doc = col.delete_one({})

@bp.route('/set/version_update')
@login_required
def version_update():
    col = get_col('set')
    doc = col.find_one({'name': 'setting'})
    ip = "127.0.0.1"
    port = 8000
    if 'repo_ip' in doc:
        ip = doc['repo_ip']
    if 'repo_port' in doc:
        port = doc['repo_port']
    if ip and port:
        repo = ip + ':' + port
        url = 'http://' + repo + '/ziem/'
        cmd = ('sudo /opt/ziem/venv/bin/python -m pip install '\
               '--trusted-host '\
               + ip +
               ' --index-url '\
               'http://' + repo + '/ ziem -U')
        os.system(cmd)
        os.system('sudo systemctl restart ziemwebd')
        os.system('sudo systemctl restart ziemcored')
        os.system('sudo systemctl restart ziempostd')
        write_log(2120, src='SET')
        return ('Система обновлена', 200)
    return ('Ошибка обновления', 400)


@bp.route('/set/map', methods=('GET', 'POST'))
@login_required
def map():
    col = get_col('log_rule')
    rules = []
    for rule in col.find().sort("name"):
        if rule['name'] == 'NET_Netmap':
            continue
        if 'active' in rule:
            if rule['active']:
                r = {
                    'name': rule['name'],
                    'ip': rule['ip'],
                }
                rules.append(r)
    col = get_col('alerts')
    time_end = datetime.now() + timedelta(minutes=10)
    time_start = datetime.now() - timedelta(minutes=60)
    query = {"$and":[ 
        {'time': {'$gte': time_start}}, 
        {'time': {'$lte': time_end}} 
    ]}
    form = MapsearchForm(
        date_start=time_start,
        time_start=time_start,
        date_end=time_end,
        time_end=time_end,
    )
    if form.validate_on_submit():
        search = form.search.data
        dt_start = datetime.combine(form.date_start.data, form.time_start.data)
        dt_end = datetime.combine(form.date_end.data, form.time_end.data)
        query = {"$and":[ 
            {'time': {'$gte': dt_start}}, 
            {'time': {'$lte': dt_end}} 
        ]}
        for rule in rules:
            query["$and"].append({'node': rule['name']})
            data = [ x for x in col.find(query).sort('time',-1).limit(100000) ]
            rule['count'] = len(data)
            if rule['count'] > 0:
                rule['lastdate'] = data[0]['time']
        return render_template('set/map.html', form=form, data=rules)
    for rule in rules:
        query["$and"].append({'node': rule['name']})
        data = [ x for x in col.find(query).sort('time',-1).limit(100000) ]
        rule['count'] = len(data)
        if rule['count'] > 0:
            rule['lastdate'] = data[0]['time']
    return render_template('set/map.html', form=form, data=rules)

@bp.route('/set/install')
@login_required
def install():
    conf_install()
    col_backup()
    write_log(2107, src='SET')
    os.system('sudo systemctl restart ziemcored')
    write_log(2119, src='SET')
    time.sleep(1)
    return ('', 204)

def conf_install():
    db = get_rawdb()
    col = db['log_rule']
    data = []
    data_raw = [ x for x in col.find({'obj':'set'}) ]
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
    data = [ x for x in col.find({'obj':'set'}) ]
    for d in data:
        del d['_id']
        del d['pubdate']
        d['norm'] = 'NORm_1'
        for event in d['events']:
            regex = { x['field']:x['value'] for x in event['regex'] }
            event['regex'] = regex
        d['logs'] = []
        col = db['log_rule']
        for log_rule in col.find():
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
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    col = db['cor_fastrule']
    data = [ x for x in col.find({'obj':'set'}) ]
    for d in data:
        del d['_id']
        del d['pubdate']
    file = '/var/opt/ziem/conf/cor_fastrule.json'
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    col = db['cor_deeprule']
    data = [ x for x in col.find({'obj':'set'}) ]
    for d in data:
        del d['_id']
        del d['pubdate']
    file = '/var/opt/ziem/conf/cor_deeprule.json'
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
