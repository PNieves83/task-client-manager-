"""
Funciones de conexión e inicialización de la tabla de la base de datos  SQLite.

Proporciona la conexión a la base de datos y la creación automática
de las tablas necesarias para el funcionamiento de la aplicación.
"""
import sqlite3
from sqlite3 import Error
import os
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "tasks.db")

def create_connection() -> Optional[sqlite3.Connection]:
    """
    Crea y retorna una conecxión a la base de datos SQLite.
    
    Crea el directorio 'data'si no existe. Retorna None si falla.
    
    Returns:
        sqlite3.Connection | None: Conexión a la base de datos o None.
    """
    try:
        data_dir = os.path.join(BASE_DIR, "data")
        os.makedirs(data_dir, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None
    
def create_tables() -> None:
    """
    Crea las tablas clients, tasks y meetings si no existen.
    
    Ejecuta sentencias CREATE TABLE IF NOT EXISTS para inicializar
    el esquemade la base de datos con sus relaciones y columnas.
    """
    conn = create_connection()
    if conn is None:
        print("[DB ERROR] No se pudo crear la conexión.")
        return
    
    cursor = conn.cursor()
    
    # CLIENTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            company TEXT,
            category TEXT,
            source TEXT,
            preferred_method TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            task_status TEXT NOT NULL,
            start_date TEXT NOT NULL,
            deadline TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            meeting TEXT NOT NULL,
            meeting_date TEXT NOT NULL,
            payment_status TEXT NOT NULL,
            total REAL DEFAULT 0,
            paid REAL DEFAULT 0,
            method TEXT,
            payment_date TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("[DB] Tablas actualizadas correctamente.")
    
if __name__ == "__main__":
    create_tables()