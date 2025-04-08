from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True)
    email = fields.String(required=True)
    senha_hash = fields.String(required=True)
