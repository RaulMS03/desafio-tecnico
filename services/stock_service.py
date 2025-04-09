from models.estoque import Estoques

def get_stocks():
    return list(Estoques.select())

def get_stock_by_id(id: int) -> Estoques:
    return Estoques.get_by_id(id)

def create_valid_stock(data):
    return Estoques.create(**data)

def change_stock_status(data):
    stock_id = data.pop('id')
    return Estoques.update(**data).where(Estoques.id == stock_id).execute()