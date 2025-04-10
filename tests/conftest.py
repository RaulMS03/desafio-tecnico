import pytest
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from peewee import SqliteDatabase

from app import create_app
from database.db import db
from models import Estoques, Usuarios, Localizacoes, TiposEquipamento, Categorias, Equipamentos, HistoricoMovimentacao

# Banco em memória para testes
test_db = SqliteDatabase(":memory:")

@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)
    return app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    db.initialize(test_db)
    db.connect(reuse_if_open=True)
    db.create_tables([
        Estoques, Usuarios, Localizacoes,
        TiposEquipamento, Categorias, Equipamentos,
        HistoricoMovimentacao
    ])

    # Dados mockados
    Usuarios.create(
        id=1,
        nome="admin",
        email="admin@example.com",
        senha_hash=generate_password_hash("admin"),
        papel="admin"
    )
    estoque = Estoques.create(id=1, nome="teste")
    Localizacoes.create(id=1, nome="Sala 1", estoque_id=estoque.id)
    TiposEquipamento.create(id=1, nome="Notebook")
    Categorias.create(id=1, nome="Informática")

    yield

    db.drop_tables([
        Estoques, Usuarios, Localizacoes,
        TiposEquipamento, Categorias, Equipamentos,
        HistoricoMovimentacao
    ])
    db.close()

@pytest.fixture
def token():
    return create_access_token(identity=1)

@pytest.fixture
def admin_token(app):
    with app.app_context():
        user = Usuarios.create(
            nome="admin",
            email="admin@admin.com",
            senha_hash=generate_password_hash("admin"),
            papel="admin"
        )
        return create_access_token(identity=str(user.id))  # 👈 ID como string

@pytest.fixture
def headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

