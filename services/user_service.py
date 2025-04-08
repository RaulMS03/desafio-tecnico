import peewee
from werkzeug.security import check_password_hash
from models.usuario import Usuarios

def create_user(data):
    return Usuarios.create(**data)

def authenticate_user(email: str, password: str):
    try:
        user = Usuarios.get(Usuarios.email == email)
        if not check_password_hash(user.senha_hash, password):
            return None, "Senha Incorreta"
        return user, None
    except peewee.DoesNotExist:
        return None, "Usuário não encontrado"