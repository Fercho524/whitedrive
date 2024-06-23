import os
from flask_login import UserMixin

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash 

from db import db

from config import config


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'

    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    username = db.Column(
        db.String(128), 
        unique=True, 
        nullable=False
    )
    email = db.Column(
        db.String(128), 
        unique=True, 
        nullable=False
    )
    password_hash = db.Column(
        db.String(256), 
        nullable=False
    )
    user_folder = db.Column(
        db.String(256),
        nullable=False,
        default=""
    )

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.user_folder = os.path.join(config.UPLOAD_FOLDER, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Archivo(db.Model):
    __tablename__ = 'archivo'

    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    id_usuario = db.Column(
        db.Integer, 
        db.ForeignKey('usuario.id'), 
        nullable=False
    )
    filename = db.Column(
        db.String(128), 
        nullable=False
    )
    filepath = db.Column(
        db.String(256), 
        nullable=False
    )
    file_type = db.Column(
        db.String(10), 
        nullable=False
    )
    uploaded_at = db.Column(
        db.DateTime(),
        nullable=False,
        default=db.func.current_timestamp()
    )