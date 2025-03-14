from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
db= SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'   #auto redirect to login page if user is not logged in

#factory function
def create_app(environment):
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(config[environment])
    login_manager.init_app(app)
    db.init_app(app)
    
    from . import models
    migrate.init_app(app, db)
    register_blueprints(app)
    return app
def register_blueprints(application):
    from app.main.routes import main_blueprint
    from app.auth.routes import auth_blueprint
    application.register_blueprint(auth_blueprint)
    application.register_blueprint(main_blueprint)
    