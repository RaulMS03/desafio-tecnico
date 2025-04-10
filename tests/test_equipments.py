import pytest
from models import Localizacoes, Categorias, TiposEquipamento, Estoques, Equipamentos

@pytest.fixture
def setup_equipamento():
    estoque = Estoques.create(nome="Estoque Central")
    tipo = TiposEquipamento.create(nome="Monitor")
    categoria = Categorias.create(nome="Periférico")
    localizacao = Localizacoes.create(nome="Corredor A", estoque_id=estoque)

    equipamento = Equipamentos.create(
        nome="Monitor Dell",
        status=True,
        estoque_id=estoque,
        tipo_id=tipo,
        categoria_id=categoria,
        localizacao_id=localizacao
    )
    return equipamento

def test_create_equipamento(client, headers):
    estoque = Estoques.create(nome="Estoque A")
    tipo = TiposEquipamento.create(nome="Notebook")
    categoria = Categorias.create(nome="Informática")
    localizacao = Localizacoes.create(nome="Corredor B", estoque_id=estoque)

    payload = {
        "nome": "Notebook Lenovo",
        "status": True,
        "estoque_id": estoque.id,
        "tipo_id": tipo.id,
        "categoria_id": categoria.id,
        "localizacao_id": localizacao.id
    }

    response = client.post("/equipamentos", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Equipamento criado com sucesso"

def test_get_all_equipamentos(client, headers, setup_equipamento):
    response = client.get("/equipamentos", headers=headers)
    assert response.status_code == 200
    equipamentos = response.get_json()["Equipamentos"]
    assert isinstance(equipamentos, list)
    assert any(e["nome"] == setup_equipamento.nome for e in equipamentos)

def test_disable_equipamento(client, headers, setup_equipamento):
    response = client.patch(
        f"/equipamentos/{setup_equipamento.id}/desativar",
        json={"status": False},
        headers=headers
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Equipamento desativado com sucesso"

def test_update_equipamento(client, headers, setup_equipamento):
    payload = {
        "nome": "Monitor Atualizado",
        "status": True,
        "estoque_id": setup_equipamento.estoque_id.id,
        "tipo_id": setup_equipamento.tipo_id.id,
        "categoria_id": setup_equipamento.categoria_id.id,
        "localizacao_id": setup_equipamento.localizacao_id.id
    }

    response = client.put(f"/equipamentos/{setup_equipamento.id}", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Equipamento atualizado com sucesso"
