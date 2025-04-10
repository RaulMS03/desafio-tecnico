from peewee import AutoField, TextField, CharField
from .base import BaseModel

class Usuarios(BaseModel):
    id = AutoField()
    nome = TextField()
    email = CharField(unique=True)
    senha_hash = CharField()
    papel = CharField(default='operador')

    class Meta:
        table_name = "usuarios"