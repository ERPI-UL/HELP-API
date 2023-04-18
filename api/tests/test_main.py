from fastapi.testclient import TestClient
import pytest
from tortoise import Tortoise

from app.main import app

client = TestClient(app)

# test hello world


# appel une seule fois au lancement de tout les tests
@pytest.fixture(scope="session", autouse=True)
async def init_db():
    """Init the database"""
    print("init_db() called")
    # use tortoise with sqlite
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    # generate the schema
    await Tortoise.generate_schemas()
    yield


def test_health():
    """Test the health endpoint"""
    print("test_health() called")
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


@pytest.mark.asyncio
async def test_create_user():
    """Test the create user endpoint"""
    print("test_create_user() called")
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    response = client.post("/users", json={"username": "lumiere", "firstname": "Jean-Jacques",
                                           "lastname": "Rousseau", "email": "jean.jacques.rousseau@gmail.com",
                                           "password_hash": "motdepasse"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "lumiere", "firstname": "Jean-Jacques",
                               "lastname": "Rousseau", "email": "jean.jacques.rousseau@gmail.com",
                               "adminLevel": 1}
