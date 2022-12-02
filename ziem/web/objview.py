"""
    ZIEM 
    
    Description:

    Author:
        Bengart Zakhar
"""

import os
import json
import tarfile
import random
import string
import functools

from datetime import datetime
from bson.objectid import ObjectId

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from flask import send_file
from werkzeug.security import generate_password_hash, check_password_hash

from .baseview import get_col, write_log
from .authview import login_required
from .objform import RuleForm, JsonForm, SearchForm
from .corview import check_fastrule, check_deeprule
from .norview import check_rule
from bson.json_util import dumps

from flask import jsonify
from flask import send_from_directory
from flask import current_app

bp = Blueprint('obj', __name__)

@bp.route('/obj/rule/', methods=('GET', 'POST'))
@login_required
def rule():
    form = SearchForm()
    return render_template('obj/rule.html', form=form)

@bp.route('/obj/get_rule', methods=('GET', 'POST'))
@login_required
def get_rule():
    col = get_col('obj_rule')
    data = [ x for x in col.find({'name':{"$ne":'main'}}).sort("name") ]
    for d in data:
        fastrule_check = check_fastrule(d['name'])
        deeprule_check = check_deeprule(d['name'])
        norrule_check = check_rule(d['name'])
        sum_fastrule = len([ x for x in fastrule_check if x['diff'] ])
        sum_deeprule = len([ x for x in deeprule_check if x['diff'] ])
        sum_norrule = len([ x for x in norrule_check if x['diff'] ])
        d['fastrule_diff'] = sum_fastrule
        d['deeprule_diff'] = sum_deeprule
        d['norrule_diff'] = sum_norrule
        if 'token' in d:
            del d['token']
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/obj/rule/add', methods=('GET', 'POST'))
@login_required
def rule_add():
    col = get_col('obj_rule')
    form = RuleForm()
    if form.validate_on_submit():
        data = form.data
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        del data['csrf_token']
        col.insert_one(data)
        write_log(2103, src='OBJ', msg={'rule':  data['name']} )
        return redirect(url_for('obj.rule', obj='main'))
    return render_template('obj/rule_edit.html', form=form)

@bp.route('/obj/rule/<string:id>/edit', methods=('GET', 'POST'))
@login_required
def rule_edit(id):
    col = get_col('obj_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    form = RuleForm(data=doc)
    if form.validate_on_submit():
        data = form.data
        msg = { 
            'rule': data['name'] 
        }
        del data['csrf_token']
        if 'pswd' in data:
            if data['pswd'] == '':
                if 'token' in doc:
                    data['token'] = doc['token']
        for k, v in data.items():
            if k in doc:
                if v != doc[k]:
                    msg[k] = [doc[k], v]
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        col.replace_one(
            {'_id': ObjectId(id)}, 
            data)
        write_log(2104, src='OBJ', msg=msg )
        return redirect(url_for('obj.rule'))
    return render_template('obj/rule_edit.html', form=form)

@bp.route('/obj/rule/<string:id>/del')
@login_required
def rule_del(id):
    col = get_col('obj_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    name = doc['name']
    col.delete_one( {'_id': ObjectId(id)} )
    get_col('nor_rule').delete_many({'obj': name})
    get_col('cor_fastrule').delete_many({'obj': name})
    get_col('cor_deeprule').delete_many({'obj': name})
    write_log(2106, src='OBJ', msg={'rule':  doc['name']} )
    return 'Правило удалено: ' + doc['name']

@bp.route('/obj/rule/conf/<string:obj>')
@login_required
def conf(obj):
    col = get_col('nor_rule')
    data = [ x for x in col.find({'obj': obj}) ]
    return render_template('obj/conf.html', data=data)

@bp.route('/obj/rule/conf/<string:obj>/json', methods=('GET', 'POST'))
@login_required
def conf_json(obj):
    data = get_currentconf(obj)
    form = JsonForm(data={'jdata': data})
    form.backup.choices = get_choice('backup')
    if form.validate_on_submit():
        data = json.loads(form.jdata.data)
        for col_name, data_col in data.items():
            col = get_col(col_name)
            for doc in col.find({'obj':obj}):
                col.remove(doc)
            if (col_name == 'log_rule' or
                col_name == 'nor_rule' or
                col_name == 'cor_fastrule' or
                col_name == 'cor_deeprule' or
                col_name == 'main'):
                for d in data_col:
                    d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                    d['obj'] = obj
                    col.insert_one(d)
        write_log(2114, src='OBJ')
        #col_backup()
        return redirect(url_for('obj.rule'))
    return render_template('obj/rule_json.html', form=form, obj=obj)

def get_currentconf(obj):
    cols = get_colllection(obj)
    data = {}
    for k,v in cols.items():
        for d in v:
            if '_id' in d:
                del d['_id']
            if 'pubdate' in d:
                del d['pubdate']
        data[k] = v
    return json.dumps(data, indent=4, ensure_ascii=False)

def get_colllection(obj):
    return {
        'log_rule': [ x for x in get_col('log_rule').find({'obj':obj}) ],
        'nor_rule': [ x for x in get_col('nor_rule').find({'obj':obj}) ],
        'cor_fastrule': [ x for x in get_col('cor_fastrule').find({'obj':obj}) ],
        'cor_deeprule': [ x for x in get_col('cor_deeprule').find({'obj':obj}) ],
        'opt_profile': [ x for x in get_col('opt_profile').find() ],
        'opt_protocol': [ x for x in get_col('opt_protocol').find() ],
        'opt_tax': [ x for x in get_col('opt_tax').find() ],
        'opt_field': [ x for x in get_col('opt_field').find() ],
        'opt_crit': [ x for x in get_col('opt_crit').find() ],
        'opt_clas': [ x for x in get_col('opt_clas').find() ],
        'main': [ x for x in get_col('main').find({'obj':obj}) ],
    }    


@bp.route('/obj/rule/<string:obj>/save')
@login_required
def rule_save(obj):
    cols = get_colllection(obj)
    data = {}
    PATH = "/var/opt/ziem/tmp"
    file = PATH + '/' + obj + '.json'
    file_main = PATH + '/' + 'ziem.json'
    tar_file = PATH + '/' + obj + '.tar.bz2'
    os.makedirs(PATH, exist_ok=True)
    with tarfile.open(tar_file, 'w:bz2') as tar:
        for col_name, data_col in cols.items():
            file_rule = PATH + '/' + col_name + '.json'
            for d in data_col:
                if '_id' in d:
                    del d['_id']
                if 'pubdate' in d:
                    del d['pubdate']
            with open(file_rule, "w") as f:
                json.dump(data_col, f, indent=4, ensure_ascii=False)
            tar.add(file_rule, os.path.basename(file_rule))
            data[col_name] = data_col
        with open(file_main, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        tar.add(file_main, 'ziem.json')
    file_name = obj + '-' + datetime.now().strftime('%Y-%m-%d') + '.tar.bz2'
    write_log(2108, src='OBJ')
    return send_file(tar_file, as_attachment=True, attachment_filename=file_name)


def obj_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        print(request.headers.get('User-Agent'), request.authorization)
        auth = request.authorization
        if auth:
            obj_id = auth.username
            token = auth.password
            col = get_col('obj_rule')
            doc = col.find_one({'_id': ObjectId(obj_id)})
            
            if doc and doc['sender_ip'] == request.environ.get('REMOTE_PORT'):
                if 'token' in doc:
                    if check_password_hash(doc['token'], token):
                        return view(**kwargs)

        return ("Unauthorized", 401)
    return wrapped_view

@bp.route('/obj/connect', methods=('GET', 'POST'))
def connect():
    name = request.json.get("username", None)
    password = request.json.get("password", None)
    col = get_col('obj_rule')
    doc = col.find_one({'name': name})
    if doc:
        if 'pswd' in doc:
            if doc['pswd']:
                if doc['pswd'] == password:
                    letters = (random.choice(
                        string.ascii_uppercase + string.ascii_lowercase) 
                        for _ in range(32))
                    token = ''.join(letters)
                    obj_id = str(doc['_id'])
                    col.update_one({
                          'name': name
                        },{
                          '$set': {
                            'token': generate_password_hash(token),
                            'pswd': '',
                          }
                        })
                    return jsonify(token=token, obj_id=obj_id)
    return jsonify({"msg": "Bad username or password"}), 401

@bp.route('/obj/getupdate')
def getupdate():
    name = request.args.get('name')
    col = get_col('obj_rule')
    isupdate = {
        'updateagent': False,
        'updateziem': False,
    }
    doc = col.find_one({'name':name})
    if doc:
        if 'updateagent' in doc:
            isupdate['updateagent'] = doc['updateagent']
        if 'updateziem' in doc:
            isupdate['updateziem'] = doc['updateziem']
        if 'updateconfig' in doc:
            isupdate['updateconfig'] = doc['updateconfig']
    col.update_one({
      'name': name
    },{
      '$set': {
        'updateagent': False,
        'updateziem': False,
        'updateconfig': False,
      }
    })
    return isupdate

@bp.route('/obj/putversion', methods=('GET', 'PUT'))
def putversion():
    print(request,request.remote_addr, request.environ.get('REMOTE_PORT'))
    name = request.args.get('name')
    col = get_col('obj_rule')
    data = request.json
    col.update_one({
      'name': data['name']
    },{
      '$set': {
        'version_ziem': data['version_ziem'],
        'version_agent': data['version_agent'],
        'date_change': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      }
    })
    return ('', 200)


@bp.route('/obj/getconfweb')
#@obj_required
def getconfweb():
    name = request.args.get('name')
    conf = {}
    cols = [
        'log_rule',
        'log_cred',
        'nor_rule',
        'cor_rule',
        'cor_fastrule',
        'cor_deeprule',
    ]
    for c in cols:
        col = get_col(c)
        data = [ x for x in col.find() if x['obj'] == name ]
        for d in data:
            if '_id' in d:
                del d['_id']
                d['obj'] = 'main'
        conf[c] = data
    cols = [
        'opt_profile',
        'opt_protocol',
        'opt_tax',
        'opt_field',
        'opt_crit',
        'opt_clas',
        'opt_bks',
        'opt_sub',
        'opt_type'
    ]
    for c in cols:
        col = get_col(c)
        data = [ x for x in col.find()]
        for d in data:
            if '_id' in d:
                del d['_id']
            if 'api' in d:  
                if d['api']:
                    d['api'] = f'https://%(ZIEM_CC_IP)s:%(ZIEM_CC_PORT)s/api/book/'+d['name']
                    d['active'] = True
                else:
                    del d['api']
            if 'scheduled' in d:  
                del d['scheduled']
            if 'token' in d:  
                del d['token']
        conf[c] = data
    
    cols = []
    col = get_col('opt_bks')
    for book in col.find():
        cols.append('bks_'+book['name'])    
        
    for c in cols:
        col = get_col(c)
        data = [ x for x in col.find()]
        for d in data:
            if '_id' in d:
                del d['_id']
        conf[c] = data
        
    col = get_col('obj_rule')
    data = col.find_one({'name': name})
    setting = {
        'name': 'setting',
        'cor_name': name,
        'sender_ip': data['sender_ip'],
    }
    conf['main'] = [setting]
    return conf