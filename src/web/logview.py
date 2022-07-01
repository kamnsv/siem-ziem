"""
    ZIEM
    
    Description:

    Author:
        Bengart Zakhar
"""

import os
import json
import tarfile
from datetime import datetime
from bson.objectid import ObjectId
from cryptography.fernet import Fernet
import os

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from flask import send_file

from .baseview import get_col, write_log, get_choice
from .authview import login_required
from .logform import RuleForm, CredForm, JsonForm, SearchForm

bp = Blueprint('log', __name__)

@bp.route('/log/rule/<string:obj>')
@login_required
def rule(obj):
    col = get_col('log_rule')
    form = SearchForm()
    form.selected_obj.choices = get_choice('obj')
    return render_template('log/rule.html', form=form)

@bp.route('/log/get_rule', methods=('GET', 'POST'))
@login_required
def get_rule():
    col = get_col('log_rule')
    form = SearchForm()
    obj = form.selected_obj.data
    if obj == None:
        obj = 'main'
    data = [ x for x in col.find({'obj':obj}).sort("name") ]
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/log/rule/add', methods=('GET', 'POST'))
@login_required
def rule_add():
    col = get_col('log_rule')
    form = RuleForm()
    form.obj.choices = get_choice('obj')
    form.login.choices = get_choice('login')
    form.protocol.choices = get_choice('protocol')
    for log in form.logs:
        log.normrule.choices = get_choice('normrule')
    if form.validate_on_submit():
        data = form.data
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        data['logs'] = [ x for x in data['logs'] if x['normrule'] ]
        del data['csrf_token']
        col.insert_one(data)
        write_log(2103, src='LOG', msg={'rule':  data['name']} )
        return redirect(url_for('log.rule', obj=data['obj']))
    url = '/log/rule/add'
    return render_template('log/rule_edit.html', form=form, url=url, obj='main')


@bp.route('/log/rule/<string:id>/<string:param>/<string:value>', methods=('GET', 'POST'))
@login_required
def rule_active_set(id, param, value):
    col = get_col('log_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    if doc.get(param) is None:
        return f'Parameter <b>"{param}"</b> is not found'
    if value.replace('.', '',1).isdigit(): 
        value = float(value) #if '.' in value else int(value)
    elif value.lower() in ['false', 'true']:
        value = True if 'true' == value else False
    doc[param] = value
    col.replace_one(
            {'_id': ObjectId(id)}, 
           doc)
    return json.dumps(doc, indent=4, default=str, ensure_ascii=False)

@bp.route('/log/rule/<string:id>/edit', methods=('GET', 'POST'))
@login_required
def rule_edit(id):
    col = get_col('log_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    form = RuleForm(data=doc)
    form.obj.choices = get_choice('obj')
    form.login.choices = get_choice('login')
    form.protocol.choices = get_choice('protocol')
    for log in form.logs:
        log.normrule.choices = get_choice('normrule')
    #return json.dumps(form.data, indent=4, default=str, ensure_ascii=False)
    if form.validate_on_submit():
        data = form.data
        del data['csrf_token']
        data['logs'] = [ x for x in data['logs'] if x['normrule'] ]
        msg = { 
            'rule': data['name'] 
        }
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
        write_log(2104, src='LOG', msg=msg )
       
        return redirect(url_for('log.rule', obj=data['obj']))
    url = request.url
    return render_template('log/rule_edit.html', form=form, url=url, obj=doc['obj'])

@bp.route('/log/rule/<string:id>/copy')
@login_required
def rule_copy(id):
    col = get_col('log_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    doc['name'] = doc['name'] + '_copy'
    doc['active'] = False
    del doc['_id']
    doc['pubdate'] = datetime.now().strftime("%Y-%m-%d")
    col.insert_one(doc)
    write_log(2105, src='LOG', msg={'rule':  doc['name']} )
    data = {
        'text': 'Правило скопировано: ' + doc['name'],
        'doc': doc,
    }
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/log/rule/<string:id>/del')
@login_required
def rule_del(id):
    col = get_col('log_rule')
    doc = col.find_one({'_id': ObjectId(id)})
    col.delete_one( {'_id': ObjectId(id)} )
    write_log(2106, src='LOG', msg={'rule':  doc['name']} )
    return 'Правило удалено: ' + doc['name']

@bp.route('/log/rule/json', methods=('GET', 'POST'))
@login_required
def rule_json():
    col = get_col('log_rule')
    data = get_currentconf(col)
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
            doc_old = col.find_one({'name': d['name']})
            if doc_old:
                for k, v in d.items():
                    if k in doc_old:
                        if v != doc_old[k]:
                            if isinstance(v, list):
                                for val in v:
                                    if val not in doc_old[k]:
                                        msg['new_value'] = val
                                        msg['old_list'] = doc_old[k]
                            else:
                                msg[k] = [doc_old[k], v]
                if len(msg) > 1:
                    d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                    col.replace_one(
                        {'name': d['name'], 'obj': obj}, d)
                    write_log(2104, src='LOG', msg=msg)
            else:
                d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                d['obj'] = obj
                col.insert_one(d)
                write_log(2103, src='LOG', msg=msg )
        return redirect(url_for('log.rule', obj='main'))
    return render_template('log/rule_json.html', form=form)

def get_currentconf(col):
    data = [ x for x in col.find() ]
    for d in data:
        del d['_id']
        del d['pubdate']
    return json.dumps(data, indent=4, ensure_ascii=False)

@bp.route('/log/get_backup/<string:col>/<string:id>')
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

@bp.route('/log/rule/save')
@login_required
def rule_save():
    col = get_col('log_rule')
    data = [ x for x in col.find() ]
    PATH = "/var/opt/ziem/tmp/log"
    file = PATH + '/log_rule.json'
    tar_file = PATH + '/log_rule.tar.bz2'
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
    write_log(2108, src='LOG')
    return send_file(tar_file, as_attachment=True, 
                     attachment_filename='log_rule.tar.bz2')

@bp.route('/log/cred/<string:obj>')
@login_required
def cred(obj):
    col = get_col('log_cred')
    form = SearchForm()
    form.selected_obj.choices = get_choice('obj')
    return render_template('log/cred.html', form=form)

@bp.route('/log/get_cred', methods=('GET', 'POST'))
@login_required
def get_cred():
    col = get_col('log_cred')
    form = SearchForm()
    obj = form.selected_obj.data
    if obj == None:
        obj = 'main'
    data = [ x for x in col.find({'obj':obj}).sort("name") ]
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/log/cred/add', methods=('GET', 'POST'))
@login_required
def cred_add():
    col = get_col('log_cred')
    form = CredForm()
    form.obj.choices = get_choice('obj')
    if form.validate_on_submit():
        data = form.data
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        data['pswd'] = enc_password(data['pswd'])
        col.insert_one(data)
        write_log(2109, src='LOG', msg={'rule': data['name']} )
        return redirect(url_for('log.cred', obj=data['obj']))
    url = '/log/cred/add'
    return render_template('log/cred_edit.html', form=form, url=url, obj='main')

@bp.route('/log/cred/<string:id>/edit', methods=('GET', 'POST'))
@login_required
def cred_edit(id):
    col = get_col('log_cred')
    doc = col.find_one({'_id': ObjectId(id)})    
    form = CredForm(data=doc)
    form.obj.choices = get_choice('obj')
    if form.validate_on_submit():
        data = form.data
        del data['csrf_token']
        msg = { 
            'rule': data['name'] 
        }
        """
        for k, v in data.items():
            if k != 'pswd':
                if k in doc:
                    if v != doc[k]:
                        msg[k] = [doc[k], v]
        """
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        data['pswd'] = enc_password(data['pswd'])
        col.replace_one(
            {'_id': ObjectId(id)},
            data)
        write_log(2110, src='LOG', msg=msg )
        return redirect(url_for('log.cred', obj=data['obj']))
    url = request.url
    return render_template('log/cred_edit.html', form=form, url=url, obj=doc['obj'])

@bp.route('/log/cred/<string:id>/del')
@login_required
def cred_del(id):
    col = get_col('log_cred')
    doc = col.find_one({'_id': ObjectId(id)})
    col.delete_one( {'_id': ObjectId(id)} )
    write_log(2106, src='LOG', msg={'cred':  doc['name']} )
    return 'Правило удалено: ' + doc['name']

def enc_password(data):
    try:
        with open('/etc/opt/ziem/ziem.k', 'rb') as f:
            key = f.read()
    except:
        key = Fernet.generate_key()
        with open('/etc/opt/ziem/ziem.k', 'wb') as f:
            f.write(key)
    fern_key = Fernet(key)
    return fern_key.encrypt(data.encode()).decode()
