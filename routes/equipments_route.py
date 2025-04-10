import peewee
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from schemas.equipments_schema import EquipmentsSchema
from services.equipments_service import get_filtered_equipments, get_equipment_by_id, \
    change_equipment_status, update_equipment_by_id, create_valid_equipments
from utils.decorators import require_admin
from utils.responses import response
from utils.validators import validate_fields

equipments_bp = Blueprint("equipments_bp", __name__)

@equipments_bp.route("/equipamentos", methods=['GET'])
@jwt_required()
def get_equipments():
    try:
        filters = request.args.to_dict()
        equipments = get_filtered_equipments(filters)
        return jsonify({"Equipamentos": EquipmentsSchema(many=True).dump(equipments)}), 200
    except ValueError as e:
        return response(message=str(e), status=404)

@equipments_bp.route("/equipamentos", methods=['POST'])
@jwt_required()
@require_admin
def create_equipments():
    try:
        data = request.get_json()
        validate_fields(data, {"nome", "status", "estoque_id", "tipo_id", "categoria_id", "localizacao_id"})
        validate_data = EquipmentsSchema().load(data)
        create_valid_equipments(validate_data)
        return response(message="Equipamento criado com sucesso", status=201)
    except ValueError as error:
        return response(message=str(error), status=400)
    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)

@equipments_bp.route("/equipamentos/<int:id>/desativar", methods=['PATCH'])
@jwt_required()
@require_admin
def disable_equipment_by_id(id):
    try:
        data = request.get_json()
        status = data.get("status")

        if status is None:
            return response(message="Campo 'status' é obrigatório", status=400)
        if status:
            return response(message="Reativação de Equipamento não é permitida nesta rota", status=400)

        equipment = get_equipment_by_id(id)

        if not equipment.status:
            return response(message="O equipamento já está desativado", status=400)

        validate_data = EquipmentsSchema().load(data={"id": id, "status": status}, partial=True)
        change_equipment_status(validate_data)

        return response(message="Equipamento desativado com sucesso", status=200)

    except peewee.DoesNotExist:
        return response(message=f"O equipamento com o ID informado não existe", status=404)
    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)
    except Exception as e:
        return response(message=f"Erro ao desativar equipamento: {str(e)}", status=500)

@equipments_bp.route("/equipamentos/<int:id>", methods=["PUT"])
@jwt_required()
@require_admin
def update_equipment(id):
    try:
        data = request.get_json()

        required_fields = {"nome", "status", "estoque_id", "tipo_id", "categoria_id", "localizacao_id"}
        validate_fields(data, required_fields)

        if any(data[field] == "" for field in required_fields):
            return response(message="Campos obrigatórios não podem ser vazios", status=400)

        data["id"] = id
        validated_data = EquipmentsSchema().load(data)
        update_equipment_by_id(validated_data)

        return response(message="Equipamento atualizado com sucesso", status=200)

    except ValidationError as error:
        return response(message=f"Erro de validação: {error.messages}", status=400)
    except ValueError as error:
        return response(message=str(error), status=404)
    except Exception as e:
        return response(message=f"Erro ao atualizar equipamento: {str(e)}", status=500)