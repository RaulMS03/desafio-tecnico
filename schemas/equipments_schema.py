from marshmallow import Schema, fields, validate

from schemas.fk_dump_load import ForeignKeyFieldDumpLoad

class EquipmentsSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True, validate=validate.Length(min=1))
    status = fields.Boolean(required=True, validate=validate.Equal(False))
    criado_em = fields.DateTime()
    atualizado_em = fields.DateTime()
    estoque_id = ForeignKeyFieldDumpLoad("estoque_id", cast_type=int)
    tipo_id = ForeignKeyFieldDumpLoad("tipo_id", cast_type=int)
    categoria_id = ForeignKeyFieldDumpLoad("categoria_id", cast_type=int)