from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer()
    nome = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True, validate=validate.Length(min=5))
    senha_hash = fields.String(required=True, validate=validate.Length(min=1))
