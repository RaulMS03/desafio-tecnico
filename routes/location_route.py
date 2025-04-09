from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.location_schema import LocationSchema
from services.location_service import get_locations, create_location
from utils.responses import response
from utils.validators import validate_fields

location_bp = Blueprint("location_bp", __name__)

@location_bp.route("/localizacoes", methods=['GET', 'POST'])
@jwt_required()
def locations_endpoint():
    if request.method == "GET":
        locations = get_locations()
        return jsonify({"Localizações": LocationSchema(many=True).dump(locations)}), 200

    if request.method == "POST":
        try:
            data = request.get_json()
            validate_fields(data, {"estoque_id", "nome"})
            validate_data = LocationSchema().load(data)
            create_location(validate_data)
            return response(message="Localização criada com sucesso", status=201)
        except ValueError as error:
            return response(message=str(error), status=400)
        except ValidationError as error:
            return response(message=f"Erro de validação: {error.messages}", status=400)