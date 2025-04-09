import sqlite3

DB_PATH = "db.sqlite"  # Asegúrate que esta ruta sea correcta para tu proyecto

def conectar():
    return sqlite3.connect(DB_PATH)


def agregar_encargado(nombre: str, correo: str):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO encargados (nombre, correo)
        VALUES (?, ?)
    """, (nombre, correo))

    conn.commit()
    conn.close()


def obtener_encargados():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, correo FROM encargados")
    encargados = cursor.fetchall()

    conn.close()
    return encargados


def eliminar_encargado(encargado_id: int):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM encargados WHERE id = ?", (encargado_id,))
    conn.commit()
    conn.close()


def actualizar_encargado(encargado_id: int, nuevo_nombre: str, nuevo_correo: str):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE encargados
        SET nombre = ?, correo = ?
        WHERE id = ?
    """, (nuevo_nombre, nuevo_correo, encargado_id))

    conn.commit()
    conn.close()
