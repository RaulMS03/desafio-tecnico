from models import Categorias

def test_create_category(client, headers):
    data = {"nome": "Eletrônicos"}
    response = client.post("/categorias", json=data, headers=headers)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Categoria criada com sucesso"

def test_get_all_categories(client, headers):
    Categorias.create(nome="Informática")
    response = client.get("/categorias", headers=headers)
    assert response.status_code == 200
    categorias = response.get_json()["Categorias"]
    assert isinstance(categorias, list)
    assert any(c["nome"] == "Informática" for c in categorias)