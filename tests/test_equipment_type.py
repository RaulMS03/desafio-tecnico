from models import TiposEquipamento

def test_create_equipment_type(client, headers):
    data = {"nome": "Impressora"}
    response = client.post("/tipos-equipamento", json=data, headers=headers)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Tipo de Equipamento criado com sucesso"

def test_get_all_equipment_types(client, headers):
    TiposEquipamento.create(nome="Scanner")
    response = client.get("/tipos-equipamento", headers=headers)
    assert response.status_code == 200
    tipos = response.get_json()["tipos_de_equipamentos"]
    assert isinstance(tipos, list)
    assert any(t["nome"] == "Scanner" for t in tipos)