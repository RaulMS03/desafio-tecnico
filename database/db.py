from peewee import PostgresqlDatabase, SqliteDatabase, Proxy, OperationalError
import os
import time

db = Proxy()

def get_postgres_database():
    return PostgresqlDatabase(
        os.getenv("PG_DB"),
        user=os.getenv("PG_DB_USER"),
        password=os.getenv("PG_DB_PASSWORD"),
        host=os.getenv("PG_DB_HOST"),
        port=int(os.getenv("PG_DB_PORT")),
    )

def init_db(testing=False):
    """Inicializa o banco de dados, dependendo do ambiente (testes ou produção)."""
    if testing:
        test_db = SqliteDatabase(':memory:')
        db.initialize(test_db)
    else:
        db.initialize(get_postgres_database())

def connect_with_retry(db_instance, attempts=10, seconds=2):
    for i in range(attempts):
        try:
            db_instance.connect()
            print(f"Conexão bem-sucedida no banco de dados (tentativa {i+1})")
            return
        except OperationalError:
            print(f"Tentativa {i + 1}/{attempts}: Banco ainda não está pronto")
            time.sleep(seconds)
    raise Exception("Não foi possível conectar ao banco de dados")
