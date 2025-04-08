import peewee
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import IntegrityError

from models import Usuarios
from schemas.user_schema import UserSchema
from services.user_service import create_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/auth/register", methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('nome')
    email = data.get('email')
    password = data.get('senha_hash')

    if not name or not email or not password:
        return jsonify({'message': "É necessario: 'nome', 'email' e 'senha_hash'"}), 400

    hashed_password = generate_password_hash(password)
    user_data = {
        "nome": name,
        "email": email,
        "senha_hash": hashed_password
    }

    try:
        validate_user = UserSchema().load(user_data)
        create_user(validate_user)

        return jsonify({"message": "Usuario criado"}), 201
    except IntegrityError:
        return jsonify({"message": "Usuario já existe"}), 409

@user_bp.route("/auth/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('senha_hash')

    if not email or not password:
        return jsonify({"message": "Necessario 'email' e 'senha_hash'"}), 400

    try:
        user = Usuarios.get(Usuarios.email == email)
    except peewee.DoesNotExist:
        return jsonify({"message": "Usuario não encontrado"}), 400

    if not check_password_hash(user.senha_hash, password):
        return jsonify({"message": "Senha incorreta"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "token": access_token,
        "usuario": {
            "id": user.id,
            "nome": user.nome,
            "email": user.email
        }
    }), 200