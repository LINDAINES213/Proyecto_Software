'''import psycopg2
from psycopg2 import DatabaseError
from decouple import config
import time

def get_connection():
    max_retries = 3
    retry_delay = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            connection = psycopg2.connect(
                dsn=config('PGSQL_URL')
            )
            return connection
        except DatabaseError as ex:
            print(f"Error de base de datos: {ex}")
            retry_count += 1
            time.sleep(retry_delay)

    raise Exception("No se pudo establecer la conexión después de varios intentos")

# Ejemplo de uso en tu aplicación Flask:
try:
    connection = get_connection()
    cursor = connection.cursor()

    # Realiza operaciones en la base de datos

    cursor.close()
    connection.close()
except psycopg2.Error as e:
    print(f"Error de base de datos: {e}")'''



import psycopg2
from psycopg2 import DatabaseError
from decouple import config

def get_connection(user='postgres', password='lind@115513'):
    conn = psycopg2.connect(
        host="database-1.cqxkfbcblu85.us-east-2.rds.amazonaws.com",
        database="postgres",
        user=user,
        password=password
    )
    return conn