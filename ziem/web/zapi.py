"""
    ZIEM 
    
    Description:

    Author:
        Kamnev Sergey
"""

import json

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for

from .objview import obj_required
from .baseview import get_col, write_log
from .authview import login_required
bp = Blueprint('api', __name__)

@login_required
@bp.route('/api/<string:api>')
def api_json(api):
    j = []
    if 'ping' == api: j = get_ping()
    return json.dumps(j, indent=4, sort_keys=True, default=str)

def get_ping():
    col = get_col('ping')
    cur = col.find({}, {'_id': False})
    return list(cur)

#@obj_required
@bp.route('/api/book/<string:name>')
def api_bks(name):
    
    col = get_col('opt_bks')
    bks = col.find_one({'name': name, 'api': {'$exists': True}})

    if bks is None:  return render_template('error.html', title=404)
    
    
    col = get_col(f'bks_{name}')
    cur = col.find({}, {'_id': False, 'pubdate': False})
    
    
    key_list = bks.get('data_list_key')
    keys_val = bks.get('data_value_key', 'name').split('.')[::-1]
    
    data = []
    name = keys_val[0] if keys_val[0] else 'name'
    for row in cur:
        item = {
            name: row['name'],
            'desc': row['desc'],
        }
        for k in keys_val[1:]:
            item = {k: item}
        data.append(item)
    
    if key_list:
        for k in key_list.split('.')[::-1]:
            data = {k: data}
        
    return json.dumps(data, indent=4, sort_keys=True, default=str)