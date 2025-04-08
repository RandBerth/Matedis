import sqlite3

class Tarea:
    def __init__(self, id=None, nombre="", tipo="", descripcion=None, lugar_id=None, tarea_padre_id=None, color="#FFFF00", estado=None):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion
        self.lugar_id = lugar_id
        self.tarea_padre_id = tarea_padre_id
        self.color = color
        self.estado = estado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "lugar_id": self.lugar_id,
            "tarea_padre_id": self.tarea_padre_id,
            "color": self.color,
            "estado": self.estado
        }
    @staticmethod
    def get_all(connection):
        cursor = connection.execute("SELECT * FROM tareas")
        rows = cursor.fetchall()
        return [Tarea(*row) for row in rows]

def create_table(connection):
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT,
                lugar_id INTEGER,
                tarea_padre_id INTEGER,
                color TEXT NOT NULL,
                estado TEXT
            )
        """)

def insert_tarea(connection, tarea):
    with connection:
        cursor = connection.execute(
            "INSERT INTO tareas (nombre, tipo, descripcion, lugar_id, tarea_padre_id, color, estado) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (tarea.nombre, tarea.tipo, tarea.descripcion, tarea.lugar_id, tarea.tarea_padre_id, tarea.color, tarea.estado)
        )
        return cursor.lastrowid

def get_all_tareas(connection):
    cursor = connection.execute("SELECT * FROM tareas")
    rows = cursor.fetchall()
    return [Tarea(*row) for row in rows]

def get_tarea_by_id(connection, id):
    cursor = connection.execute("SELECT * FROM tareas WHERE id = ?", (id,))
    row = cursor.fetchone()
    return Tarea(*row) if row else None

def update_tarea(connection, tarea):
    with connection:
        return connection.execute(
            "UPDATE tareas SET nombre = ?, tipo = ?, descripcion = ?, lugar_id = ?, tarea_padre_id = ?, color = ?, estado = ? WHERE id = ?",
            (tarea.nombre, tarea.tipo, tarea.descripcion, tarea.lugar_id, tarea.tarea_padre_id, tarea.color, tarea.estado, tarea.id)
        ).rowcount

def delete_tarea(connection, id):
    with connection:
        connection.execute("DELETE FROM tareas_encargado WHERE tarea_id = ?", (id,))
        return connection.execute("DELETE FROM tareas WHERE id = ?", (id,)).rowcount