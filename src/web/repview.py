"""
    ZIEM 
    
    Description:

    Author:
        Bengart Zakhar
"""
import os
import tarfile
from datetime import datetime
from datetime import timedelta
from bson.objectid import ObjectId

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from flask import send_file

from .baseview import get_col, get_choice
from .authview import login_required
from .repform import SearchForm

from bson.json_util import dumps
import json

bp = Blueprint('rep', __name__)

@bp.route('/rep/alert/')
@login_required
def alert():
    form = SearchForm()
    meta_fields = [ x['name'] for x in get_col('log_rule').find({'obj':'main'}).sort('name') ]
    return render_template('rep/alert.html', form=form, meta_fields=meta_fields)

@bp.route('/rep/get_alert/', methods=('GET', 'POST'))
@login_required
def get_alert():
    data = []
    max_count = 15000
    form = SearchForm()
    col = get_col('alerts')
    meta_field = form.meta_field.data
    date_start = form.date_start.data
    date_end = form.date_end.data
    if not date_start:
        date_start = datetime.now() - timedelta(minutes=10)
    if not date_end:
        date_end = datetime.now() + timedelta(hours=1)
    query = {"$and":[ 
        {'alr_time': {'$gte': date_start}}, 
        {'alr_time': {'$lte': date_end}} 
    ]}
    if meta_field:
        query["$and"].append({'alr_node': meta_field})
    data = [ x for x in col.find(query).sort('alr_time',-1).limit(max_count) ]
    #data = [ x for x in col.find(query).limit(max_count) ]
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/rep/event/')
@login_required
def event():
    form = SearchForm()
    meta_fields = [ x['name'] for x in get_col('log_rule').find({'obj':'main'}).sort('name') ]
    return render_template('rep/event.html', form=form, meta_fields=meta_fields)

@bp.route('/rep/get_event/', methods=('GET', 'POST'))
@login_required
def get_event():
    data = []
    max_count = 10000
    form = SearchForm()
    col = get_col('events')
    meta_field = form.meta_field.data
    date_start = form.date_start.data
    date_end = form.date_end.data
    if not date_start:
        date_start = datetime.now() - timedelta(days=1)
    if not date_end:
        date_end = datetime.now() + timedelta(hours=1)
    query = {"$and":[ 
        {'time': {'$gte': date_start}}, 
        {'time': {'$lte': date_end}} 
    ]}
    if meta_field:
        query["$and"].append({'node': meta_field})
    data = [ x for x in col.find(query).sort('time',-1).limit(max_count) ]
    return json.dumps(data, default=str, ensure_ascii=False)

@bp.route('/rep/event/<string:id>/modal')
@login_required
def modal_event(id):
    col = get_col('events')
    data = { k:v for k,v in col.find_one({'_id': ObjectId(id)}).items() }
    data = convert_event(data)
    return render_template('rep/event_modal.html', data=data)

@bp.route('/rep/inc/')
@login_required
def inc():
    form = SearchForm()
    meta_fast = [ x['name'] for x in get_col('cor_fastrule').find({'obj':'main'}) ]
    meta_deep = [ x['name'] for x in get_col('cor_deeprule').find({'obj':'main'}) ]
    meta_fields = sorted(meta_fast + meta_deep)
    return render_template('rep/inc.html', form=form, meta_fields=meta_fields)

@bp.route('/rep/get_inc/', methods=('GET', 'POST'))
@login_required
def get_inc():
    data = []
    max_count = 1000
    form = SearchForm()
    col = get_col('incs')
    meta_field = form.meta_field.data
    date_start = form.date_start.data
    date_end = form.date_end.data
    if not date_start:
        date_start = datetime.now() - timedelta(days=7)
    if not date_end:
        date_end = datetime.now() + timedelta(hours=1)
    query = {"$and":[ 
        {'inc_time': {'$gte': date_start}}, 
        {'inc_time': {'$lte': date_end}} 
    ]}
    if meta_field:
        query["$and"].append({'inc_name': meta_field})
    data = [ x for x in col.find(query).sort('inc_time',-1).limit(max_count) ]
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

@bp.route('/rep/inc/<string:id>/modal')
@login_required
def modal_inc(id):
    col = get_col('incs')
    data = { k:v for k,v in col.find_one({'_id': ObjectId(id)}).items() }
    data = convert_inc(data)
    return render_template('rep/inc_modal.html', data=data)

def convert_inc(data):
    fields = { x['name']: x['desc'] for x in get_col('opt_field').find() }
    crit = { x['name']: x['desc'] for x in get_col('opt_crit').find() }
    inc = { 
        'Название': data['inc_name'],
        'Описание': data['inc_mesg'],
        'Время': data['inc_time'].strftime('%d.%m.%Y %H:%M:%S'),
        'Критичность': crit[data['inc_crit']],
        'Классификатор': data['inc_clas'],
    }
    events = []
    for event_raw in data['events']:
        event = {}
        for key in event_raw:
            if key == 'tax':
                event['Таксономия'] = event_raw[key]
            elif key in fields:
                if key == 'alr_time':
                    event[fields[key]] = event_raw[key].strftime('%d.%m.%Y %H:%M:%S')
                else:
                    event[fields[key]] = event_raw[key]
            else:
                event[key] = event_raw[key]
        events.append(event)
    inc['События'] = events
    return inc

def convert_event(data_raw):
    fields = { x['name']: x['desc'] for x in get_col('opt_field').find() }
    data = []
    event = {}
    for key in data_raw:
        if key == 'alr_time':
            event[fields[key]] = data_raw[key].strftime('%d.%m.%Y %H:%M:%S')
        elif key in fields:
            event[fields[key]] = data_raw[key]
        elif key == '_id':
            pass
        else:
            event[key] = data_raw[key]
    return event
