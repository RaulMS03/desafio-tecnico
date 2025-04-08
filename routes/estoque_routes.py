from flask import Blueprint, request, jsonify
from services.estoque_service import get_estoques, get_estoque_by_id, criar_estoque, alterar_status_estoque
from schemas.estoque_schema import estoques_schema, estoque_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
import peewee

estoque_bp = Blueprint('estoque_bp', __name__)

@estoque_bp.route("/estoques", methods=['GET', 'POST'])
@jwt_required()
def estoques_endpoint():
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({"message": "Acesso negado: token inválido"}), 401

    if request.method == "GET":
        estoques = get_estoques()
        return jsonify({'estoques': estoques_schema.dump(estoques)}), 200

    if request.method == "POST":
        data = request.get_json()
        nome = data.get("nome")

        campo_permitido = {"nome"}
        campos_recebidos = set(data.keys())
        campos_invalidos = campos_recebidos - campo_permitido

        if campos_invalidos:
            return jsonify({
                "message": f"Campos inválidos: {', '.join(campos_invalidos)}. Só é necessario: 'nome'"
            }), 400

        estoque_data = {"nome": nome}

        validate_data = estoque_schema.load(estoque_data, partial=True)
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