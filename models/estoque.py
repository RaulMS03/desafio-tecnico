from peewee import AutoField, TextField, BooleanField, DateTimeField
from .base import BaseModel
import datetime

class Estoques(BaseModel):
    id = AutoField()
    nome = TextField()
    status = BooleanField(default=True)
    criado_em = DateTimeField(default=datetime.datetime.now())
    atualizado_em = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "estoques"