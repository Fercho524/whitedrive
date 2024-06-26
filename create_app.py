import os

# Config
from config import config

# Flask
from flask import Flask
from flask import render_template

# Login y Registros
from flask_login.login_manager import LoginManager

# Base de datos
from db import db
from models import *
from flask_migrate import Migrate

# Rutas
from routes import files_bp
from routes import auth_bp


def create_app(enviroment=config):
    # Servidor
    app = Flask(__name__)

    # Errores
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html', error=error), 404
    
    # Rutas
    app.register_blueprint(files_bp)
    app.register_blueprint(auth_bp)
    
    # Configuración
    app.config.from_object(enviroment)

    # Directorio de archivos
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Base de datos
    migrate = Migrate(app, db)

    with app.app_context():
        db.init_app(app)
        db.create_all()
    
    # Login y autenticación
    login_manager = LoginManager()

    login_manager.init_app(app)
    login_manager.login_view = 'Auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app