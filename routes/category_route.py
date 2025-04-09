from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.category_schema import CategorySchema
from services.category_service import get_category, create_valid_category
from utils.decorators import require_admin
from utils.responses import response
from utils.validators import validate_fields

category_bp = Blueprint("category_bp", __name__)

@category_bp.route("/categorias", methods= ['GET'])
@jwt_required()
def get_all_categories():
    category = get_category()
    return jsonify({"Categorias": CategorySchema(many=True).dump(category)}), 200

@category_bp.route("/categorias", methods=['POST'])
@jwt_required()
@require_admin
def create_category():
    try:
        data = request.get_json()
        validate_fields(data, {"nome"})
        validate_data = CategorySchema().load(data)
        create_valid_category(validate_data)
        return response(message="Categoria criada com sucesso", status=201)
    except ValueError as error:
        return response(message=str(error), status=400)
    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)