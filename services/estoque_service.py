from models.tables import Estoques

def get_estoques():
    return list(Estoques.select())

def get_estoque_by_id(id):
    return Estoques.get_by_id(id)

def criar_estoque(data):
    return Estoques.create(**data)

def alterar_status_estoque(data):
    estoque_id = data.pop('id')
    return Estoques.update(**data).where(Estoques.id == estoque_id).execute()