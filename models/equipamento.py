from peewee import AutoField, TextField, DateTimeField, ForeignKeyField, BooleanField
from .base import BaseModel
from .estoque import Estoques
from .tipos_equipamento import TiposEquipamento
from .categoria import Categorias
import datetime

class Equipamentos(BaseModel):
    id = AutoField()
    nome = TextField()
    status = BooleanField(default=True)
    criado_em = DateTimeField(default=datetime.datetime.now)
    atualizado_em = DateTimeField(default=datetime.datetime.now)
    estoque_id = ForeignKeyField(Estoques, backref="equipamentos")
    tipo_id = ForeignKeyField(TiposEquipamento, backref="equipamentos")
    categoria_id = ForeignKeyField(Categorias, backref="equipamentos")

    class Meta:
        db_table = "equipamentos"