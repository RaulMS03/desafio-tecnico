from peewee import AutoField, TextField
from .base import BaseModel

class TiposEquipamento(BaseModel):
    id = AutoField()
    nome = TextField()

    class Meta:
        db_table = "tipos_equipamentos"