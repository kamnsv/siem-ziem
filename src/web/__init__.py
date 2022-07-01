import os
import logging
from flask import Flask
from cryptography.fernet import Fernet
from logging.handlers import RotatingFileHandler

from flaskext.markdown import Markdown
from .baseview import clearweb, dropweb, dropuser
from .objview import obj_required
from flask_autoindex import AutoIndex

def start_app(port, host='0.0.0.0', 
              debug=True,
              dir_cert='/var/opt/ziem/cert'):
    
    print(f"host='{host}', port='{port}'")
    
    logging.basicConfig(
        handlers=[RotatingFileHandler('/var/log/ziem/user.log', 
                                      maxBytes=10000000, 
                                      backupCount=10)
                 ],
        level=logging.DEBUG if debug else logging.ERROR,
        format='%(asctime)s~%(levelname)s~%(message)s',
        datefmt='%m-%d-%Y %H:%M:%S'
    )

        
    app = create_app()
    
    app.run(host=host, port=port, 
            debug=debug, use_reloader=False, use_debugger=debug,
            ssl_context=(f'{dir_cert}/pub.crt', 
                         f'{dir_cert}/sec.key')
           )
    
def create_app(test_config=None):
    # create and configure the app
    
    app = Flask(__name__, instance_relative_config=True)
    
    with open('/etc/opt/ziem/ziem.k', 'rb') as f:
        key = f.read()
    fern_key = Fernet(key)
    with open("/etc/opt/ziem/db", 'r') as f:
        uri = f.readline()
    #with open("/etc/opt/ziem/pwd", 'r') as f:
     #   pwd = f.readline()
    with open('/etc/opt/ziem/web.k', 'rb') as f:
        web_key = f.read()
    app.config['SECRET_KEY'] = fern_key.decrypt(web_key)
    app.config["MONGO_URI"] = fern_key.decrypt(uri.encode()).decode()
    #app.config["MONGO_KEY"] = fern_key.decrypt(pwd.encode()).decode()
    app.config["PIP_REPO"] = '/opt/ziem/dist'
    app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 1}
     
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
    
    #from . import zsocket
    #app.register_blueprint(zsocket.bp)
    
    from . import zapi
    app.register_blueprint(zapi.bp)
    
    #Markdown(app)
    md = Markdown(app,
              extensions=["extra"],
             )
    # Auto indexing for PyPi
    files_index = AutoIndex(app, app.config["PIP_REPO"], add_url_rules=False)
    @app.route('/pypirepo')
    @app.route('/pypirepo/<path:path>')
    @obj_required
    def autoindex(path='.'):
        print(path)
        return files_index.render_autoindex(path)

    return app
