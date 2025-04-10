def historic_to_dict(historico):
    return {
        "id": historico.id,
        "equipamento_id": historico.equipamento_id.id,
        "usuario_id": historico.usuario_id.id,
        "tipo_movimentacao": historico.tipo_movimentacao,
        "data_hora": historico.data_hora.isoformat(),
        "localizacao_id": historico.localizacao_id.id
    }
