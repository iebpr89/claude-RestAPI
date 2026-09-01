import pytest
from fastapi.testclient import TestClient

from app.main import app, store


@pytest.fixture(autouse=True)
def reset_store():
    store.clear()
    yield
    store.clear()


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


def test_ids_are_sequential_and_reset_between_tests(client):
    first = client.post("/todos", json={"title": "First"}).json()
    second = client.post("/todos", json={"title": "Second"}).json()
    assert (first["id"], second["id"]) == (1, 2)


def test_create_todo_validation_error(client):
    response = client.post("/todos", json={"title": ""})
    assert response.status_code == 422


def test_get_todo(client):
    created = client.post("/todos", json={"title": "Read book"}).json()
    response = client.get(f"/todos/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_todo_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_replace_todo(client):
    created = client.post("/todos", json={"title": "Old", "completed": False}).json()
    response = client.put(
        f"/todos/{created['id']}", json={"title": "New", "completed": True}
    )
    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "title": "New", "completed": True}


def test_replace_todo_not_found(client):
    response = client.put("/todos/999", json={"title": "Nope"})
    assert response.status_code == 404


def test_patch_todo_partial(client):
    created = client.post("/todos", json={"title": "Task", "completed": False}).json()
    response = client.patch(f"/todos/{created['id']}", json={"completed": True})
    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "title": "Task", "completed": True}


def test_patch_todo_empty_body_is_noop(client):
    created = client.post("/todos", json={"title": "Task"}).json()
    response = client.patch(f"/todos/{created['id']}", json={})
    assert response.status_code == 200
    assert response.json() == created


def test_patch_todo_not_found(client):
    response = client.patch("/todos/999", json={"completed": True})
    assert response.status_code == 404


def test_patch_todo_validation_error(client):
    created = client.post("/todos", json={"title": "Task"}).json()
    response = client.patch(f"/todos/{created['id']}", json={"title": ""})
    assert response.status_code == 422


def test_delete_todo(client):
    created = client.post("/todos", json={"title": "Delete me"}).json()
    response = client.delete(f"/todos/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/todos/{created['id']}").status_code == 404


def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404
