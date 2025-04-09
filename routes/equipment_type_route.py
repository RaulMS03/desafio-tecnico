from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.equipment_type_schema import EquipmentTypeSchema
from services.equipment_type_service import get_equipment_type, create_equipment_type
from utils.responses import response
from utils.validators import validate_fields

equipment_type_bp = Blueprint('equipment_type_bp', __name__)

@equipment_type_bp.route("/tipos-equipamento", methods=['GET', 'POST'])
@jwt_required()
def equipment_type_endpoint():
    if request.method == "GET":
        equipment_type = get_equipment_type()
        return jsonify({"tipos_de_equipamentos": EquipmentTypeSchema(many=True).dump(equipment_type)}), 200

    if request.method == "POST":
        try:
            data = request.get_json()
            validate_fields(data, {"nome"})
            validate_data = EquipmentTypeSchema().load(data)
            create_equipment_type(validate_data)
            return response(message="Tipo de Equipamento criado com sucesso", status=201)
        except ValueError as error:
            return response(message=str(error), status=400)
        except ValidationError as error:
            return response(message=f"Erro de validação: {error.messages}", status=400)