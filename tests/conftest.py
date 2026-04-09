import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models import Usuario, RolEnum
from app.security import hash_password

# Base de datos en memoria para tests
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Crea y destruye la BD de test en cada test."""
    Base.metadata.create_all(bind=engine_test)
    # Crear usuario admin de test
    db = TestingSessionLocal()
    admin = Usuario(
        username="testadmin",
        nombre="Test Admin",
        password_hash=hash_password("testpass"),
        rol=RolEnum.admin,
        activo=True
    )
    db.add(admin)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def token(client):
    """Devuelve un token JWT de admin válido."""
    res = client.post(
        "/api/auth/login",
        data={"username": "testadmin", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return res.json()["access_token"]


@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def pedido_base(client, auth_headers):
    """Crea un pedido de prueba y devuelve sus datos."""
    res = client.post("/api/pedidos/", json={
        "cliente": "Cliente Test",
        "articulo": "Camiseta Test",
        "talla": "M",
        "precio": 29.99,
        "canal": "whatsapp"
    }, headers=auth_headers)
    return res.json()