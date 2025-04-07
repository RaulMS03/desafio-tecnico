from models.tables import Estoques

def get_estoques():
    return list(Estoques.select())

def get_estoque_by_id(id):
    return Estoques.get_by_id(id)

def criar_estoque(data):
    return Estoques.create(**data)