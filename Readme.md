# White Drive

## Funcionalidades
- Registrarse
- Iniciar sesión
- Cerrar sesión
- Tener una carpeta por usuario
- Borrar cuenta
- Ver información de la cuenta
- Subir archivo
- Descargar archivo
- Crear directorio
- Eliminar directorio de forma recursiva
- Eliminar archivo
- Renombrar archivo y directorio
- Descargar directorio como .zip
- Mover y copiar archivos
- Actualizar contraseña


## Funcionalidades que faltaron
- Click izquierdo a archivos y directorios para ver detalles y hacer acciones
- Copiar
- Mover


## Instalación

```sh
pip install flask flask-migrate flask-login python-dotenv flask-wtf flask-migrate psycopg2-binary Flask Werkzeug alembic SQLAlchemy Flask-SQLAlchemy
```

## Creación de la base de datos

```sh
flask db init
flask db migrate -m "Setup"
flask db upgrade
```

## Correr el servidor

```sh
python run.py
```

## Configuración

Por defecto la configuración está en desarrollo, pero esta se puede cambiar en el archivo .flaskenv, por defecto trae la siguiente configuración:

```
CONFIG=development
DBPASSWORD=524835
DBHOST=localhost
DBNAME=wdrive
UPLOADS_FOLDER=/home/fercho/Downloads/uploads
```