from peewee import *
from dotenv import load_dotenv
from database.db import get_postgres_database

import datetime

load_dotenv()

db = get_postgres_database()

class BaseModel(Model):
    class Meta:
        database = db

class Estoques(BaseModel):
    id = PrimaryKeyField(null=False)
    nome = TextField()
    status = TextField()
    criado_em = DateTimeField(default=datetime.datetime.now)
    atualizado_em = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "Estoques"

# class TiposEquipamento(BaseModel):
#     id = AutoField()
#     nome = TextField()
#
#     class Meta:
#         db_table = "TiposEquipamento"
#
# class Categorias(BaseModel):
#     id = AutoField()
#     nome = TextField()
#
#     class Meta:
#         db_table = "Categorias"
#
# class Usuarios(BaseModel):
#     id = AutoField()
#     nome = TextField()
#     email = TextField(unique=True)
#     senha_hash = TextField()
#
#     class Meta:
#         db_table = "Usuarios"
#
# class Localizacoes(BaseModel):
#     id = AutoField()
#     nome = TextField()
#     estoque_id = ForeignKeyField(Estoques, backref="id")
#
#     class Meta:
#         db_table = "Localizacoes"
#
# class Equipamentos(BaseModel):
#     id = AutoField()
#     nome = TextField()
#     status = TextField()
#     criado_em = DateTimeField()
#     atualizado_em = DateTimeField()
#     estoque_id = ForeignKeyField(Estoques, backref="id")
#     tipo_id = ForeignKeyField(TiposEquipamento, backref="id")
#     categoria_id = ForeignKeyField(Categorias, backref="id")
#
#     class Meta:
#         db_table = "Equipamentos"
#
# class HistoricoMovimentacao(BaseModel):
#     id = AutoField()
#     equipamento_id = ForeignKeyField(Equipamentos, backref="id")
#     usuario_id = ForeignKeyField(Usuarios, backref="id")
#     tipo_movimentacao = TextField()
#     data_hora = DateTimeField()
#     localizacao_id = ForeignKeyField(Localizacoes, backref="id")
#
#     class Meta:
#         db_table = "HistoricoMovimentacao"

db.connect()
db.create_tables([
    Estoques,
    # Equipamentos,
    # Localizacoes,
    # TiposEquipamento,
    # Categorias,
    # HistoricoMovimentacao,
    # Usuarios
])
db.close()