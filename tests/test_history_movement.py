import pytest
from models import Estoques, Localizacoes, TiposEquipamento, Categorias, Equipamentos, HistoricoMovimentacao

@pytest.fixture
def setup_movimentacao():
    estoque = Estoques.create(nome="Estoque Teste")
    localizacao1 = Localizacoes.create(nome="Sala A", estoque_id=estoque)
    localizacao2 = Localizacoes.create(nome="Sala B", estoque_id=estoque)
    tipo = TiposEquipamento.create(nome="Impressora")
    categoria = Categorias.create(nome="Periférico")

    equipamento = Equipamentos.create(
        nome="Impressora HP",
        status=True,
        estoque_id=estoque,
        tipo_id=tipo,
        categoria_id=categoria,
        localizacao_id=localizacao1
    )

    return {
        "estoque_id": estoque.id,
        "localizacao_origem": localizacao1.id,
        "localizacao_destino": localizacao2.id,
        "equipamento_id": equipamento.id
    }

def test_get_all_movement(client, headers, setup_movimentacao):
    # Criar uma movimentação antes do GET
    payload = {
        "equipamento_id": setup_movimentacao["equipamento_id"],  # Alterar para 'equipamento_id'
        "tipo_movimentacao": "transferencia",
        "localizacao_id": setup_movimentacao["localizacao_destino"]
    }

    client.post("/movimentacoes", json=payload, headers=headers)

    response = client.get("/movimentacoes", headers=headers)
    assert response.status_code == 200
    movimentacoes = response.get_json()["historico_de_movimentacoes"]
    assert isinstance(movimentacoes, list)
    assert any(m["equipamento_id"] == setup_movimentacao["equipamento_id"] for m in movimentacoes)

def test_create_movimentacao(client, headers, setup_movimentacao):
    payload = {
        "equipamento_id": setup_movimentacao["equipamento_id"],  # Alterar para 'equipamento_id'
        "tipo_movimentacao": "transferencia",
        "localizacao_id": setup_movimentacao["localizacao_destino"]
    }

    response = client.post("/movimentacoes", json=payload, headers=headers)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Movimentação registrada com sucesso"
    assert json_data["data"]["equipamento_id"] == setup_movimentacao["equipamento_id"]
    assert json_data["data"]["localizacao_id"] == setup_movimentacao["localizacao_destino"]
