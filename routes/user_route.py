from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from peewee import IntegrityError

from schemas.user_schema import UserSchema
from services.user_service import create_user, authenticate_user
from datetime import timedelta

from utils.responses import response
from utils.validators import validate_fields

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/auth/register", methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        validate_fields(data, {"nome", "email", "senha"})

        data["senha_hash"] = generate_password_hash(data.pop("senha"))
        validate_user = UserSchema().load(data)

        create_user(validate_user)
        return response(message="Usuário criado com sucesso", status=201)

    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)
    except IntegrityError:
        return response(message="Usuário já existe", status=409)
    except Exception as error:
        return response(message=f"Erro ao registrar usuário: {str(error)}", status=500)

@user_bp.route("/auth/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        validate_fields(data, {"email", "senha"})

        user, error = authenticate_user(data["email"], data["senha"])
        if error:
            return response(message=error, status=401)

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(minutes=15)
        )

        return jsonify({
            "token": access_token,
            "usuario": {
                "id": user.id,
                "nome": user.nome,
                "email": user.email
            }
        }), 200

    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)
    except Exception as error:
        return response(message=f"Erro ao fazer login: {str(error)}", status=500)