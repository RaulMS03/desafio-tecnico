from peewee import AutoField, TextField
from .base import BaseModel

class Categorias(BaseModel):
    id = AutoField()
    nome = TextField()

    class Meta:
        db_table = "categorias"