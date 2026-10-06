import psycopg
import pytest
from fastapi.testclient import TestClient

import app as app_module
from app import app, get_connection


@pytest.fixture
def client():
    # "with" runs the lifespan, so the notes table is created before each test
    with TestClient(app) as test_client:
        with get_connection() as conn:
            conn.execute("TRUNCATE notes RESTART IDENTITY")
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_database_down(client, monkeypatch):
    def broken_connection():
        raise psycopg.OperationalError("database is down")

    monkeypatch.setattr(app_module, "get_connection", broken_connection)

    response = client.get("/health")

    assert response.status_code == 503


def test_create_note(client):
    response = client.post("/notes", json={"text": "first note"})

    assert response.status_code == 201
    assert response.json() == {"text": "first note"}


def test_list_notes(client):
    client.post("/notes", json={"text": "first note"})
    client.post("/notes", json={"text": "second note"})

    response = client.get("/notes")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "text": "first note"},
        {"id": 2, "text": "second note"},
    ]


def test_list_notes_empty(client):
    response = client.get("/notes")

    assert response.status_code == 200
    assert response.json() == []


def test_create_note_invalid_body(client):
    response = client.post("/notes", json={"wrong": "field"})

    assert response.status_code == 422
