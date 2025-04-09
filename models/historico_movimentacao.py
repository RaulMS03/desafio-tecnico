from peewee import AutoField, ForeignKeyField, TextField, DateTimeField
from .base import BaseModel
from .equipamento import Equipamentos
from .usuario import Usuarios
from .localizacao import Localizacoes
import datetime

class HistoricoMovimentacao(BaseModel):
    id = AutoField()
    equipamento = ForeignKeyField(Equipamentos, backref="historicos")
    usuario = ForeignKeyField(Usuarios, backref="historicos")
    tipo_movimentacao = TextField()
    data_hora = DateTimeField(default=datetime.datetime.now)
    localizacao = ForeignKeyField(Localizacoes, backref="historicos")

    class Meta:
        table_name = "historico_movimentacao"