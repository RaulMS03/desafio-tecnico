from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def create_database_if_not_exists():
    db_nome = os.getenv("PG_DB")

    conn = psycopg2.connect(
        host=os.getenv("PG_DB_HOST"),
        user=os.getenv("PG_DB_USER"),
        password=os.getenv("PG_DB_PASSWORD")
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_nome,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f'CREATE DATABASE "{db_nome}"')
        print(f"Banco '{db_nome}' criado.")
    else:
        print(f"Banco '{db_nome}' já existe.")

    cursor.close()
    conn.close()
