from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField

from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField(
        label='Correo electrónico', 
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        label='Contraseña', 
        validators=[
            DataRequired()
        ]
    )
    remember_me = BooleanField(
        label='Recordarme'
    )
    submit = SubmitField(
        label='Iniciar sesión'
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        label='Nombre de usuario', 
        validators=[
            DataRequired(), 
            Length( min=4, max=20)
        ]
    )
    email = StringField(
        label='Correo electrónico', 
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        label='Contraseña', 
        validators=[
            DataRequired()
        ]
    )
    confirm_password = PasswordField(
        label='Repetir contraseña', 
        validators=[
            DataRequired(), 
            EqualTo('password')
        ]
    )
    submit = SubmitField(
        label='Registrarse'
    )


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')