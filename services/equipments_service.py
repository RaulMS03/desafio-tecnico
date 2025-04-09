import peewee

from datetime import datetime, timezone
from models import Equipamentos, Estoques, TiposEquipamento, Categorias

def get_filtered_equipments(filters: dict):
    query = Equipamentos.select().where(Equipamentos.status)

    if 'estoque_id' in filters:
        query = query.where(Equipamentos.estoque_id == filters['estoque_id'])
    # if 'localizacao' in filters:
    #     query = query.where(Equipamentos. == filters['localizacao'])
    if 'tipo_id' in filters:
        query = query.where(Equipamentos.tipo_id == filters['tipo_id'])
    if 'categoria_id' in filters:
        query = query.where(Equipamentos.categoria_id == filters['categoria_id'])

    equipamentos = list(query)
    if not equipamentos:
        raise ValueError("Nenhum equipamento encontrado com os filtros fornecidos.")
    return equipamentos


def create_equipments(data):
    try:
        stock = Estoques.get_by_id(data["estoque_id"])
        equipment_type = TiposEquipamento.get_by_id(data["tipo_id"])
        category = Categorias.get_by_id(data["categoria_id"])
    except peewee.DoesNotExist:
        raise ValueError("Alguma referência de ID fornecida não existe.")

    if Equipamentos.select().where(
        (Equipamentos.nome == data["nome"]) &
        (Equipamentos.estoque_id == stock.id)
    ).exists():
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
        equipments = Equipamentos.get_by_id(data["id"])

        new_name = data.get("nome", equipments.nome)
        new_stock_id = data.get("estoque_id", equipments.estoque_id)

        if Equipamentos.select().where(
            (Equipamentos.nome == new_name) &
            (Equipamentos.estoque_id == new_stock_id) &
            (Equipamentos.id != equipments.id)
        ).exists():
            raise ValueError("Já existe um equipamento com esse nome nesse estoque.")

        equipments.nome = data.get("nome", equipments.nome)
        equipments.status = data.get("status", equipments.status)
        equipments.estoque_id = data.get("estoque_id", equipments.estoque_id)
        equipments.tipo_id = data.get("tipo_id", equipments.tipo_id)
        equipments.categoria_id = data.get("categoria_id", equipments.categoria_id)
        # equipments.localizacao = data.get("localizacao", equipments.localizacao)
        equipments.atualizado_em = datetime.now(timezone.utc)

        equipments.save()
        return equipments

    except peewee.DoesNotExist:
        raise ValueError("Equipamento não encontrado.")