from models import TiposEquipamento

def get_equipment_type():
    return list(TiposEquipamento.select())

def create_equipment_type(data):
    try:
        return TiposEquipamento.create(**data)
    except Exception as e:
        raise ValueError(f"Erro ao criar tipo de equipamento: {str(e)}")