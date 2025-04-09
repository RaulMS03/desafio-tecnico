from models import Categorias

def get_category():
    return list(Categorias.select())

def create_category(data):
    return Categorias.create(**data)