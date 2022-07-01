"""
    ZIEM 
    
    Description:

    Author:
        Kamnev Sergey
"""

import json

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for

from .baseview import get_col, write_log

bp = Blueprint('api', __name__)

@bp.route('/api/<string:api>')
def api_json(api):
    j = []
    if 'ping' == api: j = get_ping()
    return json.dumps(j, indent=4, sort_keys=True, default=str)

def get_ping():
    col = get_col('ping')
    cur = col.find({}, {'_id': False})
    return list(cur)