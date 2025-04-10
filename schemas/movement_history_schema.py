from marshmallow import Schema, fields, validate

from schemas.fk_dump_load import ForeignKeyFieldDumpLoad

class MovementSchema(Schema):
    id = fields.Integer()
    data_hora = fields.DateTime()
    tipo_movimentacao = fields.Str(
        required=True,
        validate=validate.OneOf(["entrada", "saida", "transferencia"])
    )
    equipamento_id = ForeignKeyFieldDumpLoad("equipamento_id", cast_type=int)
    localizacao_id = ForeignKeyFieldDumpLoad("localizacao_id", cast_type=int)