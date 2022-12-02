"""
    ZIEM
    
    Description:
        This is Wiki for ZIEM
        Generated from MD files from Github
    Author:
        Bengart Zakhar
"""
import os
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for

from flaskext.markdown import Markdown

from .authview import login_required

bp = Blueprint('wiki', __name__)

@bp.route('/wiki/<string:page>/')
@login_required
def wiki_page(page):
    abs_path = os.path.dirname(os.path.realpath(__file__))              # абсолютный путь
    pwd = abs_path + '/templates/wiki'                                  # путь к wiki
    pages = [i for i in os.listdir(pwd) if os.path.isdir(f'{pwd}/{i}')] # папки страницы
    if page in pages:                                                   # запрашиваемая папка есть
        dir_path = pwd  + '/' + page
        data = {}
        for i in os.listdir(dir_path):
            fname = f'{dir_path}/{i}'
            path, ext = os.path.splitext(fname)
            if os.path.isdir(fname) or '.md' != ext: continue    # выбираем только md файлы
            name = os.path.basename(path).lower()
            with open(fname, 'r') as f:
                data[name] = f.read()
        return render_template('wiki/index.html', data=data)
    return render_template('error.html', title=404)