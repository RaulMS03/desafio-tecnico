from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from schemas.movement_history_schema import MovementSchema
from services.movement_history_service import register_movement, get_movements_history
from utils.decorators import require_admin
from utils.responses import response

movement_bp = Blueprint("movement_bp", __name__)

@movement_bp.route("/movimentacoes", methods=['GET'])
@jwt_required()
def get_all_movement_history():
    movement = get_movements_history()

    return jsonify({"historico_de_movimentacoes": MovementSchema(many=True).dump(movement)}), 200

@movement_bp.route("/movimentacoes", methods=['POST'])
@jwt_required()
@require_admin
def movement_equipment():
    try:
        data = request.get_json()

        validated_data = MovementSchema().load(data)
        user_id = get_jwt_identity()

        history = register_movement(
            equipamento_id=validated_data["equipamento_id"],
            tipo_movimentacao=validated_data["tipo_movimentacao"],
            localizacao_id=validated_data["localizacao_id"],
            usuario_id=user_id
        )

        return response(data=history, message="Movimentação registrada com sucesso", status=201)
    except ValueError as error:
        return response(message=str(error), status=400)
    except Exception as error:
        return response(message=f"Erro ao movimentar equipamento: {str(error)}", status=500)