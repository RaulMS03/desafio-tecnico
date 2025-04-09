from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True, validate=validate.Length(min=1))