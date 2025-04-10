import logging
from database.db import connect_with_retry, get_postgres_database
from models import (
    Estoques,
    TiposEquipamento,
    Categorias,
    Usuarios,
    Localizacoes,
    Equipamentos,
    HistoricoMovimentacao,
)
from models.base import db

logging.basicConfig(level=logging.INFO)


def create_all_tables(testing=False):
    try:
        logging.info("Conectando ao banco.")

        if testing:
            from peewee import SqliteDatabase
            db.initialize(SqliteDatabase(':memory:'))
        else:
            db.initialize(get_postgres_database())
            connect_with_retry(db)

        if db.is_closed():
            db.connect()
            logging.info("Banco de dados conectado com sucesso.")

        logging.info("Criando tabelas.")
        db.create_tables(
            [Estoques, TiposEquipamento, Categorias, Usuarios, Localizacoes, Equipamentos, HistoricoMovimentacao])

        logging.info("Tabelas criadas com sucesso.")
    except Exception as error:
        logging.error(f"Erro ao criar tabelas: {error}")
    finally:
        if not db.is_closed():
            db.close()

if __name__ == "__main__":
    create_all_tables()
