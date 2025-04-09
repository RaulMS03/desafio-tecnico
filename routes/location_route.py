from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.location_schema import LocationSchema
from services.location_service import get_locations, create_valid_location
from utils.decorators import require_admin
from utils.responses import response
from utils.validators import validate_fields

location_bp = Blueprint("location_bp", __name__)

@location_bp.route("/localizacoes", methods=['GET'])
@jwt_required()
def get_all_locations():
    locations = get_locations()
    return jsonify({"Localizações": LocationSchema(many=True).dump(locations)}), 200


@location_bp.route("/localizacoes", methods=['POST'])
@jwt_required()
@require_admin
def create_location():
    try:
        data = request.get_json()
        validate_fields(data, {"estoque_id", "nome"})
        validate_data = LocationSchema().load(data)
        create_valid_location(validate_data)
        return response(message="Localização criada com sucesso", status=201)
    except ValueError as error:
        return response(message=str(error), status=400)
    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)