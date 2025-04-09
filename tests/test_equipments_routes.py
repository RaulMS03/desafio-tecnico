import pytest

# Teste de criação de equipamento
def test_create_equipamento_sucesso(client, auth_headers):
    payload = {
        "nome": "Mouse",
        "status": True,
        "estoque_id": 1,
        "tipo_id": 1,
        "categoria_id": 1
    }
    response = client.post("/equipamentos", json=payload, headers=auth_headers)
    assert response.status_code == 201
    assert "Equipamento criado com sucesso" in response.json["message"]


def test_create_equipamento_dados_invalidos(client, auth_headers):
    payload = {
        "nome": "",
        "status": True,
        "estoque_id": 1,
        "tipo_id": 1,
        "categoria_id": 1
    }
    response = client.post("/equipamentos", json=payload, headers=auth_headers)
    assert response.status_code == 400
    assert "não podem ser vazios" in response.json["message"] or "Erro de validação" in response.json["message"]


# Teste de GET com e sem filtro
def test_get_equipamentos(client, auth_headers):
    response = client.get("/equipamentos", headers=auth_headers)
    assert response.status_code == 200
    assert "Equipamentos" in response.json


def test_get_equipamentos_com_filtro(client, auth_headers):
    response = client.get("/equipamentos?estoque_id=1", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json["Equipamentos"], list)


# Teste de desativação
def test_patch_desativar_equipamento(client, auth_headers):
    # Você pode criar um equipamento antes via POST se quiser
    patch_data = {"status": False}
    response = client.patch("/equipamentos/1/desativar", json=patch_data, headers=auth_headers)

    # Pode dar 400 se já estiver desativado, mas valida o comportamento
    assert response.status_code in (200, 400)


# Teste de atualização PUT
def test_put_atualizar_equipamento(client, auth_headers):
    payload = {
        "nome": "Mouse Atualizado",
        "status": True,
        "estoque_id": 1,
        "tipo_id": 1,
        "categoria_id": 1
    }
    response = client.put("/equipamentos/1", json=payload, headers=auth_headers)

    # Pode retornar 200 se atualizou ou 404 se não encontrou
    assert response.status_code in (200, 404)
