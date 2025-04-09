import peewee

from models import Localizacoes, Estoques

def get_locations():
    return list(Localizacoes.select())

def create_valid_location(data):
    try:
        stock = Estoques.get_by_id(data["estoque_id"])
    except peewee.DoesNotExist:
        raise ValueError("Estoque com o ID fornecido não existe.")

    return Localizacoes.create(nome=data["nome"], estoque_id=stock.id)