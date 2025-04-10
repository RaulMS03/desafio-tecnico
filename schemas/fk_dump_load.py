from marshmallow import fields

class ForeignKeyFieldDumpLoad(fields.Function):
    def __init__(self, attribute_name, cast_type=int, **kwargs):
        super().__init__(
            serialize=lambda obj: getattr(getattr(obj, attribute_name), "id", None),
            deserialize=lambda value: cast_type(value),
            required=True,
            **kwargs
        )