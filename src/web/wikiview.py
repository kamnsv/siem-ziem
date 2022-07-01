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

#    for filename in os.listdir(wiki):
#       with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
#          # do your stuff


@bp.route('/wiki/home/')
@login_required
def home():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/templates/wiki/Home.md", "r") as f:
        md = f.read()
    return render_template('wiki/home.html', md=md)

@bp.route('/wiki/log/')
@login_required
def log():
    data = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pwd = dir_path + '/templates/wiki/log'
    for filename in os.listdir(pwd):
        if os.path.isdir(os.path.join(pwd, filename)): continue
        with open(os.path.join(pwd, filename), 'r') as f:
            md = f.read()
            data[filename.split('.')[0]] = md
    return render_template('wiki/log.html', data=data)

@bp.route('/wiki/nor/')
@login_required
def nor():
    data = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pwd = dir_path + '/templates/wiki/nor'
    for filename in os.listdir(pwd):
        with open(os.path.join(pwd, filename), 'r') as f:
            md = f.read()
            data[filename.split('.')[0]] = md
    return render_template('wiki/nor.html', data=data)

@bp.route('/wiki/cor/')
@login_required
def cor():
    data = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pwd = dir_path + '/templates/wiki/cor'
    for filename in os.listdir(pwd):
        with open(os.path.join(pwd, filename), 'r') as f:
            md = f.read()
            data[filename.split('.')[0]] = md
    return render_template('wiki/cor.html', data=data)

@bp.route('/wiki/adm/')
@login_required
def adm():
    data = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pwd = dir_path + '/templates/wiki/adm'
    for filename in os.listdir(pwd):
        with open(os.path.join(pwd, filename), 'r') as f:
            md = f.read()
            data[filename.split('.')[0]] = md
    return render_template('wiki/adm.html', data=data)
