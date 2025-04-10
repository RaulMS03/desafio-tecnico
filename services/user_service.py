import peewee
import jwt
from flask import request
from werkzeug.security import check_password_hash
from models.usuarios import Usuarios
import os

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

def get_user_by_token(req: request):
    auth_header = req.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]

    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        usuario_id = payload.get('sub')
        if not usuario_id:
            return None
        return Usuarios.get_or_none(Usuarios.id == usuario_id)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None