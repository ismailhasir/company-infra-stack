import pytest
from fastapi.testclient import TestClient
from app import app, notes_list

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_notes():
    # notes_list is a module-level list, so clear it to keep tests independent
    notes_list.clear()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_note():
    response = client.post("/notes", json={"text": "first note"})

    assert response.status_code == 201
    assert response.json() == {"text": "first note"}


def test_list_notes():
    client.post("/notes", json={"text": "first note"})
    client.post("/notes", json={"text": "second note"})

    response = client.get("/notes")

    assert response.status_code == 200
    assert response.json() == [{"text": "first note"}, {"text": "second note"}]


def test_list_notes_empty():
    response = client.get("/notes")

    assert response.status_code == 200
    assert response.json() == []


def test_create_note_invalid_body():
    response = client.post("/notes", json={"wrong": "field"})

    assert response.status_code == 422
