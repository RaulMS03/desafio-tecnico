from peewee import AutoField, ForeignKeyField, TextField, DateTimeField, CharField, Check
from .base import BaseModel
from .equipamento import Equipamentos
from .usuario import Usuarios
from .localizacao import Localizacoes
import datetime

class HistoricoMovimentacao(BaseModel):
    id = AutoField()
    equipamento_id = ForeignKeyField(Equipamentos, backref="historicos")
    usuario_id = ForeignKeyField(Usuarios, backref="historicos")
    tipo_movimentacao = CharField(constraints=[Check("tipo_movimentacao IN ('entrada', 'saida', 'transferencia')")])
    data_hora = DateTimeField(default=datetime.datetime.now)
    localizacao_id = ForeignKeyField(Localizacoes, backref="historicos")

    class Meta:
        table_name = "historico_movimentacao"