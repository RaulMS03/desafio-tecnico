from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.equipment_type_schema import EquipmentTypeSchema
from services.equipment_type_service import get_equipment_type, create_valid_equipment_type
from utils.decorators import require_admin
from utils.responses import response
from utils.validators import validate_fields

equipment_type_bp = Blueprint('equipment_type_bp', __name__)

@equipment_type_bp.route("/tipos-equipamento", methods=['GET'])
@jwt_required()
def get_all_equipment_types():
    equipment_type = get_equipment_type()
    return jsonify({"tipos_de_equipamentos": EquipmentTypeSchema(many=True).dump(equipment_type)}), 200

@equipment_type_bp.route("/tipos-equipamento", methods=['POST'])
@jwt_required()
@require_admin
def create_equipment_type():
    try:
        data = request.get_json()
        validate_fields(data, {"nome"})
        validate_data = EquipmentTypeSchema().load(data)
        create_valid_equipment_type(validate_data)
        return response(message="Tipo de Equipamento criado com sucesso", status=201)
    except ValueError as error:
        return response(message=str(error), status=400)
    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)