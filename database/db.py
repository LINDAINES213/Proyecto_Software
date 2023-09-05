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

def get_connection():
    try:
        return psycopg2.connect(
            host=config('PGSQL_HOST'),
            user=config('PGSQL_USER'),
            password=config('PGSQL_PASSWORD'),
            database=config('PGSQL_DATABASE')
        )
    except DatabaseError as ex:
        raise ex
