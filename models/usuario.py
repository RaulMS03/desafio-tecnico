from peewee import AutoField, TextField
from .base import BaseModel

class Usuarios(BaseModel):
    id = AutoField()
    nome = TextField()
    email = TextField(unique=True)
    senha_hash = TextField()

    class Meta:
        db_table = "usuarios"