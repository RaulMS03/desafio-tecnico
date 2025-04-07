from peewee import AutoField, TextField, DateTimeField, ForeignKeyField
from .base import BaseModel
from .estoque import Estoques
from .tipos_equipamento import TiposEquipamento
from .categoria import Categorias
import datetime

class Equipamentos(BaseModel):
    id = AutoField()
    nome = TextField()
    status = TextField()
    criado_em = DateTimeField(default=datetime.datetime.now)
    atualizado_em = DateTimeField(default=datetime.datetime.now)
    estoque = ForeignKeyField(Estoques, backref="equipamentos")
    tipo = ForeignKeyField(TiposEquipamento, backref="equipamentos")
    categoria = ForeignKeyField(Categorias, backref="equipamentos")

    class Meta:
        db_table = "equipamentos"
