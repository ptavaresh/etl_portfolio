# mysql_module.py

import mysql.connector
from mysql.connector import Error
from config.config import mysql_config

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
