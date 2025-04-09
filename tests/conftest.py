import pytest
from flask_jwt_extended import create_access_token

from app import create_app

@pytest.fixture
def app_instance():
    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret"  # ou use uma .env de testes
    return app

@pytest.fixture
def client(app_instance):
    with app_instance.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(app_instance):
    with app_instance.app_context():
        token = create_access_token(identity="usuario_teste")
        return {"Authorization": f"Bearer {token}"}