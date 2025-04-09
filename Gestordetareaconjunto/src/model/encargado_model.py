import sqlite3

class Encargado:
    def __init__(self, id=None, nombre="", contacto=None, detalles=None):
        self.id = id
        self.nombre = nombre
        self.contacto = contacto
        self.detalles = detalles

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "contacto": self.contacto,
            "detalles": self.detalles,
        }
def create_table(connection):
    with connection:
        print("Creando tabla de encargados...")
        connection.execute("""
            CREATE TABLE IF NOT EXISTS encargados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                contacto TEXT,
                detalles TEXT
            )
        """)
        print("Tabla encargados creada o ya existe.")

def insert_encargado(connection, encargado):
    with connection:
        cursor = connection.execute(
            "INSERT INTO encargados (nombre, contacto, detalles) VALUES (?, ?, ?)",
            (encargado.nombre, encargado.contacto, encargado.detalles),
        )
        return cursor.lastrowid

def get_all_encargados(connection):
    cursor = connection.execute("SELECT * FROM encargados")
    rows = cursor.fetchall()
    return [Encargado(*row) for row in rows]

def get_encargado_by_id(connection, id):
    cursor = connection.execute("SELECT * FROM encargados WHERE id = ?", (id,))
    row = cursor.fetchone()
    return Encargado(*row) if row else None

def update_encargado(connection, encargado):
    with connection:
        return connection.execute(
            "UPDATE encargados SET nombre = ?, contacto = ?, detalles = ? WHERE id = ?",
            (encargado.nombre, encargado.contacto, encargado.detalles, encargado.id),
        ).rowcount

def delete_encargado(connection, id):
    with connection:
        connection.execute("DELETE FROM tareas_encargado WHERE encargado_id = ?", (id,))
        return connection.execute("DELETE FROM encargados WHERE id = ?", (id,)).rowcount