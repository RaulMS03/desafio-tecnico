from marshmallow import Schema, fields

class EstoqueSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True)
    status = fields.Boolean(required=True)
    criado_em = fields.DateTime()
    atualizado_em = fields.DateTime()

estoques_schema = EstoqueSchema(many=True)
estoque_schema = EstoqueSchema()