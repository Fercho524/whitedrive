import os
import shutil
from werkzeug.utils import secure_filename

# Flask
from flask import flash,request,make_response,url_for,redirect,render_template

# Base de datos
from db import db

# Rutas
from flask.blueprints import Blueprint

# Archivos
from flask import send_file

# Validación de formularios
from forms import LoginForm,RegistrationForm,UpdatePasswordForm

# Models
from models import *

# Login
from flask_login import login_user,logout_user,login_required,current_user

from config import config

# Rutas y Endpoints
files_bp = Blueprint('File',__name__,)
auth_bp = Blueprint('Auth',__name__,)
main_bp = Blueprint('Main',__name__,)

from utils import list_all_files,remove_full_directory


#######################################################################################
#           AUTENTICACIÓN
#######################################################################################


@auth_bp.route('/login',methods=["GET","POST"])
def login():
    # Obtención de los datos del formulario
    form = LoginForm()

    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()

        # Validación del email
        if not user:
            flash('Email does not exist', 'danger')

        # Validación de contraseña
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('File.list_files'))
        else:
            flash('Incorrect Password', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Obtención de los datos del formulario
    form = RegistrationForm()

    if form.validate_on_submit():
        # Validación del email
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('User already exists', 'error')
            return redirect(url_for('Auth.login'))
        
        # Creación de un nuevo usuario
        new_user = Usuario(
            username=form.username.data, 
            email=form.email.data
        )
        # Se guarda la contraseña encriptada
        new_user.set_password(form.password.data)

        # Se guarda el usuario
        db.session.add(new_user)
        db.session.commit()

        # Crea su carpeta personal
        if not os.path.exists(new_user.user_folder):
            os.mkdir(new_user.user_folder)

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('Auth.login'))
    
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Auth.login'))


@auth_bp.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)


@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Eliminar la carpeta de subidas del usuario en el sistema de archivos
    if os.path.exists(current_user.user_folder):
        shutil.rmtree(current_user.user_folder)

    # Eliminar todos los registros relacionados con el usuario en la base de datos
    Archivo.query.filter_by(id_usuario=current_user.id).delete()
    Usuario.query.filter_by(id=current_user.id).delete()
    db.session.commit()

    # Cerrar la sesión del usuario
    logout_user()

    flash('Your account has been deleted successfully.', 'success')
    return redirect(url_for('Auth.login'))


@auth_bp.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()

    if form.new_password.data != form.confirm_new_password.data:
        flash('New passwords do not match.', 'danger')
    
    if form.validate_on_submit():
        user = Usuario.query.get(current_user.id)
        
        if user.check_password(form.current_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated successfully.', 'success')
            return redirect(url_for('Auth.account'))
        else:
            flash('Current password is incorrect.', 'danger')

    return render_template('update_password.html', form=form)



#######################################################################################
#           RECURSOS Y ARCHIVOS
#######################################################################################


@files_bp.route('/',methods=["GET","POST"])
@login_required
def list_files():
    # Get the current dir from cookies or form
    if request.method == 'POST':
        currentdir = request.form.get('filepath')
    else:
        currentdir = request.cookies.get('currentdir', '')

    # If currentdir is none or invalid
    if currentdir == "" or currentdir == "/":
        currentdir_path = current_user.user_folder
        currentdir = ""
    else:
        currentdir_path = os.path.join(current_user.user_folder, currentdir)

    # If dir don't exists, the default dir will be user folder
    if not os.path.exists(currentdir_path):
        currentdir_path = current_user.user_folder
        currentdir = ""
    
    # If you are out of your dir
    if not currentdir_path.startswith(current_user.user_folder):
        flash('No tienes acceso a esta ruta', 'danger')
        return redirect(url_for('File.list_files'))

    # Get all files from current path
    files = Archivo.query.filter_by(filepath=currentdir_path, id_usuario=current_user.id).all()
    resp = make_response(render_template('list_files.html', files=files, currentdir=currentdir))
    resp.set_cookie('currentdir', currentdir)

    return resp


@files_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        current_folder = request.form.get('subfolder')
        
        if current_folder == "" or current_folder == "/":
            current_folder_path = current_user.user_folder
        else:
            current_folder_path = os.path.join(current_user.user_folder, current_folder)

        if not os.path.exists(current_folder_path):
            flash('La ruta específicada no existe', 'danger')
            return redirect(url_for('File.list_files'))

        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_folder_path, filename)
            file.save(file_path)

            subfolder_path, file_name = os.path.split(file_path)

            nuevo_archivo = Archivo(
                id_usuario=current_user.id,
                filename=file_name,
                filepath=subfolder_path,
                file_type='file'
            )
            db.session.add(nuevo_archivo)
            db.session.commit()

            flash('Archivo subido exitosamente', 'success')
            return redirect(url_for('File.list_files'))
        else:
            flash('Por favor, proporciona un archivo', 'danger')

    return redirect(url_for('File.list_files'))


@files_bp.route('/files/download/<int:file_id>', methods=['GET'])
@login_required
def download_file(file_id):
    file = Archivo.query.get_or_404(file_id)
    
    if file.file_type == "file":
        filename = os.path.join(file.filepath, file.filename)
        return send_file(filename, as_attachment=True)
    else:
        directory_path = os.path.join(file.filepath, file.filename)
        
        if not directory_path:
            flash('Ruta del directorio no proporcionada', 'danger')
            return redirect(url_for('File.list_files'))

        if not directory_path.startswith(current_user.user_folder):
            flash('No tienes acceso a esta ruta', 'danger')
            return redirect(url_for('File.list_files'))

        # Genera el nombre del archivo zip
        zip_filename = os.path.basename(directory_path)
        zip_path = os.path.join(current_user.user_folder, zip_filename)
        
        print(zip_filename)
        print(zip_path)

        try:
            shutil.make_archive(zip_path, 'zip',directory_path)
            return send_file(zip_path+'.zip', as_attachment=True)
        except Exception as e:
            flash(f'Error al crear el archivo zip: {str(e)}', 'danger')
            return redirect(url_for('File.list_files'))
        finally:
            if os.path.exists(zip_filename+'.zip'):
                os.remove(zip_filename+'.zip')


@files_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = Archivo.query.get_or_404(file_id)

    if file.file_type == 'file':
        try:
            os.remove(os.path.join(file.filepath,file.filename))
        except OSError as e:
            flash(f'Error al eliminar el archivo: {str(e)}', 'danger')
            return redirect(url_for('File.list_files'))

        db.session.delete(file)
        db.session.commit()

        flash('File successfully deleted', 'success')
        return redirect(url_for('File.list_files'))
    else:
        dirname = os.path.join(os.path.join(file.filepath,file.filename))
        
        # Eliminación en el sistema de archivos
        remove_full_directory(dirname)

        # Eliminación en la base de datos
        archivos = Archivo.query.filter_by(filepath=dirname).all()
        
        try:
            for archivo in archivos:
                db.session.delete(archivo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        db.session.delete(file)
        db.session.commit()

        flash('Directory successfully deleted', 'success')
        return redirect(url_for('File.list_files'))


@files_bp.route('/mkdir', methods=['GET', 'POST'])
@login_required
def create_directory():
    if request.method == 'POST':
        current_folder = request.form.get('currentdir')
        foldername = request.form.get('foldername')

        if current_folder == "" or current_folder == "/":
            current_folder_path = current_user.user_folder
        else:
            current_folder_path = os.path.join(current_user.user_folder, current_folder)

        if not os.path.exists(current_folder_path):
            flash('La ruta específicada no existe', 'danger')
            return redirect(url_for('File.list_files'))

        if foldername:
            folder_path = os.path.join(current_folder_path, foldername)

            if os.path.exists(folder_path):
                flash('El directorio ya existe', 'danger')
                return redirect(url_for('File.list_files'))

            os.mkdir(folder_path)
            subfolder_path, folder_name = os.path.split(folder_path)

            nuevo_directorio = Archivo(
                id_usuario=current_user.id,
                filename=folder_name,
                filepath=subfolder_path,
                file_type='folder'
            )
            db.session.add(nuevo_directorio)
            db.session.commit()

            flash('Directorio creado exitosamente', 'success')
            return redirect(url_for('File.list_files'))
        else:
            flash('Por favor, proporciona un nombre para el directorio', 'danger')

    return redirect(url_for('File.list_files'))


@files_bp.route('/rename/<int:file_id>', methods=['POST'])
@login_required
def rename_file(file_id):
    new_name = request.form.get('new_name')
    file = Archivo.query.get_or_404(file_id)

    if not new_name:
        flash('Please provide a new name', 'danger')
        return redirect(url_for('File.list_files'))

    old_path = os.path.join(file.filepath,file.filename)
    new_name = secure_filename(new_name)
    new_path = os.path.join(file.filepath, new_name)
    
    print(old_path)
    print(new_name)
    print(new_path)

    try:
        os.rename(old_path, new_path)
    except OSError as e:
        flash(f'Error al renombrar el archivo/directorio: {str(e)}', 'danger')
        return redirect(url_for('File.list_files'))

    file.filename = new_name
    file.filepath = file.filepath
    db.session.commit()

    flash('File/directory renamed successfully', 'success')
    return redirect(url_for('File.list_files'))



@files_bp.route('/copy/<int:file_id>', methods=['POST'])
@login_required
def copy_file(file_id):
    destination = request.form.get('destination')
    file = Archivo.query.get_or_404(file_id)

    if destination == "..":
        newpath,dirs =  os.path.split(file.filepath)
        print(newpath)
        print(dirs)
        destination = newpath

    destination = os.path.join(current_user.user_folder,destination)
    

    if not destination:
        flash('Please provide a destination directory', 'danger')
        return redirect(url_for('File.list_files'))

    if not destination.startswith(current_user.user_folder):
        flash('No tienes acceso a esta ruta', 'danger')
        return redirect(url_for('File.list_files'))

    if not os.path.exists(destination):
        flash('Destination directory does not exist', 'danger')
        return redirect(url_for('File.list_files'))
    

    old_path = os.path.join(file.filepath, file.filename)
    new_path = os.path.join(destination, file.filename)

    try:
        if file.file_type == 'file':
            shutil.copy2(old_path, new_path)
        else:
            shutil.copytree(old_path, new_path)
    except OSError as e:
        flash(f'Error copying file/directory: {str(e)}', 'danger')
        return redirect(url_for('File.list_files'))

    new_file = Archivo(
        id_usuario=current_user.id,
        filename=file.filename,
        filepath=destination,
        file_type=file.file_type
    )
    db.session.add(new_file)
    db.session.commit()

    flash('File/directory copied successfully', 'success')
    return redirect(url_for('File.list_files'))

@files_bp.route('/move/<int:file_id>', methods=['POST'])
@login_required
def move_file(file_id):
    destination = request.form.get('destination')
    file = Archivo.query.get_or_404(file_id)

    if destination == "..":
        newpath,dirs =  os.path.split(file.filepath)
        print(newpath)
        print(dirs)
        destination = newpath

    destination = os.path.join(current_user.user_folder,destination)

    if not destination:
        flash('Please provide a destination directory', 'danger')
        return redirect(url_for('File.list_files'))

    if not os.path.exists(destination):
        flash('Destination directory does not exist', 'danger')
        return redirect(url_for('File.list_files'))

    if not os.path.exists(destination):
        flash('Destination directory does not exist', 'danger')
        return redirect(url_for('File.list_files'))

    old_path = os.path.join(file.filepath, file.filename)
    new_path = os.path.join(destination, file.filename)

    try:
        shutil.move(old_path, new_path)
    except OSError as e:
        flash(f'Error moving file/directory: {str(e)}', 'danger')
        return redirect(url_for('File.list_files'))

    file.filepath = destination
    db.session.commit()

    flash('File/directory moved successfully', 'success')
    return redirect(url_for('File.list_files'))