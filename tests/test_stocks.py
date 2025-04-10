from models.estoque import Estoques

def test_create_stock(client, headers):
    data = {"nome": "Estoque de Teste"}
    response = client.post("/estoques", json=data, headers=headers)

    assert response.status_code == 201
    assert response.get_json()["message"] == "Estoque criado com sucesso"

def test_get_all_stocks(client, headers):
    Estoques.create(nome="Estoque Leste")
    response = client.get("/estoques", headers=headers)
    assert response.status_code == 200
    estoques = response.get_json()["Estoques"]
    assert isinstance(estoques, list)
    assert any(e["nome"] == "Estoque Leste" for e in estoques)

def test_disable_stock(client, headers):
    estoque = Estoques.create(nome="Estoque Norte")
    response = client.patch(
        f"/estoques/{estoque.id}/desativar",
        json={"status": False},
        headers=headers
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Estoque desativado com sucesso"
