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

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from flask import send_file

from .baseview import get_col, write_log, get_choice
from .authview import login_required
from .corform import FastruleForm, DeepruleForm, JsonForm, SearchForm

bp = Blueprint('cor', __name__)

@bp.route('/cor/fastrule/<string:obj>')
@login_required
def fastrule(obj):
    col = get_col('cor_fastrule')
    form = SearchForm()
    form.selected_obj.choices = get_choice('obj')
    form.selected_obj.data = obj
    return render_template('cor/fastrule.html', form=form, obj=obj)

@bp.route('/cor/get_fastrule/<string:obj>', methods=('GET', 'POST'))
@login_required
def get_fastrule(obj):
    form = SearchForm()
    if form.selected_obj.data:
        obj = form.selected_obj.data
    data = check_fastrule(obj)
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

def check_fastrule(obj):
    col = get_col('cor_fastrule')
    if obj == None:
        obj = 'main'
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

@bp.route('/cor/fastrule/add', methods=('GET', 'POST'))
@login_required
def fastrule_add():
    col = get_col('cor_fastrule')
    form = FastruleForm()
    form.obj.choices = get_choice('obj')
    form.tax_main.choices = get_choice('tax_main')
    form.tax_object.choices = get_choice('tax_object')
    form.tax_action.choices = get_choice('tax_action')
    form.crit.choices = get_choice('crit')
    form.clas.choices = get_choice('clas')
    if form.validate_on_submit():
        data = form.data
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        del data['csrf_token']
        col.insert_one(data)
        write_log(2103, src='COR', msg={'rule':  data['name']} )
        return redirect(url_for('cor.fastrule', obj=data['obj']))
    diff = {}
    return render_template('cor/fastrule_edit.html', form=form, obj='main', diff=diff)

@bp.route('/cor/fastrule/<string:id>/edit', methods=('GET', 'POST'))
@login_required
def fastrule_edit(id):
    col = get_col('cor_fastrule')
    doc = col.find_one({'_id': ObjectId(id)})
    form = FastruleForm(data=doc)
    form.obj.choices = get_choice('obj')
    form.tax_main.choices = get_choice('tax_main')
    form.tax_object.choices = get_choice('tax_object')
    form.tax_action.choices = get_choice('tax_action')
    form.crit.choices = get_choice('crit')
    form.clas.choices = get_choice('clas')
    if form.validate_on_submit():
        data = form.data
        del data['csrf_token']
        msg = { 
            'rule': data['name'] 
        }
        """
        for k, v in data.items():
            if k in doc:
                if v != doc[k]:
                    msg[k] = [doc[k], v]
        """
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        col.replace_one(
            {'_id': ObjectId(id)},
            data)
        get_col('cor_fastrule').update_many(
            {'name': doc['name']},
            { '$set': {'name': data['name'], 'desc': data['desc'] }}
        )
        write_log(2104, src='COR', msg=msg )
        #file = '/var/opt/ziem/conf/conf_changed'
        #with open(file, "w") as f:
        #    f.write('1')
        return redirect(url_for('cor.fastrule', obj=data['obj']))
    diff = diff_fastrule(doc, col)
    return render_template('cor/fastrule_edit.html', form=form, obj=doc['obj'], diff=diff)

def diff_fastrule(doc, col):
    doc_main = col.find_one({'$and': [{'obj':'main'}, {'name':doc['name']}]})
    diff = {}
    if doc_main:
        for d in doc:
            if d not in ('obj', 'pubdate', '_id'):
                if d in doc_main:
                    if doc[d] != doc_main[d]:
                        diff[d] = doc_main[d]
    return diff

@bp.route('/cor/fastrule/<string:id>/copy')
@login_required
def fastrule_copy(id):
    col = get_col('cor_fastrule')
    doc = col.find_one({'_id': ObjectId(id)})
    doc['name'] = doc['name'] + '_copy'
    del doc['_id']
    doc['pubdate'] = datetime.now().strftime("%Y-%m-%d")
    col.insert_one(doc)
    write_log(2105, src='COR', msg={'rule':  doc['name']} )
    data = {
        'text': 'Правило скопировано: ' + doc['name'],
        'doc': doc,
    }
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/cor/fastrule/<string:id>/del')
@login_required
def fastrule_del(id):
    col = get_col('cor_fastrule')
    doc = col.find_one({'_id': ObjectId(id)})
    col.delete_one( {'_id': ObjectId(id)} )
    write_log(2106, src='COR', msg={'rule':  doc['name']} )
    return 'Правило удалено: ' + doc['name']

@bp.route('/cor/fastrule/<string:id>/sync/<string:obj>')
@login_required
def fastrule_sync(id, obj):
    col = get_col('cor_fastrule')
    doc = col.find_one({'_id': ObjectId(id)})
    if doc['obj'] == 'main':
        del doc['_id']
        doc['obj'] = obj
        col.insert_one(doc)
        write_log(2103, src='COR', msg={'rule':  doc['name']} )
    else:
        new_doc = col.find_one({'$and': [{'name': doc['name']}, {'obj':'main'}]})
        if new_doc:
            col.delete_one( {'_id': ObjectId(id)} )
            del new_doc['_id']
            new_doc['obj'] = obj
            col.insert_one(new_doc)
            write_log(2103, src='COR', msg={'rule':  new_doc['name']} )
    return 'Правило синхронизировано: ' + doc['name']

@bp.route('/cor/fastrule/json', methods=('GET', 'POST'))
@login_required
def fastrule_json():
    col = get_col('cor_fastrule')
    data = get_currentconf(col)
    form = JsonForm(request.form, data={'jdata': data})
    form.obj.choices = (
        [("main", "Основной")] + [(x['name'], x['name']) 
        for x in get_col('obj_rule').find().sort('name')])
    form.backup.choices = ([('/cor/get_backup/cor_fastrule/current', 'Текущая конфигурация')] 
        + [('/cor/get_backup/cor_fastrule/' + str(x['_id']), x['time']) for x in get_col('backup').find()])
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
                            msg[k] = [doc_old[k], v]
                if len(msg) > 1:
                    d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                    col.replace_one(
                        {'name': d['name'], 'obj': obj}, d)
                    write_log(2104, src='COR', msg=msg)
            else:
                d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                d['obj'] = obj
                col.insert_one(d)
                write_log(2103, src='COR', msg=msg )
        return redirect(url_for('cor.fastrule', obj='main'))
    return render_template('cor/fastrule_json.html', form=form)

@bp.route('/cor/fastrule/save')
@login_required
def fastrule_save():
    col = get_col('cor_fastrule')
    data = [ x for x in col.find() ]
    PATH = "/var/opt/ziem/tmp/cor"
    file = PATH + '/cor_fastrule.json'
    tar_file = PATH + '/cor_fastrule.tar.bz2'
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
    write_log(2108, src='COR')
    return send_file(tar_file, as_attachment=True, attachment_filename='cor_fastrule.tar.bz2')

@bp.route('/cor/deeprule/<string:obj>')
@login_required
def deeprule(obj):
    col = get_col('cor_deeprule')
    form = SearchForm()
    form.selected_obj.choices = get_choice('obj')
    form.selected_obj.data = obj
    return render_template('cor/deeprule.html', form=form, obj=obj)

@bp.route('/cor/get_deeprule/<string:obj>', methods=('GET', 'POST'))
@login_required
def get_deeprule(obj):
    form = SearchForm()
    if form.selected_obj.data:
        obj = form.selected_obj.data
    data = check_deeprule(obj)
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

def check_deeprule(obj):
    col = get_col('cor_deeprule')
    if obj == None:
        obj = 'main'
    data_main = { x['name']:x for x in col.find({'obj':'main'}) }
    data = { x['name']:x for x in col.find().sort("name") if x['obj'] == obj }
    data_miss = [ x for x in data_main if x not in data ]
    data_search = []
    for d in data_miss:
        data_main[d]['diff'] = 'miss'
        data_search.append(data_main[d])
    for d in data:
        if 'rule_force' in data[d]:
            data[d]['diff'] = False
        elif data[d]['name'] not in data_main:
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
                        k == 'pubdate' or k == 'rule_force'):
                        diff = False
                    else:
                        diff = 'changed'
                        break
            data[d]['diff'] = diff
            data[d]['_id'] = d_id
        data_search.append(data[d])
    return data_search
@bp.route('/cor/deeprule/add', methods=('GET', 'POST'))
@login_required
def deeprule_add():
    col = get_col('cor_deeprule')
    form = DeepruleForm()
    form.obj.choices = get_choice('obj')
    form.crit.choices = get_choice('crit')
    form.clas.choices = get_choice('clas')
    form.uniq1.choices = get_choice('field')
    form.uniq2.choices = get_choice('field')
    for event in form.events:
        event.tax_main.choices = get_choice('tax_main')
        event.tax_object.choices = get_choice('tax_object')
        event.tax_action.choices = get_choice('tax_action')
        event.diff.choices = get_choice('field')
        for incfilter in event.incfilter:
            incfilter.field.choices = get_choice('field')
        for excfilter in event.excfilter:
            excfilter.field.choices = get_choice('field')
    if form.validate_on_submit():
        data = form.data
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        data['events'] = [ x for x in data['events'] if x['tax_main'] ]
        del data['csrf_token']
        for event in data['events']:
            event['incfilter'] = [ x for x in event['incfilter'] if x['value'] ]
            event['excfilter'] = [ x for x in event['excfilter'] if x['value'] ]
        col.insert_one(data)
        write_log(2103, src='COR', msg={'rule':  data['name']} )
        return redirect(url_for('cor.deeprule', obj=data['obj']))
    return render_template('cor/deeprule_edit.html', form=form, obj='main', diff={})

@bp.route('/cor/deeprule/<string:id>/edit', methods=('GET', 'POST'))
@login_required
def deeprule_edit(id):
    col = get_col('cor_deeprule')
    doc = col.find_one({'_id': ObjectId(id)})
    form = DeepruleForm(data=doc)
    form.obj.choices = get_choice('obj')
    form.crit.choices = get_choice('crit')
    form.clas.choices = get_choice('clas')
    form.uniq1.choices = get_choice('field')
    form.uniq2.choices = get_choice('field')
    for event in form.events:
        event.tax_main.choices = get_choice('tax_main')
        event.tax_object.choices = get_choice('tax_object')
        event.tax_action.choices = get_choice('tax_action')
        event.diff.choices = get_choice('field')
        for incfilter in event.incfilter:
            incfilter.field.choices = get_choice('field')
        for excfilter in event.excfilter:
            excfilter.field.choices = get_choice('field')
    if form.validate_on_submit():
        data = form.data
        msg = { 
            'rule': data['name'] 
        }
        data['events'] = [ x for x in data['events'] if x['tax_main'] ]
        del data['csrf_token']
        for event in data['events']:
            event['incfilter'] = [ x for x in event['incfilter'] if x['value'] ]
            event['excfilter'] = [ x for x in event['excfilter'] if x['value'] ]
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
        if 'rule_force' in data:
            del data['rule_force']
        col.replace_one(
            {'_id': ObjectId(id)}, 
            data)
        get_col('cor_deeprule').update_many(
            {'name': doc['name']},
            { '$set': {'name': data['name'], 'desc': data['desc'] }}
        )
        write_log(2104, src='COR', msg=msg )
        return redirect(url_for('cor.deeprule', obj=data['obj']))
    diff = diff_deeprule(doc, col)
    return render_template('cor/deeprule_edit.html', form=form, obj=doc['obj'], diff=diff)

def diff_deeprule(doc, col):
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

@bp.route('/cor/deeprule/<string:id>/copy')
@login_required
def deeprule_copy(id):
    col = get_col('cor_deeprule')
    doc = col.find_one({'_id': ObjectId(id)})
    doc['name'] = doc['name'] + '_copy'
    del doc['_id']
    doc['pubdate'] = datetime.now().strftime("%Y-%m-%d")
    col.insert_one(doc)
    write_log(2105, src='COR', msg={'rule':  doc['name']} )
    data = {
        'text': 'Правило скопировано: ' + doc['name'],
        'doc': doc,
    }
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/cor/deeprule/<string:id>/del')
@login_required
def deeprule_del(id):
    col = get_col('cor_deeprule')
    doc = col.find_one({'_id': ObjectId(id)})
    col.delete_one( {'_id': ObjectId(id)} )
    write_log(2106, src='COR', msg={'rule':  doc['name']} )
    return 'Правило удалено: ' + doc['name']

@bp.route('/cor/deeprule/<string:id>/sync/<string:obj>')
@login_required
def deeprule_sync(id, obj):
    col = get_col('cor_deeprule')
    doc = col.find_one({'_id': ObjectId(id)})
    if doc['obj'] == 'main':
        del doc['_id']
        doc['obj'] = obj
        col.insert_one(doc)
        write_log(2103, src='COR', msg={'rule':  doc['name']} )
    else:
        new_doc = col.find_one({'$and': [{'name': doc['name']}, {'obj':'main'}]})
        if new_doc:
            col.delete_one( {'_id': ObjectId(id)} )
            del new_doc['_id']
            new_doc['obj'] = obj
            col.insert_one(new_doc)
            write_log(2103, src='COR', msg={'rule':  new_doc['name']} )
    return 'Правило синхронизировано: ' + doc['name']

@bp.route('/cor/deeprule/<string:id>/force')
@login_required
def deeprule_force(id):
    col = get_col('cor_deeprule')
    doc = col.find_one({'_id': ObjectId(id)})
    doc_main = col.find({'$and': [{'name': doc['name']}, {'obj':'main'}]})

    if doc['obj'] == 'main' or not doc_main:
        return '','400'
    get_col('cor_deeprule').update_one(
        {'_id': ObjectId(id)},
        { '$set': {'rule_force': True }}
    )
    write_log(2104, src='COR', msg={'rule':  doc['name']} )
    return 'Правило форсировано: ' + doc['name']

@bp.route('/cor/deeprule/json', methods=('GET', 'POST'))
@login_required
def deeprule_json():
    col = get_col('cor_deeprule')
    data = [ x for x in col.find({'obj':'main'}) ]
    for d in data:
        del d['_id']
        del d['pubdate']
    data = json.dumps(data, indent=4, ensure_ascii=False)
    form = JsonForm(data={'jdata': data})
    form.obj.choices = (
        [("main", "Основной")] + [(x['name'], x['name']) 
        for x in get_col('obj_rule').find().sort('name')])
    form.backup.choices = ([('/cor/get_backup/cor_deeprule/current', 'Текущая конфигурация')] 
        + [('/cor/get_backup/cor_deeprule/' + str(x['_id']), x['time']) for x in get_col('backup').find()])
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
                                        msg['old_list'] = doc_old[k]
                            else:
                                msg[k] = [doc_old[k], v]
                if len(msg) > 1:
                    d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                    col.replace_one(
                        {'name': d['name'], 'obj': obj}, d)
                    write_log(2104, src='COR', msg=msg)
            else:
                d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                d['obj'] = obj
                col.insert_one(d)
                write_log(2103, src='COR', msg=msg )
        return redirect(url_for('cor.deeprule', obj='main'))
    return render_template('cor/deeprule_json.html', form=form)

@bp.route('/cor/deeprule/save')
@login_required
def deeprule_save():
    col = get_col('cor_deeprule')
    data = [ x for x in col.find() ]
    PATH = "/var/opt/ziem/tmp/cor"
    file = PATH + '/cor_deeprule.json'
    tar_file = PATH + '/cor_deeprule.tar.bz2'
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
    write_log(2108, src='COR')
    return send_file(tar_file, as_attachment=True, attachment_filename='cor_deeprule.tar.bz2')

@bp.route('/cor/rulemap/')
@login_required
def rulemap():
    # просмотр карты соответсвия правил корреляции и нормализации
    nor_rule = get_col('nor_rule').find({'obj':'main'}).sort('name')
    cor_fastrule = get_col('cor_fastrule').find({'obj':'main'}).sort('name')
    cor_deeprule = get_col('cor_deeprule').find({'obj':'main'}).sort('name')
    data = dict()
    for rule in nor_rule:
        for event in rule['events']:
            tax = rule['tax_main'] + event['tax_object'] + event['tax_action']
            fastrules = get_col('cor_fastrule').find()
            for fastrule in fastrules:
                tax_fast = fastrule['tax_main'] + fastrule['tax_object'] + fastrule['tax_action']
                event_name = rule['name'] + ':' + event['alr_msg']
                if tax == tax_fast:
                    if fastrule['name'] not in data:
                        data[fastrule['name']] = []
                    if event_name not in data[fastrule['name']]:
                        data[fastrule['name']].append(event_name)
            deeprules = get_col('cor_deeprule').find()
            for deeprule in deeprules:
                if deeprule['name'] not in data:
                    data[deeprule['name']] = []
                for deepevent in deeprule['events']:
                    tax_deep = deepevent['tax_main'] + deepevent['tax_object'] + deepevent['tax_action']
                    if tax == tax_deep:
                        event_name = rule['name'] + ':' + event['alr_msg']
                        if event_name not in data[deeprule['name']]:
                            data[deeprule['name']].append(event_name)
    return render_template('cor/rulemap.html', data=data)

def get_currentconf(col):
    data = [ x for x in col.find() ]
    for d in data:
        del d['_id']
        del d['pubdate']
    return json.dumps(data, indent=4, ensure_ascii=False)

@bp.route('/cor/get_backup/<string:col>/<string:id>')
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
