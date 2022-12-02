#!/usr/local/lib/python3.9

import os
import logging
from flask import Flask, Markup
from flask import render_template
from logging.handlers import RotatingFileHandler
from . import config
from flaskext.markdown import Markdown
from .baseview import clearweb, dropweb, dropuser
from .objview import obj_required
from flask_autoindex import AutoIndex


def start_app(host, port, certs, debug):
    
    #print(f"host='{host}', port='{port}', ", 'ssl:', certs is not None)
    
    logging.basicConfig(
        handlers=[RotatingFileHandler('/var/log/ziem/user.log', 
                                      maxBytes=10000000, 
                                      backupCount=10)
                 ],
        level=logging.DEBUG if debug else logging.ERROR,
        format=os.environ['ZIEM_FORMAT_LOG']
    )

    app = create_app(int(os.environ['ZIEM_CENTER']), debug)
    #if certs is None: certs ='adhoc'
    
    try:
        if certs is None:
            #app.wsgi_app = ProxyFix(app.wsgi_app)
            app.run(host=host, port=port,
                debug=debug, use_reloader=False, use_debugger=debug)
        else:
            app.run(host=host, port=port, ssl_context=certs,
                debug=debug, use_reloader=False, use_debugger=debug)
    except Exception as e:
        print('start_app:', e)
    
def create_app(center=False, debug=False):
    # create and configure the app

    os.environ['ZIEM_CENTER'] = ['0', '1', '2'][center]
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.cfg[debug])
    
    os.environ['ZIEM_FORMAT_LOG'] = app.config['FORMAT_LOG']
    os.environ['ZIEM_VERSION'] = app.config['VERSION']
    os.environ['ZIEM_WEBMODE'] = app.config['FLASK_ENV']
    
    from . import authview
    app.register_blueprint(authview.bp)

    from . import mainview
    app.register_blueprint(mainview.bp)
    app.add_url_rule('/', endpoint='index')

    from . import optview
    app.register_blueprint(optview.bp)
    
    from . import objview
    app.register_blueprint(objview.bp)

    from . import logview
    app.register_blueprint(logview.bp)

    from . import norview
    app.register_blueprint(norview.bp)

    from . import corview
    app.register_blueprint(corview.bp)

    from . import repview
    app.register_blueprint(repview.bp)

    from . import wikiview
    app.register_blueprint(wikiview.bp)

    from . import testview
    app.register_blueprint(testview.bp)

    from . import setview
    app.register_blueprint(setview.bp)
    
    from . import jouview
    app.register_blueprint(jouview.bp)
    
    #from . import zsocket
    #app.register_blueprint(zsocket.bp)
    
    from . import zapi
    app.register_blueprint(zapi.bp)
    
    #Markdown(app)
    md = Markdown(app, extensions=["extra"],)
    
    if True or '1' == os.environ["ZIEM_CENTER"]:
        # Auto indexing for PyPi
        files_index = AutoIndex(app, app.config["PIP_REPO"], add_url_rules=False)
        @app.route('/pypirepo')
        @app.route('/pypirepo/')
        @app.route('/pypirepo/<path:path>')
        #@obj_required
        def autoindex(path='.'):
            return files_index.render_autoindex(path)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', title=404)
    
    
    # Переменные окружения
    @app.context_processor
    def processor_env():
        def env(key):
            val = os.getenv(key)
            if val.lower() in ('false', 'off', 'no', None):
                return False
            if val.lower() in ('true', 'on', 'y', 'yes'):
                return True
            if val.isdigit():
                return int(val)
            return os.getenv(key)
        return dict(env=env)
    
      
    # Динамическое меню   
    from .bksview import menu_books
    from .optview import menu_systems
    from .jouview import menu_logs, format_line
    
    @app.context_processor
    def processor_menu():
        
        # Справочники  
        def books():
            return Markup(menu_books())
        
        # Системы
        def systems():
            return Markup(menu_systems())
        
        # Журналы 
        def jouranls():
            return Markup(menu_logs())
        
        # Статус ядра
        def status():
            return os.popen('systemctl is-active ziemcored').read().strip()
        
        return dict(
            books=books,
            systems=systems,
            jouranls=jouranls,
            status=status
                   )
    
    # Фильтры
    @app.template_filter()
    def format_log(item):
        return Markup(format_line(item))

    return app