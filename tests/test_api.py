from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_create_user_ok():
    payload = {"name": "Alice", "age": 25}
    r = client.post("/users", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Alice"
    assert data["age"] == 25
    assert isinstance(data["id"], int) and data["id"] >= 1