import peewee

from datetime import datetime, timezone
from models import Equipamentos, Estoques, TiposEquipamento, Categorias

def get_filtered_equipments(filters: dict):
    query = Equipamentos.select().where(Equipamentos.status)

    if 'estoque_id' in filters:
        query = query.where(Equipamentos.estoque_id == filters['estoque_id'])
    if 'tipo_id' in filters:
        query = query.where(Equipamentos.tipo_id == filters['tipo_id'])
    if 'categoria_id' in filters:
        query = query.where(Equipamentos.categoria_id == filters['categoria_id'])

    equipamentos = list(query)
    if not equipamentos:
        raise ValueError("Nenhum equipamento encontrado com os filtros fornecidos.")
    return equipamentos

def check_equipment_duplicate(nome, estoque_id, ignore_id=None):
    query = Equipamentos.select().where(
        (Equipamentos.nome == nome) &
        (Equipamentos.estoque_id == estoque_id)
    )
    if ignore_id:
        query = query.where(Equipamentos.id != ignore_id)
    return query.exists()

def create_valid_equipments(data):
    try:
        stock = Estoques.get_by_id(data["estoque_id"])
        equipment_type = TiposEquipamento.get_by_id(data["tipo_id"])
        category = Categorias.get_by_id(data["categoria_id"])
    except peewee.DoesNotExist:
        raise ValueError("Alguma referência de ID fornecida não existe.")

    if check_equipment_duplicate(data["nome"], stock.id):
        raise ValueError("Já existe um equipamento com esse nome nesse estoque.")

    return Equipamentos.create(
        nome=data["nome"],
        status=data["status"],
        estoque_id=stock.id,
        tipo_id=equipment_type.id,
        categoria_id=category.id
    )

def get_equipment_by_id(id: int) -> Equipamentos:
    return Equipamentos.get_by_id(id)

def change_equipment_status(data):
    equipment_id = data.pop('id')
    return Equipamentos.update(**data).where(Equipamentos.id == equipment_id).execute()

def update_equipment_by_id(data):
    try:
        equipment = Equipamentos.get_by_id(data["id"])

        new_name = data.get("nome", equipment.nome)
        new_stock_id = data.get("estoque_id", equipment.estoque_id)

        if check_equipment_duplicate(new_name, new_stock_id, ignore_id=equipment.id):
            raise ValueError("Já existe um equipamento com esse nome nesse estoque.")

        equipment.nome = data.get("nome", equipment.nome)
        equipment.status = data.get("status", equipment.status)
        equipment.estoque_id = data.get("estoque_id", equipment.estoque_id)
        equipment.tipo_id = data.get("tipo_id", equipment.tipo_id)
        equipment.categoria_id = data.get("categoria_id", equipment.categoria_id)
        equipment.atualizado_em = datetime.now(timezone.utc)

        equipment.save()
        return equipment

    except peewee.DoesNotExist:
        raise ValueError("Equipamento não encontrado.")