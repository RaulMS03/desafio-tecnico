from peewee import PostgresqlDatabase
import os

def get_postgres_database():
    '''
    Cria o Banco de Dados(PostgreSQL)
    :return: PostgresqlDatabase
    '''

    return PostgresqlDatabase(
        os.getenv("PG_DB"),
        user=os.getenv("PG_DB_USER"),
        password=os.getenv("PG_DB_PASSWORD"),
        host=os.getenv("PG_DB_HOST"),
        port=int(os.getenv("PG_DB_PORT"))
    )
