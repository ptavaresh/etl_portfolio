# postgres_module.py

import psycopg2
from config.config import pg_config


def fetch_postgres_data():
    try:
        conn = psycopg2.connect(**pg_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, edad, departamento FROM empleados")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        print("Datos recolectados de PostgreSQL")
        return rows
    except Exception as e:
        print(f"Error al conectar con PostgreSQL: {e}")
        return None
