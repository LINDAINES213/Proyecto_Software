import os
import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "ep-crimson-dust-83713520.us-east-2.aws.neon.fl0.io"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "proyectoIS"),
        user=os.getenv("DB_USER", "fl0user"),
        password=os.getenv("DB_PASSWORD", "CPxpRr6Eal3Y"),
        sslmode="require"
    )
    return conn

'''def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "dpg-ckrvlhg5vl2c73c1jt00-a.oregon-postgres.render.com"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "proyectosoftware2"),
        user=os.getenv("DB_USER", "grupo6"),
        password=os.getenv("DB_PASSWORD", "jCAkeexPSlPnD8njLYB9iVZS22ZHlKkd"),
        sslmode="require"
    )
    return conn'''