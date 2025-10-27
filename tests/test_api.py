# tests/test_api.py
# -------------------------------------------------------
# 這支測試示範：
# - 使用 TestClient 在「記憶體內」測 API，不需真正開 8000 port
# - fixture 在每個測試前後清空「記憶體 DB」，避免測試互相污染
# - 覆蓋成功情境、驗證失敗、404/400 錯誤情境
# -------------------------------------------------------

import pytest
from fastapi.testclient import TestClient
from app.main import app, _FAKE_DB

# 用你的 app 建一個測試用 HTTP 客戶端
client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_db():
    """
    autouse=True：每個測試自動套用。
    測試前/後都清空 _FAKE_DB，確保測試彼此獨立、可重現。
    """
    _FAKE_DB.clear()
    yield
    _FAKE_DB.clear()


def test_health():
    """GET /health 應 200 並回固定 JSON"""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_user_ok():
    """POST /users 正常建立：201，且回傳含自增 id 與欄位"""
    payload = {"name": "Alice", "age": 25}
    r = client.post("/users", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Alice"
    assert data["age"] == 25
    assert isinstance(data["id"], int) and data["id"] >= 1


def test_create_user_validation():
    """POST /users 驗證失敗：name 空字串、age < 0 → 422"""
    bad = {"name": "", "age": -1}
    r = client.post("/users", json=bad)
    assert r.status_code == 422


def test_list_users_empty():
    """GET /users 初始應為空陣列 []"""
    r = client.get("/users")
    assert r.status_code == 200
    assert r.json() == []


def test_get_user_by_id_found():
    """先建立一筆，再 GET /users/1 應 200 且名稱正確"""
    client.post("/users", json={"name": "Alice", "age": 25})
    r = client.get("/users/1")
    assert r.status_code == 200
    assert r.json()["name"] == "Alice"


def test_get_user_by_id_404():
    """查詢不存在的 id 應回 404 與固定訊息"""
    r = client.get("/users/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "user not found"


def test_create_user_duplicate_name_400():
    """名稱重複時，第二次建立應回 400 與固定訊息"""
    client.post("/users", json={"name": "Alice", "age": 25})
    r = client.post("/users", json={"name": "Alice", "age": 30})
    assert r.status_code == 400
    assert r.json()["detail"] == "name already exists"
