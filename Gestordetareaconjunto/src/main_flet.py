import sys
import os
from model.db_config import get_db_connection
from model.init_tables import crear_tablas_si_no_existen

# Crear las tablas si no existen
conn = get_db_connection()
crear_tablas_si_no_existen(conn)
conn.close()  # <- Importante cerrar la conexión

# Añadir src al path raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import flet as ft
from view.flet_ui.home import main

if __name__ == "__main__":
    ft.app(target=main)
