"""
    ZIEM 
    
    Description:

    Author:
        Kamnev Sergey
"""

import json
import time
from threading import Thread # потоки

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for
from flask_sock import Sock

from .baseview import get_col, write_log, get_db

bp = Blueprint('ws', __name__)

sock = Sock(bp)

clients = set()


@sock.route('/ws')
def webscoket(ws):
    
    while True:
        q = ws.receive()
        clients.add((ws, q, g.user))
        ini_subscrub(q)

# Subscrub 
def ini_subscrub(name):    
    col = get_col(name)
    with col.watch(full_document='updateLookup') as change_stream: #full_document='updateLookup'
        for change in change_stream:
            send_client(name, change)
    
      
def send_client(query, msg):
     while True:
        for i, client in enumerate(list(clients)):
            s, q, u = client
            if q != query: continue
            try:
                s.send(msg)
            except: 
                clients.remove(client)
        time.sleep(1)   
    
#Thread(target=send_client, name='ZIEM-WS').start()    
