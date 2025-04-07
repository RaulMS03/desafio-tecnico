from flask import Blueprint, request, jsonify
from services.estoque_service import get_estoques, get_estoque_by_id, criar_estoque, alterar_status_estoque
from schemas.estoque_schema import estoques_schema, estoque_schema
import peewee

estoque_bp = Blueprint('estoque_bp', __name__)

@estoque_bp.route("/estoques", methods=['GET', 'POST'])
def estoques_endpoint():
    if request.method == "GET":
        estoques = get_estoques()
        return jsonify({'estoques': estoques_schema.dump(estoques)}), 200

    if request.method == "POST":
        data = request.get_json()
        validate_data = estoque_schema.load(data)
        criar_estoque(validate_data)

        return jsonify({"message": "Criado com sucesso"}), 201

@estoque_bp.route("/estoques/<int:id>", methods=['GET'])
def estoque_id(id):
    try:
        estoque = get_estoque_by_id(id)
        return jsonify({'estoque': estoque_schema.dump(estoque)}), 200

    except peewee.DoesNotExist:
        return {"message": f"O estoque com o id informado não existe"}, 404

@estoque_bp.route("/estoques/<int:id>/desativar", methods=['PATCH'])
def desativar_estoque_by_id(id):
    try:
        estoque = get_estoque_by_id(id)
        data = request.get_json()
        status = data.get("status")

        if status is None:
            return {"message": "Campo 'status' é obrigatorio"}, 400

        if status:
            return {"message": "Não é permitido reativar um estoque por esta rota"}, 400

        if not estoque.status:
            return {"message": "O estoque ja está desativado"}, 400

        estoque_data = {"id": id, "status": status}
        validate_data = estoque_schema.load(estoque_data, partial=True)

        alterar_status_estoque(validate_data)

        return jsonify({"estoque": "Estoque alterado com sucesso"}), 200

    except peewee.DoesNotExist:
        return {"message": f"O estoque com o id informado não existe"}, 404

    except Exception as e:
        return {"message": f"Erro ao desativar estoque: {str(e)}"}, 500