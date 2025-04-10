import pytest
from werkzeug.security import generate_password_hash
from models import Usuarios

@pytest.fixture
def user_data():
    return {"nome": "admin", "email": "admin@admin.com", "senha": "admin", "papel": "admin"}

def test_register_user(client, user_data):
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert "message" in json_data
    assert json_data["message"] == "Usuário criado com sucesso"

def test_register_existing_user(client, user_data):
    Usuarios.create(
        nome="admin",
        email="admin@admin.com",
        senha_hash=generate_password_hash("admin"),
        papel="admin"
    )
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 409
    json_data = response.get_json()
    assert json_data["message"] == "Usuário já existe"

def test_login_user(client, user_data):
    Usuarios.create(
        nome="admin",
        email="admin@admin.com",
        senha_hash=generate_password_hash("admin"),
        papel="admin"
    )
    response = client.post("/auth/login", json={
        "email": user_data["email"],
        "senha": user_data["senha"]
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "token" in json_data
    assert "usuario" in json_data
    assert json_data["usuario"]["email"] == user_data["email"]

