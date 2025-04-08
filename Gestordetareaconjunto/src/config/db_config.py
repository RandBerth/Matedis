import sqlite3
import os

DB_NAME = 'database.db'
DB_PATH = r'C:\Users\Ronnie Herrera\Documents\GitHub\Matedis\Gestordetareaconjunto\src\model\database.db'

# Verifica si la carpeta de la base de datos existe, si no, la crea.
db_folder = os.path.dirname(DB_PATH)
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

TABLE_OUTLAWS = """
    CREATE TABLE IF NOT EXISTS outlaws(
        outlaw_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        reward REAL NOT NULL
    );
"""

# Intentar conectar a la base de datos
try:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(TABLE_OUTLAWS)
    connection.commit()
    connection.close()
    print("Base de datos y tabla creada correctamente.")
except sqlite3.OperationalError as e:
    print(f"Error al abrir o crear la base de datos: {e}")
