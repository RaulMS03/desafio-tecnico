from marshmallow import Schema, fields

class EquipmentTypeSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True)