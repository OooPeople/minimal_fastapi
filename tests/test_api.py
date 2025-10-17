import pytest
from fastapi.testclient import TestClient
from app.main import app, _FAKE_DB

client = TestClient(app)

@pytest.fixture(autouse=True)
def _reset_db():
    # 每個測試前/後都清空，避免互相影響
    _FAKE_DB.clear()
    yield
    _FAKE_DB.clear()

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

def test_create_user_validation():
    # name 空字串、age < 0 都應驗證失敗
    bad = {"name": "", "age": -1}
    r = client.post("/users", json=bad)
    assert r.status_code == 422
