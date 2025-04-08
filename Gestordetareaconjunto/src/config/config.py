import os
from dbconfig import DB_PATH

def db_exists():
    return os.path.exists(DB_PATH)

def db_create():
    if not db_exists():
        # Llamar a la lógica de dbconfig.py para crear la base de datos
        import dbconfig
