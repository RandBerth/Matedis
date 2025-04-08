
from model.tarea_model import Tarea
from model.db_config import get_db_connection

def obtener_tareas():
    conn = get_db_connection()
    tareas = Tarea.get_all(conn)
    conn.close()
    return tareas

def eliminar_tarea(id_tarea: int):
    conn = get_db_connection()
    Tarea.delete(conn, id_tarea)
    conn.commit()
    conn.close()
