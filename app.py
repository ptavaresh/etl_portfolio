# main.py

from modules.postgres_module import fetch_postgres_data
from modules.mysql_module import insert_mysql_data

if __name__ == "__main__":
    data = fetch_postgres_data()
    if data:
        insert_mysql_data(data)
    else:
        print("No se obtuvieron datos de PostgreSQL.")
