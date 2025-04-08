def validate_fields(data, allowed_fields):
    received_fields = set(data.keys())
    invalid_fields = received_fields - allowed_fields
    if invalid_fields:
        raise ValueError(
            f"Campos inválidos: {', '.join(invalid_fields)}. Só é necessário: {', '.join(allowed_fields)}"
        )