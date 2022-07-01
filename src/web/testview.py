"""
    ZIEM

    Description:

    Author:
        Bengart Zakhar
"""

import json
import socket
import asyncio
import traceback
from asyncua import Client

from flask import Blueprint, flash, g, redirect
from flask import render_template, request, session, url_for

from .authview import login_required
from .testform import JsonForm, WmiForm, FtpForm, NmapForm, OpcuaForm
from .testform import TestForm

import sys
sys.path.append("..")
from core.log_modules.wmi import DCOM, IEnum
from core.log_modules.ftp import get_log
from core.log_modules.netmap import ping as pinger
from core.log_modules.opcua import SubscriptionHandler, print_tree_node

import os

bp = Blueprint('test', __name__,
              static_folder=os.path.dirname(os.path.abspath(__file__)) + os.sep + 'static')

@bp.route('/test/syslog', methods=('GET', 'POST'))
@login_required
def syslog():
    form = JsonForm()
    if form.validate_on_submit():
        #data = json.loads(form.jdata.data)
        send_udp(form.jdata.data)
    return render_template('tst/syslog.html', form=form)

def send_udp(message):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 514
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))

@bp.route('/test/wmi/')
#@login_required
async def wmi():
    if g.user is None:
        return redirect(url_for('auth.login'))    
    form = WmiForm()
    return render_template('tst/wmi.html', form=form)

@bp.route('/test/get_wmi/', methods=('GET', 'POST'))
#@login_required
async def get_wmi():
    if g.user is None:
        return redirect(url_for('auth.login'))    
    result = ''
    form = WmiForm()
    ip = ip2 = form.ip.data
    username = form.username.data
    password = form.pswd.data
    query = "select * from __InstanceCreationEvent WHERE TargetInstance isa 'Win32_NTLogEvent'"
    result = ''
    dcom = ''
    iEnum = ''
    try:
        dcom = DCOM(ip, ip2, username, password)
        async with dcom:
            iEnum = IEnum(dcom.connection, query)
            async with iEnum:
                result = 'WMI доступен'
    except Exception as e:
        result = 'ОШИБКА:' + repr(e)
    return json.dumps(result, indent=4, default=str, ensure_ascii=False)


@bp.route('/test/ftp/')
#@login_required
async def ftp():
    if g.user is None:
        return redirect(url_for('auth.login'))    
    form = FtpForm()
    return render_template('tst/ftp.html', form=form)

@bp.route('/test/get_ftp/', methods=('GET', 'POST'))
#@login_required
async def get_ftp():
    if g.user is None:
        return redirect(url_for('auth.login'))    
    result = ''
    form = FtpForm()
    port = form.port.data
    ip = form.ip.data
    username = form.username.data
    pswd = form.pswd.data
    log = form.log.data
    PATH_LOG = '/tmp/'
    try:
        alerts = await asyncio.wait_for(
            get_log(ip, port, username, pswd, log, PATH_LOG),
            timeout=15)
        result = 'FTP достутен'
    except Exception as e:
        result = 'ОШИБКА:' + repr(e)
    return json.dumps(result, indent=4, default=str, ensure_ascii=False)

@bp.route('/test/nmap/')
@login_required
def nmap():
    form = NmapForm()
    result = ''
    return render_template('tst/nmap.html', form=form)

@bp.route('/test/get_nmap/', methods=('GET', 'POST'))
@login_required
def get_nmap():
    form = NmapForm()
    ip = form.ip.data
    port = form.port.data
    result = ''
    if ip:
        if port:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            try:
                s.connect((ip, int(port)))
                result = 'Порт открыт'
                s.close()
            except Exception as e:
                result = 'Порт закрыт:' + repr(e)
        else:
            result = ''
            res = asyncio.run(pinger(ip))
            if res == 0:
                result = 'Источник доступен'
            else:
                result = 'Источник недоступен'
    return json.dumps(result, indent=4, default=str, ensure_ascii=False)


@bp.route('/test/opcua/')
#@login_required
async def opcua():
    if g.user is None:
        return redirect(url_for('auth.login'))    
    form = OpcuaForm()
    return render_template('tst/opcua.html', form=form)


@bp.route('/test/get_opcua/', methods=('GET', 'POST'))
#@login_required
async def get_opcua():
    if g.user is None:
        return redirect(url_for('auth.login'))    
    result = ''
    form = OpcuaForm()
    ip = form.ip.data
    port = form.port.data
    username = form.username.data
    pswd = form.pswd.data
    log = form.log.data
    PATH_LOG = '/tmp/'
    if ip:
        node = ''
        queue_alerts = ''
        queue_rep = ''
        ip = form.ip.data
        username = form.username.data
        port = form.port.data
        pswd = form.pswd.data
        log = form.log.data
        url = 'opc.tcp://' + ip + ':' + port
        client = Client(url=url, timeout=10)
        try:
            async with client as c:
                result = 'OPCUA доступен'
                if log:
                    fname = os.path.join(bp.static_folder, 'yaml', f'opcua-{ip}-{port}.yml')
                    if not os.path.isfile(fname):
                        with open(fname, 'w') as f:
                            f.write('')
                        root = c.get_root_node()    
                        await print_tree_node(root, fname)
                else:
                    handler = SubscriptionHandler(ip, node, queue_alerts, queue_rep)
                    subscription = await c.create_subscription(1000, handler)
        except Exception as e:
            result = 'ОШИБКА:' + repr(e)
            
    return json.dumps(result, indent=4, default=str, ensure_ascii=False)



@bp.route('/test/get_opcae/', methods=('GET', 'POST'))
#@login_required
async def get_opcae():
    if g.user is None:
        return redirect(url_for('auth.login'))    
    result = ''
    form = OpcuaForm()
    ip = form.ip.data
    port = form.port.data
    username = form.username.data
    pswd = form.pswd.data
    if ip is None or port is None:
        return json.dumps(result, indent=4, default=str, ensure_ascii=False)

    url = 'opc.tcp://' + ip + ':' + port
    
    client = Client(url=url, timeout=30000)
    if username: client.set_user(username)
    if pswd: client.set_password(pswd)
    result = []
    try:
        async with client as c:
            root = c.get_root_node()
            await search_ae(root, result)
    except Exception as e:
            result = 'ОШИБКА:' + repr(e)
            
    return json.dumps(result, indent=4, default=str, ensure_ascii=False)

async def search_ae(root, ae):
    for ch in await root.get_children():
        if str(ch).endswith('.5000'): 
            try:
                val = await ch.get_value()
                # '{ ModuleId=(AeServer) Protocol=(OPCAE) Conditions=(Message) }'
                if 'Protocol=(OPCAE)' in val:
                    ae.append(str(root))
            except: pass 
        await search_ae(ch, ae)