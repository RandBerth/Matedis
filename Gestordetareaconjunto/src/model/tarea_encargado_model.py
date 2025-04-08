import sqlite3
from .encargado_model import get_encargado_by_id
from .tarea_model import get_tarea_by_id

class TareaEncargado:
    def __init__(self, tarea_id, encargado_id):
        self.tarea_id = tarea_id
        self.encargado_id = encargado_id

    def to_dict(self):
        return {
            "tarea_id": self.tarea_id,
            "encargado_id": self.encargado_id,
        }

def create_table(connection):
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tareas_encargado (
                tarea_id INTEGER NOT NULL,
                encargado_id INTEGER NOT NULL,
                PRIMARY KEY (tarea_id, encargado_id),
                FOREIGN KEY (tarea_id) REFERENCES tareas (id) ON DELETE CASCADE,
                FOREIGN KEY (encargado_id) REFERENCES encargados (id) ON DELETE CASCADE
            )
        """)

def insert_tarea_encargado(connection, relacion):
    with connection:
        return connection.execute(
            "INSERT INTO tareas_encargado (tarea_id, encargado_id) VALUES (?, ?)",
            (relacion.tarea_id, relacion.encargado_id)
        ).rowcount

def get_encargados_by_tarea_id(connection, tarea_id):
    cursor = connection.execute(
        "SELECT encargado_id FROM tareas_encargado WHERE tarea_id = ?", (tarea_id,)
    )
    encargados = []
    for row in cursor.fetchall():
        encargado = get_encargado_by_id(connection, row[0])
        if encargado:
            encargados.append(encargado)
    return encargados

def get_tareas_by_encargado_id(connection, encargado_id):
    cursor = connection.execute(
        "SELECT tarea_id FROM tareas_encargado WHERE encargado_id = ?", (encargado_id,)
    )
    tareas = []
    for row in cursor.fetchall():
        tarea = get_tarea_by_id(connection, row[0])
        if tarea:
            tareas.append(tarea)
    return tareas

def delete_by_tarea_id(connection, tarea_id):
    with connection:
        return connection.execute("DELETE FROM tareas_encargado WHERE tarea_id = ?", (tarea_id,)).rowcount

def delete_by_encargado_id(connection, encargado_id):
    with connection:
        return connection.execute("DELETE FROM tareas_encargado WHERE encargado_id = ?", (encargado_id,)).rowcount