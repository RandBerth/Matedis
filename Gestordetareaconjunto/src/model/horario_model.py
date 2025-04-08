import sqlite3
from datetime import datetime

class Horario:
    def __init__(self, id=None, tarea_id=None, hora_inicio="", hora_fin="", fecha_inicio=None, fecha_fin=None):
        self.id = id
        self.tarea_id = tarea_id
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def to_dict(self):
        return {
            "id": self.id,
            "tarea_id": self.tarea_id,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
        }

def create_table(connection):
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS horarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarea_id INTEGER NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fin TEXT NOT NULL,
                fecha_inicio TEXT,
                fecha_fin TEXT,
                FOREIGN KEY (tarea_id) REFERENCES tareas (id) ON DELETE CASCADE
            )
        """)

def insert_horario(connection, horario):
    with connection:
        cursor = connection.execute(
            "INSERT INTO horarios (tarea_id, hora_inicio, hora_fin, fecha_inicio, fecha_fin) VALUES (?, ?, ?, ?, ?)",
            (horario.tarea_id, horario.hora_inicio, horario.hora_fin, horario.fecha_inicio, horario.fecha_fin)
        )
        return cursor.lastrowid

def get_by_tarea_id(connection, tarea_id):
    cursor = connection.execute("SELECT * FROM horarios WHERE tarea_id = ?", (tarea_id,))
    rows = cursor.fetchall()
    return [Horario(*row) for row in rows]

def get_all_horarios(connection):
    cursor = connection.execute("SELECT * FROM horarios")
    rows = cursor.fetchall()
    return [Horario(*row) for row in rows]

def get_by_id(connection, id):
    cursor = connection.execute("SELECT * FROM horarios WHERE id = ?", (id,))
    row = cursor.fetchone()
    return Horario(*row) if row else None

def delete_horario(connection, id):
    with connection:
        connection.execute("DELETE FROM dia_horario WHERE horario_id = ?", (id,))
        return connection.execute("DELETE FROM horarios WHERE id = ?", (id,)).rowcount