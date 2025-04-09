import sqlite3
from .tarea_model import create_table as create_tarea_table
from .encargado_model import create_table as create_encargado_table
from .tarea_encargado_model import create_table as create_tarea_encargado_table
from .horario_model import create_table as create_horario_table
from .dia_horario_model import create_table as create_dia_horario_table
def check_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    print("Tablas en la base de datos:", tables)
def init_all_tables(db_path="src/model/database.db"):
    conn = sqlite3.connect(db_path)
    print("Conectado a la base de datos.")
    create_tarea_table(conn)
    create_encargado_table(conn)
    create_tarea_encargado_table(conn)
    create_horario_table(conn)
    create_dia_horario_table(conn)
    conn.commit()
    conn.close()
    print("Todas las tablas fueron creadas correctamente.")

def crear_tablas_si_no_existen(conn):
    create_tarea_table(conn)
    create_encargado_table(conn)
    create_tarea_encargado_table(conn)
    create_horario_table(conn)
    create_dia_horario_table(conn)

if __name__ == "__main__":
    init_all_tables()