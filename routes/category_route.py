from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.category_schema import CategorySchema
from services.category_service import get_category, create_category
from utils.responses import response
from utils.validators import validate_fields

category_bp = Blueprint("category_bp", __name__)

@category_bp.route("/categorias", methods= ['GET', 'POST'])
@jwt_required()
def category_endpoint():
    if request.method == "GET":
        category = get_category()
        return jsonify({"Categorias": CategorySchema(many=True).dump(category)}), 200

    if request.method == "POST":
        try:
            data = request.get_json()
            validate_fields(data, {"nome"})
            validate_data = CategorySchema().load(data)
            create_category(validate_data)
            return response(message="Categoria criada com sucesso", status=201)
        except ValueError as error:
            return response(message=str(error), status=400)
        except ValidationError as error:
            return response(message=f"Erro de validação: {error.messages}", status=400)