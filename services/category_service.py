from models import Categorias

def get_category():
    return list(Categorias.select())

def create_category(data):
    try:
        return Categorias.create(**data)
    except Exception as e:
        raise ValueError(f"Erro ao criar categoria: {str(e)}")