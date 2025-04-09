from marshmallow import Schema, fields

from schemas.fk_dump_load import ForeignKeyFieldDumpLoad


class LocationSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True)
    estoque_id = ForeignKeyFieldDumpLoad("estoque_id", cast_type=int)