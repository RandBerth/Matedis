import sqlite3

DB_PATH = "F:\Matedis\Gestordetareaconjunto\src\model\database.db"  
def conectar():
    return sqlite3.connect(DB_PATH)


def agregar_encargado(nombre: str, contacto: str):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO encargados (nombre, contacto)
        VALUES (?, ?)
    """, (nombre, contacto))

    conn.commit()
    conn.close()


def obtener_encargados():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, contacto FROM encargados")
    encargados = cursor.fetchall()

    conn.close()
    return encargados


def eliminar_encargado(encargado_id: int):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM encargados WHERE id = ?", (encargado_id,))
    conn.commit()
    conn.close()


def actualizar_encargado(encargado_id: int, nuevo_nombre: str, nuevo_contacto: str):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE encargados
        SET nombre = ?, contacto = ?
        WHERE id = ?
    """, (nuevo_nombre, nuevo_contacto, encargado_id))

    conn.commit()
    conn.close()
