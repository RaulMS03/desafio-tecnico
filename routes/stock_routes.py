from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from services.estoque_service import (
    get_estoques,
    get_estoque_by_id,
    criar_estoque,
    alterar_status_estoque
)
from schemas.estoque_schema import EstoqueSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.responses import response
from utils.validators import validate_fields
import peewee

stock_bp = Blueprint('stock_bp', __name__)

@stock_bp.route("/estoques", methods=['GET', 'POST'])
@jwt_required()
def stocks_endpoint():
    user_id = get_jwt_identity()

    if not user_id:
        return response(message="Acesso negado: token inválido", status=401)

    if request.method == "GET":
        stocks = get_estoques()
        return jsonify({"Estoques": EstoqueSchema(many=True).dump(stocks)}),200

    if request.method == "POST":
        try:
            data = request.get_json()
            validate_fields(data, {"nome"})
            validate_data = EstoqueSchema().load(data, partial=True)
            criar_estoque(validate_data)
            return response(message="Estoque criado com sucesso", status=201)
        except ValueError as error:
            return response(message=str(error), status=400)
        except ValidationError as error:
            return response(message=f"Erro de validação: {error.messages}", status=400)

@stock_bp.route("/estoques/<int:id>", methods=['GET'])
@jwt_required()
def estoque_id(id):
    try:
        estoque = get_estoque_by_id(id)
        return jsonify({'estoque': EstoqueSchema().dump(estoque)}), 200

    except peewee.DoesNotExist:
        return {"message": f"O estoque com o ID informado não existe"}, 404

@stock_bp.route("/estoques/<int:id>/desativar", methods=['PATCH'])
@jwt_required()
def desativar_estoque_by_id(id):
    try:
        data = request.get_json()
        status = data.get("status")

        if status is None:
            return response(message="Campo 'status' é obrigatório", status=400)
        if status:
            return response(message="Reativação de estoque não é permitida nesta rota", status=400)

        estoque = get_estoque_by_id(id)

        if not estoque.status:
            return response(message="O estoque já está desativado", status=400)

        validate_data = EstoqueSchema().load(data={"id": id, "status": status}, partial=True)
        alterar_status_estoque(validate_data)

        return response(message="Estoque desativado com sucesso", status=200)

    except peewee.DoesNotExist:
        return response(message=f"O estoque com o ID informado não existe", status=404)
    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)
    except Exception as e:
        return response(message=f"Erro ao desativar estoque: {str(e)}", status=500)