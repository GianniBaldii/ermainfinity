from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import HISTORY_FILE, NOTES_FILE, STATE_FILE
from app.main import app


FILES_TO_RESTORE = [STATE_FILE, HISTORY_FILE, NOTES_FILE]


@pytest.fixture(autouse=True)
def restore_data_files():
    snapshots = {}
    for file_path in FILES_TO_RESTORE:
        path = Path(file_path)
        snapshots[path] = path.read_text(encoding="utf-8") if path.exists() else None

    yield

    for path, content in snapshots.items():
        if content is None:
            if path.exists():
                path.unlink()
            continue

        path.write_text(content, encoding="utf-8")


@pytest.fixture
def client():
    return TestClient(app)


def test_get_state(client):
    response = client.get("/state")

    assert response.status_code == 200
    data = response.json()
    assert {"status", "emotion", "message"} <= set(data)


def test_sleep_command(client):
    response = client.post("/command", json={"text": "ERMA dormite un rato"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "sleep"
    assert data["status"] == "sleep"
    assert "dormite" in data["matched_keywords"]


def test_unknown_command(client):
    response = client.post("/command", json={"text": "abrir portal imposible"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "unknown"
    assert data["emotion"] == "curioso"


def test_note_command_adds_note_and_history(client):
    response = client.post("/command", json={"text": "recordame comprar pilas"})

    assert response.status_code == 200
    assert response.json()["intent"] == "note_add"

    notes_response = client.get("/notes")
    history_response = client.get("/history")

    assert notes_response.status_code == 200
    assert history_response.status_code == 200
    assert notes_response.json()[-1]["text"] == "comprar pilas"
    assert history_response.json()[-1]["command"] == "recordame comprar pilas"


def test_datetime_command(client):
    response = client.post("/command", json={"text": "que hora es"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "datetime"
    assert "son las" in data["message"]
