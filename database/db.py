import os
import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "ep-bitter-mud-14160489.us-east-2.aws.neon.fl0.io"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "proyectosoftware2"),
        user=os.getenv("DB_USER", "fl0user"),
        password=os.getenv("DB_PASSWORD", "jKxprFuf05OS"),
        sslmode="require"
    )
    return conn