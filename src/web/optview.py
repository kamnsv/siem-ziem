"""
    ZIEM 
    
    Description:

    Author:
        Bengart Zakhar
"""

import json
import logging
from datetime import datetime
from bson.objectid import ObjectId

from flask import Blueprint, flash, redirect
from flask import render_template, g, request, url_for

from .authview import login_required
from .baseview import get_col, write_log
from .optform import OptForm, JsonForm, SearchForm

bp = Blueprint('opt', __name__)

def update_opt(option, doc, data):
    if option == 'opt_taxmain':
        get_col('nor_rule').update_many(
            {'tax_main': doc['name']},
            { '$set': {'tax_main': data['name'] }}
        )
        get_col('cor_fastrule').update_many(
            {'tax_main': doc['name']},
            { '$set': {'tax_main': data['name'] }}
        )
        get_col('cor_deeprule').update_many(
            {}  ,
            { '$set': {'events.$[element].tax_main': data['name'] }},
            array_filters=[{ "element.tax_main": doc['name'] }],
        )
    elif option == 'opt_taxobject':
        get_col('nor_rule').update_many(
            {}  ,
            { '$set': {'events.$[element].tax_object': data['name'] }},
            array_filters=[{ "element.tax_object": doc['name'] }],
        )
        get_col('cor_fastrule').update_many(
            {'tax_object': doc['name']},
            { '$set': {'tax_object': data['name'] }}
        )
        get_col('cor_deeprule').update_many(
            {}  ,
            { '$set': {'events.$[element].tax_object': data['name'] }},
            array_filters=[{ "element.tax_object": doc['name'] }],
        )
    elif option == 'opt_taxaction':
        get_col('nor_rule').update_many(
            {}  ,
            { '$set': {'events.$[element].tax_action': data['name'] }},
            array_filters=[{ "element.tax_action": doc['name'] }],
        )
        get_col('cor_fastrule').update_many(
            {'tax_action': doc['name']},
            { '$set': {'tax_action': data['name'] }}
        )
        get_col('cor_deeprule').update_many(
            {}  ,
            { '$set': {'events.$[element].tax_action': data['name'] }},
            array_filters=[{ "element.tax_action": doc['name'] }],
        )
    elif option == 'opt_profile':
        get_col('nor_rule').update_many(
            {'profile': doc['name']},
            { '$set': {'profile': data['name'] }}
        )
    elif option == 'opt_protocol':
        get_col('log_rule').update_many(
            {'protocol': doc['name']},
            { '$set': {'protocol': data['name'] }}
        )
    elif option == 'opt_field':
        get_col('nor_rule').update_many(
            {}  ,
            { '$set': {'events.$[].regex.$[r].field': data['name'] }},
            array_filters=[{ "r.field": doc['name'] }],
        )
        get_col('cor_deeprule').update_many(
            {'uniq1': doc['name']},
            { '$set': {'uniq1': data['name'] }}
        )
        get_col('cor_deeprule').update_many(
            {'uniq2': doc['name']},
            { '$set': {'uniq2': data['name'] }}
        )
        get_col('cor_deeprule').update_many(
            {}  ,
            { '$set': {'events.$[element].diff': data['name'] }},
            array_filters=[{ "element.diff": doc['name'] }],
        )
        get_col('cor_deeprule').update_many(
            {}  ,
            { '$set': {'events.$[].incfilter.$[r].field': data['name'] }},
            array_filters=[{ "r.field": doc['name'] }],
        )
        get_col('cor_deeprule').update_many(
            {}  ,
            { '$set': {'events.$[].excfilter.$[r].field': data['name'] }},
            array_filters=[{ "r.field": doc['name'] }],
        )
    elif option == 'opt_clas':
        get_col('cor_fastrule').update_many(
            {'clas': doc['name']},
            { '$set': {'clas': data['name'] }}
        )    
        get_col('cor_deeprule').update_many(
            {'clas': doc['name']},
            { '$set': {'clas': data['name'] }}
        )
    elif option == 'opt_crit':
        get_col('cor_fastrule').update_many(
            {'crit': doc['name']},
            { '$set': {'crit': data['name'] }}
        )    
        get_col('cor_deeprule').update_many(
            {'crit': doc['name']},
            { '$set': {'crit': data['name'] }}
        )

@bp.route('/opt/<string:option>/')
@login_required
def opt(option):
    form = SearchForm()
    return render_template('opt/opt.html', form=form, option=option)

@bp.route('/opt/<string:option>/get')
@login_required
def get_opt(option):
    col = get_col(option)
    data = [ x for x in col.find().sort("name") ]
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/opt/<string:option>/add', methods=('GET', 'POST'))
@login_required
def opt_add(option):
    col = get_col(option)
    form = OptForm()
    if form.validate_on_submit():
        data = form.data
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        del data['csrf_token']
        col.insert_one(data)
        write_log(2116, src='OPT', msg={'profile':  data['name']} )
        return redirect(url_for('opt.opt', option=option))
    return render_template('opt/opt_edit.html', form=form)

@bp.route('/opt/<string:option>/<string:id>/edit', methods=('GET', 'POST'))
@login_required
def opt_edit(option, id):
    col = get_col(option)
    doc = col.find_one({'_id': ObjectId(id)})
    form = OptForm(data=doc)
    if form.validate_on_submit():
        data = form.data
        msg = { 
            option: data['name'] 
        }
        """
        for k, v in data.items():
            if k in doc:
                if v != doc[k]:
                    msg[k] = [doc[k], v]
        """
        data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
        del data['csrf_token']
        col.replace_one(
            {'_id': ObjectId(id)}, 
            data)
        write_log(2117, src='OPT', msg=msg )
        update_opt(option, doc, data)
        return redirect(url_for('opt.opt', option=option))
    return render_template('opt/opt_edit.html', form=form, option=option)

@bp.route('/opt/<string:option>/<string:id>/del', methods=('GET', 'POST'))
@login_required
def opt_del(option, id):
    col = get_col(option)
    doc = col.find_one({'_id': ObjectId(id)})
    col.delete_one( {'_id': ObjectId(id)} )
    write_log(2118, src='OPT', msg={option:  doc['name']} )
    name = doc['name']
    doc['name'] = ''
    data = {'name': ''}
    update_opt(option, doc, data)
    return 'Правило удалено: ' + name

@bp.route('/opt/<string:col_id>/json', methods=('GET', 'POST'))
@login_required
def opt_json(col_id):
    col_name = 'opt_' + col_id
    col = get_col(col_name)
    data = get_currentconf(col)
    form = JsonForm(data={'jdata': data})
    form.backup.choices = get_choice('opt_backup')
    form.backup.choices = ([('/opt/get_backup/' + col_name + '/current', 'Текущая конфигурация')] 
        + [('/opt/get_backup/' + col_name + '/' + str(x['_id']), x['time']) for x in get_col('backup').find()])
    if form.validate_on_submit():
        data = json.loads(form.jdata.data)
        for d in data:
            msg = { 
                'opt': col_id,
                'rule': d['name'],
            }
            doc_old = col.find_one({'name': d['name']})
            if doc_old:
                for k, v in d.items():
                    if k in doc_old:
                        if v != doc_old[k]:
                            msg[k] = [doc_old[k], v]
                if len(msg) > 2:
                    d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                    col.replace_one(
                        {'name': d['name']}, d)
                    write_log(2117, src='OPT', msg=msg)
            else:
                d['pubdate'] = datetime.now().strftime("%Y-%m-%d")
                col.insert_one(d)
                write_log(2116, src='OPT', msg=msg )
        return redirect(url_for('opt.' + col_id))
    return_href = '/opt/' + col_id
    return render_template('opt/opt_json.html', form=form, return_href=return_href)

def get_currentconf(col):
    data = [ x for x in col.find() ]
    for d in data:
        del d['_id']
        del d['pubdate']
    return json.dumps(data, indent=4, ensure_ascii=False)

@bp.route('/opt/get_backup/<string:col>/<string:id>')
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
