from models import TiposEquipamento

def get_equipment_type():
    return list(TiposEquipamento.select())

def create_equipment_type(data):
    return TiposEquipamento.create(**data)