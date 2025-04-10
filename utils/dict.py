def historic_to_dict(history):
    return {
        "id": history.id,
        "equipamento_id": history.equipamento_id.id,
        "usuario_id": history.usuario_id.id,
        "tipo_movimentacao": history.tipo_movimentacao,
        "data_hora": history.data_hora.isoformat(),
        "localizacao_id": history.localizacao_id.id
    }
