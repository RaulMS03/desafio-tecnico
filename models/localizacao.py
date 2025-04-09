from peewee import AutoField, TextField, ForeignKeyField
from .base import BaseModel
from .estoque import Estoques

class Localizacoes(BaseModel):
    id = AutoField()
    nome = TextField()
    estoque_id = ForeignKeyField(Estoques, backref="localizacoes")

    class Meta:
        db_table = "localizacoes"