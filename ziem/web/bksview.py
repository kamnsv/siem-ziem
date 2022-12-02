"""
    ZIEM
    
    Description:
        This is Books for ZIEM
    Author:
        Kamnev Sergey
"""
import os
from flask import flash, g, redirect
from flask import render_template, request, session, url_for
from datetime import datetime

from .baseview import get_col


def get_books():
    col = get_col('opt_bks')
    return { x['name']:x['desc'] for x in col.find() }
    
    
def menu_books():
    books = get_books()
    if not len(books): return ''
    menu = ''
    for k, v in books.items():
        menu += f'''
                <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                  <li>
                    <a 
                      class="nav-link rounded" 
                      href="/opt/bks_{k}/"
                      data-menu="bks"
                      aria-current="/opt/bks_{k}/">
                      {v}
                    </a>
                  </li>
                </ul>
                '''
    return f'''<li class="mb-1">
              <button class="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse" data-bs-target="#bks-collapse" aria-expanded="false" id="bks">
                <i class="fa-solid fa-book-open mx-3 fa-fw text-secondary"></i>
                Справочники
              </button>
              <div class="collapse ps-2" id="bks-collapse">
                {menu}
              </div>
            </li>
            '''

def str_to_date(str_date):
    if type(str_date) != str: 
        if str_date is None:
            return datetime.now()
        else:
            return str_date
    try:
        return datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S.%f')
    except: pass
    try:
        return datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
    except: pass
    try:
        return datetime.strptime(str_date, '%Y-%m-%dT%H:%M')
    except: pass
    try:
        return datetime.strptime(str_date, '%Y-%m-%d')
    except: pass
    