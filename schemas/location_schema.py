from marshmallow import Schema, fields, validate

from schemas.fk_dump_load import ForeignKeyFieldDumpLoad

class LocationSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True, validate=validate.Length(min=1))
    estoque_id = ForeignKeyFieldDumpLoad("estoque_id", cast_type=int)