from models.usuario import Usuarios

def create_user(data):
    return Usuarios.create(**data)
