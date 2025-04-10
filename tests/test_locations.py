from models.localizacao import Localizacoes

def test_create_location(client, headers):
    payload = {
        "nome": "Corredor B",
        "estoque_id": 1
    }

    response = client.post("/localizacoes", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.get_json()["message"] == "Localização criada com sucesso"

def test_get_all_locations(client, headers):
    Localizacoes.create(nome="Corredor A", estoque_id=1)

    response = client.get("/localizacoes", headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert "Localizações" in data
    assert isinstance(data["Localizações"], list)
    assert any(loc["nome"] == "Corredor A" for loc in data["Localizações"])