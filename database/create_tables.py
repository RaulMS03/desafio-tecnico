from peewee import OperationalError

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
import time

def create_all_tables():
    print("Conectando ao banco")
    connect_with_retry(db)

    print("Criando tabelas")
    db.create_tables([
        Estoques,
        TiposEquipamento,
        Categorias,
        Usuarios,
        Localizacoes,
        Equipamentos,
        HistoricoMovimentacao
    ])
    print("Tabelas criadas com sucesso")
    db.close()

if __name__ == "__main__":
    create_all_tables()
