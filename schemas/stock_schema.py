from marshmallow import Schema, fields, validate

class StockSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True, validate=validate.Length(min=1))
    status = fields.Boolean(required=True, validate=validate.Equal(False))
    criado_em = fields.DateTime()
    atualizado_em = fields.DateTime()