"""
    ZIEM 
    
    Description:

    Author:
        Bengart Zakhar
"""

import json
from bson.objectid import ObjectId

import functools
from datetime import datetime
from datetime import timedelta
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .baseview import get_col, write_log
from .authform import LoginForm, CredForm, SearchForm
import re
import os

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    
    if form.validate_on_submit():
        username = form.user.data
        password = form.pswd.data
        col = get_col('users')
        if not col.count(): dropuser()
        error = None
        user = col.find_one({'name': username})
        if (user is None) or (not check_password_hash(user['pswd'], password)):
            write_log(2121, src='AUTH', msg={'user': username} )
            flash('Неправильный логин или пароль')
            if user: count_try_auth(username)
            return render_template('auth/login.html', form=form)
        else:
            if user_is_block(user):
                form.blockuser = user['block'].strftime("%d.%m.%Y %H:%M:%S")
                return render_template('auth/login.html', form=form)
            session.clear()
            session['user_id'] = str(user['_id'])
            #write_log(2100, src='AUTH', msg={'user': username} )
            return redirect(url_for('index'))
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        col = get_col('users')
        user = col.find_one({'_id': ObjectId(user_id)})
        if user:
            g.user = user['name']
        else:
            g.user = None

@bp.route('/logout')
def logout():
    write_log(2101, src='AUTH')
    session.clear()
    return redirect(url_for('main.status', period='hour'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/auth/cred/')
@login_required
def cred():
    form = SearchForm()
    return render_template('auth/cred.html', form=form)

@bp.route('/auth/get_cred/')
@login_required
def get_cred():
    col = get_col('users')
    data = [ x for x in col.find().sort("name") ]
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)

def get_err_pwd(password : str)->list:
    errors = []
    if  len(password) <= 10:
        errors.append('Пароль должен быть длиннее 10 символов')
    if not re.search('^(?=.*?\d)', password):
        errors.append('Пароль должен содержать цифры')
    if not re.search('(?=.*?[a-z])', password):
        errors.append('Пароль должен содержать строчные буквы')
    if not re.search('(?=.*?[A-Z])', password):
        errors.append('Пароль должен содержать заглавные буквы')
    if not re.search('(?=.*?[^A-Za-z\s0-9])', password):
        errors.append('Пароль должен содержать спецсимволы')
    return errors

@bp.route('/auth/cred/add', methods=('GET', 'POST'))
@login_required
def cred_add():
    col = get_col('users')
    form = CredForm()
    if form.validate_on_submit():
        data = form.data
        if col.find( {'name': data['name'] }).count() > 0:
            flash('Имя пользователя существует')
            return render_template('auth/cred_edit.html', form=form)
        errors = get_err_pwd(data['pswd'])
        if len(errors):    
            _ = [flash(e) for e in errors]
            return render_template('auth/cred_edit.html', form=form)
        else:
            data['pswd'] = generate_password_hash(data['pswd'])
            data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
            col.insert_one(data)
            write_log(2124, src='AUTH', msg={ 'new_user': data['name'] })
            return redirect(url_for('auth.cred'))
    return render_template('auth/cred_edit.html', form=form)

@bp.route('/auth/cred/<string:id>/edit', methods=('GET', 'POST'))
@login_required
def cred_edit(id):
    col = get_col('users')
    doc = col.find_one({'_id': ObjectId(id)})    
    form = CredForm(data=doc)
    if form.validate_on_submit():
        data = form.data
        errors = get_err_pwd(data['pswd'])
        if len(errors):    
            _ = [flash(e) for e in errors]
            return render_template('auth/cred_edit.html', form=form)
        else:
            data['pswd'] = generate_password_hash(data['pswd'])
            data['pubdate'] = datetime.now().strftime("%Y-%m-%d")
            col.replace_one({'_id': ObjectId(id)}, data)
            write_log(2125, src='AUTH', msg={ 'user_change': data['name'] })
            return redirect(url_for('auth.cred'))
    return render_template('auth/cred_edit.html', form=form)

@bp.route('/auth/cred/<string:id>/del')
@login_required
def cred_del(id):
    col = get_col('users')
    doc = col.find_one({'_id': ObjectId(id)})
    if col.find().count() > 1:
        col.delete_one( {'_id': ObjectId(id)} )
        write_log(2126, src='LOG', msg={'user_deleted': doc['name']} )
    else:
        flash('Невозможно удалить последнего пользоваателя')
    return redirect(url_for('auth.cred'))


def count_try_auth(user):
    
    if session.get('try') is None:
        session['try'] = 1
    else:
        session['try'] += 1
        
    n = int(os.getenv('ZIEM_WEB_COUNT_TRY_AUTH', '3'))
    if session.get('try') < n: return
    
    session.pop('try')
    
    sec = int(os.getenv('ZIEM_WEB_BLOCKUSER_TIME', '60'))
    block = datetime.now() + timedelta(seconds=sec)
    get_col('users').update_one(
        {'name': user},
        { '$set': {'block': block}}
    )
    
def user_is_block(user):
    if user.get('block'):
        delta = user['block'] - datetime.now()
        return delta.total_seconds() > 0