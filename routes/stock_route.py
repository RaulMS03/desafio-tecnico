from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from services.stock_service import (
    get_stocks,
    get_stock_by_id,
    change_stock_status,
    create_valid_stock,
)
from schemas.stock_schema import StockSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.decorators import require_admin
from utils.responses import response
from utils.validators import validate_fields
import peewee

stock_bp = Blueprint('stock_bp', __name__)

@stock_bp.route("/estoques", methods=['GET'])
@jwt_required()
def get_all_stocks():
    user_id = get_jwt_identity()

    if not user_id:
        return response(message="Acesso negado: token inválido", status=401)

    stocks = get_stocks()
    return jsonify({"Estoques": StockSchema(many=True).dump(stocks)}),200

@stock_bp.route("/estoques/<int:id>", methods=['GET'])
@jwt_required()
def stock_by_id(id):
    try:
        stock = get_stock_by_id(id)
        return jsonify({'estoque': StockSchema().dump(stock)}), 200

    except peewee.DoesNotExist:
        return {"message": f"O estoque com o ID informado não existe"}, 404

@stock_bp.route("/estoques", methods=['POST'])
@jwt_required()
@require_admin
def create_stock():
    try:
        data = request.get_json()
        validate_fields(data, {"nome"})
        validate_data = StockSchema().load(data)
        create_valid_stock(validate_data)
        return response(message="Estoque criado com sucesso", status=201)
    except ValueError as error:
        return response(message=str(error), status=400)
    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)

@stock_bp.route("/estoques/<int:id>/desativar", methods=['PATCH'])
@jwt_required()
@require_admin
def disable_stock_by_id(id):
    try:
        data = request.get_json()
        status = data.get("status")

        if status is None:
            return response(message="Campo 'status' é obrigatório", status=400)
        if status:
            return response(message="Reativação de estoque não é permitida nesta rota", status=400)

        stock = get_stock_by_id(id)

        if not stock.status:
            return response(message="O estoque já está desativado", status=400)

        validate_data = StockSchema().load(data={"id": id, "status": status}, partial=True)
        change_stock_status(validate_data)

        return response(message="Estoque desativado com sucesso", status=200)

    except peewee.DoesNotExist:
        return response(message=f"O estoque com o ID informado não existe", status=404)
    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)
    except Exception as e:
        return response(message=f"Erro ao desativar estoque: {str(e)}", status=500)