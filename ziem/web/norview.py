"""
    ZIEM 

    Description:

    Author:
        Bengart Zakhar
"""

import os
import json
import re
import tarfile
from datetime import datetime
from bson.objectid import ObjectId

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from flask import send_file

from .baseview import get_col, write_log, get_choice
from .authview import login_required
from .norform import RuleForm, JsonForm, SearchForm
import sys
from ziem.core import Normaleizer

bp = Blueprint('nor', __name__)


@bp.route('/nor/rule/<string:obj>', methods=('GET', 'POST'))
@login_required
def rule(obj):
    form = SearchForm()
    form.selected_obj.choices = get_choice('obj')
    form.selected_obj.data = obj
    return render_template('nor/rule.html', form=form, obj=obj)

@bp.route('/nor/get_rule/<string:obj>', methods=('GET', 'POST'))
@login_required
def get_rule(obj):
    form = SearchForm()
    if form.selected_obj.data:
        obj = form.selected_obj.data
    data = check_rule(obj)
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

def check_rule(obj):
    col = get_col('nor_rule')
    if obj == None: obj = 'main'
    data_main = { x['name']:x for x in col.find({'obj':'main'}) }
    data = { x['name']:x for x in col.find().sort("name") if x['obj'] == obj }
    data_miss = [ x for x in data_main if x not in data ]
    data_search = []
    for d in data_miss:
        data_main[d]['diff'] = 'miss'
        data_search.append(data_main[d])
    for d in data:
        if data[d]['name'] not in data_main:
            data[d]['diff'] = 'new'
        else:
            del data[d]['obj']
            d_id = data[d]['_id']
            del data[d]['_id']
            del data_main[data[d]['name']]['obj']
            del data_main[data[d]['name']]['_id']
            for k, v in data[d].items():
                if k in data_main[data[d]['name']]:
                    if (v == data_main[data[d]['name']][k] or
                        k == 'pubdate'):
                        diff = False
                    else:
                        diff = 'changed'
                        break
            data[d]['diff'] = diff
            data[d]['_id'] = d_id
        data_search.append(data[d])
    return data_search

@bp.route('/nor/rule/add', methods=('GET', 'POST'))
@login_required
def rule_add():
    col = get_col('nor_rule')
    form = RuleForm()
    form.obj.choices = get_choice('obj')
    form.profile.choices = get_choice('profile')
    form.tax_main.choices = get_choice('tax_main')
    for event in form.events:
        event.tax_object.choices = get_choice('tax_object')
        event.tax_action.choices = get_choice('tax_action')
        for regex in event.regex:
            regex.field.choices = get_choice('field')
    if form.validate_on_submit():
        data = form.data
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        del data['csrf_token']
        col.insert_one(data)
        write_log(2103, src='NOR', msg={'rule':  data['name']} )
        return redirect(url_for('nor.rule', obj=data['obj']))
    url = '/nor/rule/add'
    return render_template('nor/rule_edit.html', form=form, url=url, obj='main', diff='')

@bp.route('/nor/rule/<string:id>/edit', methods=('GET', 'POST'))
@login_required
def rule_edit(id):
    col = get_col('nor_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    form = RuleForm(data=doc)
    form.obj.choices = get_choice('obj')
    form.profile.choices = get_choice('profile')
    form.tax_main.choices = get_choice('tax_main')
    for event in form.events:
        event.tax_object.choices = get_choice('tax_object')
        event.tax_action.choices = get_choice('tax_action')
        for regex in event.regex:
            regex.field.choices = get_choice('field')
    if form.validate_on_submit():
        data = form.data
        msg = { 
            'rule': data['name'] 
        }
        data['events'] = [ x for x in data['events'] if x['string'] ]
        del data['csrf_token']
        for event in data['events']:
            event['regex'] = [ x for x in event['regex'] if x['value'] ]
        """
        for k, v in data.items():
            if k in doc:
                if v != doc[k]:
                    if isinstance(v, list):
                        for val in v:
                            if val not in doc[k]:
                                msg['new_value'] = val
                                msg['old_list'] = doc[k]
                    else:
                        msg[k] = [doc[k], v]
        """
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        col.replace_one(
            {'_id': ObjectId(id)}, 
            data)
        get_col('nor_rule').update_many(
            {'name': doc['name']},
            { '$set': {'name': data['name'], 'desc': data['desc'] }}
        )
        write_log(2104, src='NOR', msg=msg )
        return redirect(url_for('nor.rule', obj=doc['obj']))
    diff = diff_rule(doc, col)
    return render_template('nor/rule_edit.html', form=form, diff=diff, obj=doc['obj'])

def diff_rule(doc, col):
    doc_main = col.find_one({'$and': [{'obj':'main'}, {'name':doc['name']}]})
    diff = {}
    if doc_main:
        for d in doc:
            if d == 'events':
                for index, event in enumerate(doc['events']):
                    if 'events' in doc_main:
                        for field in event:
                            if field in doc_main['events'][index]:
                                if event[field] != doc_main['events'][index][field]:
                                    diff['events-' + str(index) + '-' + field] = doc_main['events'][index][field]
                            else:
                                diff['events-' + str(index) + '-' + field] = doc_main['events'][index][field]
            elif d not in ('obj', 'pubdate', '_id'):
                if d in doc_main:
                    if doc[d] != doc_main[d]:
                        diff[d] = doc_main[d]
    return diff

@bp.route('/nor/rule/<string:id>/copy')
@login_required
def rule_copy(id):
    col = get_col('nor_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    doc['name'] = doc['name'] + '_copy'
    del doc['_id']
    doc['pubdate'] = datetime.now().strftime("%Y-%m-%d")
    col.insert_one(doc)
    write_log(2105, src='NOR', msg={'rule':  doc['name']} )
    data = {
        'text': 'Правило скопировано: ' + doc['name'],
        'doc': doc,
    }
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/nor/rule/<string:id>/del')
@login_required
def rule_del(id):
    col = get_col('nor_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    col.delete_one( {'_id': ObjectId(id)} )
    write_log(2106, src='NOR', msg={'rule':  doc['name']} )
    return 'Правило удалено: ' + doc['name']

@bp.route('/nor/rule/<string:id>/sync/<string:obj>')
@login_required
def rule_sync(id, obj):
    col = get_col('nor_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    if doc['obj'] == 'main':
        del doc['_id']
        doc['obj'] = obj
        col.insert_one(doc)
        write_log(2103, src='NOR', msg={'rule':  doc['name']} )
    else:
        new_doc = col.find_one({'$and': [{'name': doc['name']}, {'obj':'main'}]})
        if new_doc:
            col.delete_one( {'_id': ObjectId(id)} )
            del new_doc['_id']
            new_doc['obj'] = obj
            col.insert_one(new_doc)
            write_log(2103, src='NOR', msg={'rule':  new_doc['name']} )
    return 'Правило синхронизировано: ' + doc['name']

@bp.route('/nor/rule/json', methods=('GET', 'POST'))
@login_required
def rule_json():
    col = get_col('nor_rule')
    data = get_currentconf(col)
    print(data)
    form = JsonForm(data={'jdata': data})
    form.obj.choices = get_choice('obj')
    form.backup.choices = get_choice('backup')
    if form.validate_on_submit():
        data = json.loads(form.jdata.data)
        obj = form.obj.data
        for d in data:
            if 'obj' in d:
                if d['obj'] != obj:
                    continue
            msg = { 
                'rule': d['name'] 
            }
            doc_old = col.find_one({'name': d['name'], 'obj': obj})
            if doc_old:
                for k, v in d.items():
                    if k in doc_old:
                        if v != doc_old[k]:
                            if isinstance(v, list):
                                for val in v:
                                    if val not in doc_old[k]:
                                        msg['new_value'] = val
                                        msg['old_value'] = doc_old[k]
                            else:
                                msg[k] = [doc_old[k], v]
                if len(msg) > 1:
                    d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                    col.replace_one(
                        {'name': d['name'], 'obj': obj}, d)
                    write_log(2104, src='NOR', msg=msg)
            else:
                d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                d['obj'] = obj
                col.insert_one(d)
                write_log(2103, src='NOR', msg=msg )
        return redirect(url_for('nor.rule', obj='main'))
    return render_template('nor/rule_json.html', form=form)

def get_currentconf(col):
    data = [ x for x in col.find() ]
    for d in data:
        del d['_id']
        del d['pubdate']
    return json.dumps(data, indent=4, ensure_ascii=False)

@bp.route('/nor/get_backup/<string:col>/<string:id>')
@login_required
def get_backup(col, id):
    if id == 'current':
        return get_currentconf(get_col(col))
    else:
        doc = get_col('backup').find_one({ '_id': ObjectId(id) })['conf'][col]
        for d in doc:
            if '_id' in d:
                del d['_id']
            if 'name' in d:
                del d['pubdate']
        return json.dumps(doc, indent=4, ensure_ascii=False)

@bp.route('/nor/rule/save')
@login_required
def rule_save():
    col = get_col('nor_rule')
    data = [ x for x in col.find() ]
    PATH = "/var/opt/ziem/tmp/nor"
    file = PATH + '/nor_rule.json'
    tar_file = PATH + '/nor_rule.tar.bz2'
    os.makedirs(PATH, exist_ok=True)
    with tarfile.open(tar_file, 'w:bz2') as tar:
        for d in data:
            file_rule = PATH + '/' + d['name'] + '.json'
            del d['_id']
            del d['pubdate']
            with open(file_rule, "w") as f:
                json.dump(d, f, indent=4, ensure_ascii=False)
            tar.add(file_rule, os.path.basename(file_rule))
        with open(file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        tar.add(file, os.path.basename(file))
    write_log(2108, src='NOR')
    return send_file(tar_file, as_attachment=True, attachment_filename='nor_rule.tar.bz2')

@bp.route('/nor/rule/<string:id>/tax')
@login_required
def tax_view(id):
    # просмотр испльзуемой/неиспользуемой таксономии в правиле
    col = get_col('nor_rule')
    rule = col.find_one({'_id': ObjectId(id)})
    fast_taxes_raw = get_col('cor_fastrule').find({'tax_main':rule['tax_main']})
    data = dict()
    taxes = []
    taxes_unused = []
    deep_taxes = []
    for tax in fast_taxes_raw:
        find = False
        if tax['tax_object'] and tax['tax_action'] and tax['tax_main']:
            for event in rule['events']:
                if event['tax_object'] and event['tax_action']:
                    if (tax['tax_object'] == event['tax_object'] and
                        tax['tax_action'] == event['tax_action']):
                        find = True
                        break
            t = {
                'tax_main': tax['tax_main'],
                'tax_object': tax['tax_object'],
                'tax_action': tax['tax_action'],
                'name': tax['name'],
                'desc': tax['desc'],
                'find': find,
                }
            if t not in taxes:
                taxes.append(t)
    deep_taxes_raw = get_col('cor_deeprule').find()
    for deeprule in deep_taxes_raw:
        for tax in deeprule['events']:
            if tax['tax_main'] == rule['tax_main']:
                find = False
                for event in rule['events']:
                    if event['tax_object'] and event['tax_action']:
                        if (tax['tax_object'] == event['tax_object'] and
                            tax['tax_action'] == event['tax_action']):
                            find = True
                            break
                t = {
                    'tax_main': tax['tax_main'],
                    'tax_object': tax['tax_object'],
                    'tax_action': tax['tax_action'],
                    'name': deeprule['name'],
                    'desc': deeprule['desc'],
                    'find': find,
                    }
                if t not in taxes:
                    taxes.append(t)
    for event in rule['events']:
        if event['tax_object'] and event['tax_action']:
            find = False
            for tax in taxes:
                if event['tax_object'] and event['tax_action']:
                    if (tax['tax_object'] == event['tax_object'] and
                        tax['tax_action'] == event['tax_action']):
                        find = True
                        break
            if not find:
                t = {
                    'tax_object': event['tax_object'],
                    'tax_action': event['tax_action'],
                    'alr_msg': event['alr_msg'],
                    }
                taxes_unused.append(t)
    data = {
        'used_taxes': [ x for x in taxes if x['find'] ],
        'miss_taxes': [ x for x in taxes if not x['find'] ],
        'unused_taxes': taxes_unused,
    }
    #data['html_form'] = render_to_string('nor/tax_view.html',
    #                                     context,
    #                                     request=request)
    return render_template('nor/rule_taxview.html', data=data)


def get_journals_by_nor(name):
    # Все журналы на кого воздействует правило name
    col = get_col('log_rule')
    ruls = col.find({"logs.normrule": name}, {"logs.logname": 1, "name": 1})
    
    # уникальные названия журналов (нод если пусто)
    logs = set()
    for rul in ruls:
        for x in rul['logs']:
            if x['logname']:
                logs.add(x['logname'])
            else:
                logs.add(rul['name'])
    logs = list(logs)
    
    return logs

def pack_uniq_alerts(alerts):
    # уникальные сообщения 
    unique = {}
    for alert in alerts:
        log, raw = alert.get('alr_log'), alert.get('alr_raw')
        if None is (log, raw): continue
        
        other = '; '.join([f'{k}: {v}' for k, v in alert.items() if k not in ('alr_log', 'alr_raw') and type(v) == str])
        
        if type(raw) == list:
            raw = '<br/>'.join(raw)
        raw += '<br/>' + other
        
        if raw in unique:
            unique[raw].add(log)
        else:
            unique[raw] = set([log])
            
    for k in unique:
        unique[k] = ', '.join(unique[k])
        
    return unique
    
@bp.route('/nor/<string:name>/unique')
@login_required
def search_alerts(name):
    
    skip = request.args.get('skip')
    limit = request.args.get('limit')
    skip = int(skip) if skip.isdigit() else None
    limit = int(limit) if limit.isdigit() else 10000
    search = request.args.get('s')
    a = request.args.get('a')
    b = request.args.get('b')
    try:
        a = datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
    except:
        a = None
    try:
        b = datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
    except:
        b = None   
    
    logs = get_journals_by_nor(name)
    col = get_col('alerts')
    
    f = {'$and': []}
    
    f['$and'].append({'alr_log': {'$in': logs}})
    f['$and'].append({'alr_raw': {'$regex': search}})
    if a: f['$and'].append({'alr_time': {'$gte': a}})
    if b: f['$and'].append({'alr_time': {'$lt': b}})
    
    alert = []
    if skip and limit:
        alerts = col.find(f).skip(skip).limit(limit)
    elif skip:
        alerts = col.find(f).skip(skip)
    elif limit:
        alerts = col.find(f).limit(limit)
    else:
        alerts = col.find(f)
        
    unique = pack_uniq_alerts(alerts)
    return json.dumps(unique, indent=4, sort_keys=True, default=str)

@bp.route('/nor/<string:name>/alerts-unique')
@login_required
def alerts_unique(name):
    logs = get_journals_by_nor(name)
    skip = request.args.get('skip')
    limit = request.args.get('limit')
    skip = int(skip) if skip.isdigit() else None
    limit = int(limit) if limit.isdigit() else 10000
    # все сообщения журналов
    col = get_col('alerts')
    
    f = {'alr_log': {'$in': logs}}
    alert = []
    if skip and limit:
        alerts = col.find(f).skip(skip).limit(limit)
    elif skip:
        alerts = col.find(f).skip(skip)
    elif limit:
        alerts = col.find(f).limit(limit)
    else:
        alerts = col.find(f)
    
    unique = pack_uniq_alerts(alerts)
            
    return json.dumps(unique, indent=4, sort_keys=True, default=str)



@bp.route('/nor/regex/', methods=('GET', 'POST'))
@login_required
def check_regex():
    alert = str(request.form['alert'])
    regex = request.form['regex']
    try:
        res = Normaleizer.regex(regex, alert)
    except Exception as e: 
        logging.error('/nor/regex/' +repr(e))
        return '', 500
    if res == None: 
        if re.search(regex, alert): return True
        return ''
    return res