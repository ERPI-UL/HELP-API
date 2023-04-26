import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise

from app.main import app
from app.models.action import Action
from app.models.language import Language
from app.models.type import Type
from app.utils import init_db_with_data

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
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models.user", "app.models.language"]})
    await Tortoise.generate_schemas()
    response = client.post("/users", json={"username": "lumiere", "firstname": "Jean-Jacques",
                                           "lastname": "Rousseau", "email": "jean.jacques.rousseau@gmail.com",
                                           "password": "motdepasse"})
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "lumiere", "firstname": "Jean-Jacques",
                               "lastname": "Rousseau", "email": "jean.jacques.rousseau@gmail.com",
                               "adminLevel": 1}


@pytest.mark.asyncio
async def test_linked_list():
    """Test the linked list endpoint"""
    print("test_linked_list() called")
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["app.models.action", "app.models.type", "app.models.language", "app.models.user", "app.models.artifact"]})
    await Tortoise.generate_schemas()
    await init_db_with_data()
    action = await Action.create(name="test", description="test", tag="test", type=await Type.get(id=1), x=0, y=0, z=0, language=await Language.get(code="fr"))
    action.next = await Action.create(name="test2", description="test2", tag="test2", type=await Type.get(id=1), x=0, y=0, z=0, language=await Language.get(code="fr"))
    action.previous = await Action.create(name="test3", description="test3", tag="test3", type=await Type.get(id=1), x=0, y=0, z=0, language=await Language.get(code="fr"))
    await action.save()

    from app.models.action import ActionInPatch
    artifact = ActionInPatch(next=action.next.id, previous=action.previous.id, artifactID=None)
    print(artifact)

    assert 1 == 2
