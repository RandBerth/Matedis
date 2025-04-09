import sqlite3
import sys
import os
from model.db_config import get_db_connection
from model.init_tables import crear_tablas_si_no_existen
from model.init_tables import init_all_tables 
from model.init_tables import check_tables

db_path = "F:\\Matedis\\Gestordetareaconjunto\\src\\model\\database.db"

# Imprimir el path de la base de datos para ver si es correcto
print(f"Conectando a la base de datos en: {db_path}")

# Llamar a la función para crear todas las tablas
init_all_tables(db_path)

# Verificar tablas después de la inicialización
check_tables(db_path)

# Añadir src al path raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import flet as ft
from view.flet_ui.home import main

if __name__ == "__main__":
    ft.app(target=main)
    
def verificar_tablas(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar las tablas disponibles
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tablas disponibles:", tables)
    
    conn.close()

# Llama a esta función después de llamar a init_all_tables
verificar_tablas(db_path)
