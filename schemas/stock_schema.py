from marshmallow import Schema, fields

class StockSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True)
    status = fields.Boolean(required=True)
    criado_em = fields.DateTime()
    atualizado_em = fields.DateTime()