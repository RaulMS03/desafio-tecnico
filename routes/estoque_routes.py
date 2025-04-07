from flask import Blueprint, request, jsonify
from services.estoque_service import get_estoques, get_estoque_by_id, criar_estoque
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

@estoque_bp.route("/estoques/<id>", methods=['GET', 'PATCH'])
def estoque_id(id):
    if request.method == "GET":
        try:
            estoque = get_estoque_by_id(id)
            return jsonify({'estoque': estoque_schema.dump(estoque)}), 200
        except peewee.DoesNotExist:
            return {"message": f"O estoque com o id informado não existe"}

    if request.method == "PATCH":
        return