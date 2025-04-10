from models import Equipamentos, HistoricoMovimentacao
from models.base import db
import peewee

from utils.dict import historic_to_dict

def get_movements_history():
    return list(HistoricoMovimentacao.select())

def register_movement(equipamento_id, usuario_id, tipo_movimentacao, localizacao_id):
    try:
        with db.atomic():
            equipment = Equipamentos.get_by_id(equipamento_id)
            equipment.localizacao_id = localizacao_id
            equipment.save()

            history = HistoricoMovimentacao.create(
                equipamento_id=equipamento_id,
                usuario_id=usuario_id,
                tipo_movimentacao=tipo_movimentacao,
                localizacao_id=localizacao_id
            )

            return historic_to_dict(history)

    except peewee.DoesNotExist:
        raise ValueError("Alguma instancia não foi encontrada")
    except peewee.IntegrityError:
        raise ValueError("Localização inválida")
    except Exception as e:
        raise RuntimeError(f"Erro ao registrar movimentação: {str(e)}")
