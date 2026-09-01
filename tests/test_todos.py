import pytest
from fastapi.testclient import TestClient

from app.main import app, _todos


@pytest.fixture(autouse=True)
def reset_store():
    _todos.clear()
    yield
    _todos.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_list_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo(client):
    response = client.post("/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Buy milk"
    assert body["completed"] is False


def test_create_then_list(client):
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second", "completed": True})

    response = client.get("/todos")
    assert response.status_code == 200
    titles = [t["title"] for t in response.json()]
    assert titles == ["First", "Second"]


def test_create_todo_validation_error(client):
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422
