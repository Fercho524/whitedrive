import shutil
import os

def list_all_files(directorio):
    """
    Lista de manera recursiva todos los archivos contenidos en el directorio especificado.

    Args:
    - directorio (str): Ruta del directorio a listar.

    Returns:
    - archivos (list): Lista con las rutas completas de todos los archivos encontrados.
    """
    archivos = []
    
    # Recorre todos los elementos (archivos y directorios) dentro del directorio
    for elemento in os.listdir(directorio):
        ruta_elemento = os.path.join(directorio, elemento)
        
        # Si es un archivo, añadirlo a la lista
        if os.path.isfile(ruta_elemento):
            archivos.append(ruta_elemento)
        
        # Si es un directorio, llamar recursivamente a la función para listar sus archivos
        elif os.path.isdir(ruta_elemento):
            archivos.extend(list_all_files(ruta_elemento))
    
    return archivos


def remove_full_directory(directorio):
    """
    Elimina de forma recursiva todos los elementos (archivos y directorios) dentro del directorio especificado.
    
    Args:
    - directorio (str): Ruta del directorio que se desea eliminar.
    
    """
    # Verificar que el directorio existe
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe.")
        return
    
    # Iterar sobre los elementos en el directorio
    for root, dirs, files in os.walk(directorio, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)  # Eliminar archivo
                print(f"Archivo eliminado: {file_path}")
            except OSError as e:
                print(f"No se pudo eliminar el archivo {file_path}: {e}")
        
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                shutil.rmtree(dir_path)  # Eliminar directorio y sus contenidos
                print(f"Directorio eliminado recursivamente: {dir_path}")
            except OSError as e:
                print(f"No se pudo eliminar el directorio {dir_path}: {e}")

    # Eliminar el directorio raíz
    try:
        shutil.rmtree(directorio)
        print(f"Directorio raíz eliminado recursivamente: {directorio}")
    except OSError as e:
        print(f"No se pudo eliminar el directorio raíz {directorio}: {e}")
