import os
class BaseConfig:
        SECRET_KEY = os.environ.get('SECRET_KEY')   
        DEBUG =True
        SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')

class DevelopmentConfig(BaseConfig):
        SECRET_KEY = "LOCAL_SECRET_KEY"
        SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
class ProductionConfig(BaseConfig):
         DEBUG = False

config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig
}