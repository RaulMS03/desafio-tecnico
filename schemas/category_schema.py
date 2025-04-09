from marshmallow import Schema, fields

class CategorySchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True)