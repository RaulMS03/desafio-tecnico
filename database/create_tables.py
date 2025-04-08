import logging
from database.db import connect_with_retry
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

def create_all_tables():
    try:
        logging.info("Conectando ao banco.")
        connect_with_retry(db)

        logging.info("Criando tabelas.")
        db.create_tables([
            Estoques,
            TiposEquipamento,
            Categorias,
            Usuarios,
            Localizacoes,
            Equipamentos,
            HistoricoMovimentacao
        ])
        logging.info("Tabelas criadas com sucesso.")
    except Exception as error:
        logging.error(f"Erro ao criar tabelas: {error}")
    finally:
        db.close()

if __name__ == "__main__":
    create_all_tables()
