import psycopg2
import mysql.connector
from mysql.connector import Error

# Configuración de PostgreSQL
pg_config = {
    'dbname': 'postgres_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'postgres',
    'port': '5432'
}

# Configuración de MySQL
mysql_config = {
    'database': 'testdb',
    'user': 'root',
    'password': 'rootpassword',
    'host': 'mysql',
    'port': '3306'
}

def fetch_postgres_data():
    try:
        conn = psycopg2.connect(**pg_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, edad, departamento FROM empleados")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        print(f"data collected")
        return rows
    except Exception as e:
        print(f"Error al conectar con PostgreSQL: {e}")
        return None

def insert_mysql_data(data):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO empleados (id, nombre, edad, departamento)
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
        print("Datos insertados en MySQL")
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")

if __name__ == "__main__":
    data = fetch_postgres_data()
    if data:
        insert_mysql_data(data)
    else:
        print("No se obtuvieron datos de PostgreSQL.")
