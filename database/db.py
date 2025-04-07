import time

from peewee import PostgresqlDatabase, OperationalError
import os

def get_postgres_database():
    '''
    Cria o Banco de Dados(PostgreSQL)
    :return: PostgresqlDatabase
    '''
    tentativas = 10
    segundos = 2

    db = PostgresqlDatabase(
        os.getenv("PG_DB"),
        user=os.getenv("PG_DB_USER"),
        password=os.getenv("PG_DB_PASSWORD"),
        host=os.getenv("PG_DB_HOST"),
        port=int(os.getenv("PG_DB_PORT"))
    )

    for i in range(tentativas):
        try:
            db.connect()
            print("Conectado ao banco de dados")
            db.close()
            break
        except OperationalError as e:
            print(f"Tentativa {i + 1}/{tentativas}: Banco ainda não esta pronto")
            time.sleep(segundos)
    else:
        raise Exception("Não foi possivel se conectar ao banco de dados")

    return db