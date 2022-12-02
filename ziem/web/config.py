from cryptography.fernet import Fernet
import pkg_resources

class Config:
    MONGO_URI = 'mongodb://zuser:123456@mongo:27017/?authSource=ziem&authMechanism=SCRAM-SHA-256'
    SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    FORMAT_LOG = '%(asctime)s ~ %(levelname)s ~ %(message)s'
    VERSION = pkg_resources.get_distribution('ziem').version
    
    try:
        with open('/etc/opt/ziem/ziem.k', 'rb') as f:
            key = f.read()
        fern_key = Fernet(key)
        with open("/etc/opt/ziem/db", 'r') as f:
            uri = f.readline()
        with open('/etc/opt/ziem/web.k', 'rb') as f:
            web_key = f.read()
        SECRET_KEY = fern_key.decrypt(web_key)
        MONGO_URI = fern_key.decrypt(uri.encode()).decode()
    except:pass

    PIP_REPO = '/opt/ziem/dist'
    SOCK_SERVER_OPTIONS = {'ping_interval': 1}
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER =  {'HTTP_X_FORWARDED_PROTO': 'https'}  
    
class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    print('development:', Config.MONGO_URI)
    
class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

cfg = [ProductionConfig, DevelopmentConfig]
