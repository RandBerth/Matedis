import sqlite3

class DiaHorario:
    def __init__(self, horario_id, dia):
        self.horario_id = horario_id
        self.dia = dia

    def to_dict(self):
        return {
            "horario_id": self.horario_id,
            "dia": self.dia,
        }

def create_table(connection):
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS dia_horario (
                horario_id INTEGER NOT NULL,
                dia TEXT NOT NULL,
                PRIMARY KEY (horario_id, dia),
                FOREIGN KEY (horario_id) REFERENCES horarios (id) ON DELETE CASCADE
            )
        """)

def insert_dia_horario(connection, dia_horario):
    with connection:
        return connection.execute(
            "INSERT INTO dia_horario (horario_id, dia) VALUES (?, ?)",
            (dia_horario.horario_id, dia_horario.dia)
        ).rowcount

def get_dias_by_horario_id(connection, horario_id):
    cursor = connection.execute(
        "SELECT dia FROM dia_horario WHERE horario_id = ?", (horario_id,)
    )
    return [row[0] for row in cursor.fetchall()]

def get_all_dia_horarios(connection):
    cursor = connection.execute("SELECT * FROM dia_horario")
    rows = cursor.fetchall()
    return [DiaHorario(*row) for row in rows]

def delete_by_horario_id(connection, horario_id):
    with connection:
        return connection.execute("DELETE FROM dia_horario WHERE horario_id = ?", (horario_id,)).rowcount