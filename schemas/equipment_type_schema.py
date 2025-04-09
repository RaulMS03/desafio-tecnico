from marshmallow import Schema, fields, validate

class EquipmentTypeSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True, validate=validate.Length(min=1))