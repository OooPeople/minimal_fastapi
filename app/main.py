# app/main.py
# ---------------------------------------------
# 這支檔案示範一個最小但完整的 Users API：
# - GET  /health          健康檢查
# - POST /users           建立使用者（含 Pydantic 驗證與「名稱不可重複」的錯誤處理）
# - GET  /users           取得所有使用者清單
# - GET  /users/{user_id} 取得單一使用者（找不到回 404）
# ---------------------------------------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# 建立 FastAPI 應用實例；title/version 會顯示在 /docs
app = FastAPI(title="Minimal API", version="0.2.0")


# ---------- (1) 定義資料模型：輸入與輸出 ----------

class UserIn(BaseModel):
    """
    用戶建立請求模型（Request Schema）
    - name: 至少 1 個字
    - age:  0 ~ 120
    - email: 可省略（None）
    """
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=120)
    email: str | None = None


class UserOut(BaseModel):
    """
    用戶回應模型（Response Schema）
    - id:    系統產生的流水號
    - name, age, email: 與輸入相同
    使用 response_model=UserOut 時，FastAPI 會依此 schema 輸出 JSON
    """
    id: int
    name: str
    age: int
    email: str | None = None


# ---------- (2) 簡易「記憶體資料庫」 ----------
# 真實專案會換成資料庫（例如 Postgres）。這裡用 list 模擬即可。
_FAKE_DB: list[UserOut] = []


# ---------- (3) 路由實作 ----------

@app.get("/health")
def health() -> dict[str, str]:
    """
    健康檢查：用最簡單的型別（dict）回傳，FastAPI 會自動轉成 JSON。
    加上回傳型別註記，有助於補完與靜態檢查。
    """
    return {"status": "ok"}


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn) -> UserOut:
    """
    建立使用者：
    - FastAPI 會把請求 JSON 轉成 UserIn，並自動做 Pydantic 驗證
    - 若 name 重複，回 400 Bad Request
    - 建立後回 201，並依 UserOut schema 輸出（避免多曝露內部欄位）
    """
    # (A) 名稱重複檢查：只要 _FAKE_DB 內有任何人重名，就回 400
    if any(u.name == user.name for u in _FAKE_DB):
        raise HTTPException(status_code=400, detail="name already exists")

    # (B) 產生流水號 id；將 "驗證過的 user" 轉成 dict 後解包到 UserOut
    #     model_dump()：把 Pydantic 模型 → 乾淨 dict
    #     **dict：把 dict 的鍵值展開成關鍵字參數
    new = UserOut(id=len(_FAKE_DB) + 1, **user.model_dump())

    # (C) 寫入「記憶體資料庫」
    _FAKE_DB.append(new)

    # (D) 回傳 UserOut，FastAPI 會轉成 JSON，並套用 response_model
    return new


@app.get("/users", response_model=list[UserOut])
def list_users() -> list[UserOut]:
    """
    列出所有使用者：
    - 直接回傳目前「記憶體資料庫」內容
    - response_model=list[UserOut] 讓文件清楚顯示回傳陣列的元素型別
    """
    return _FAKE_DB


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int) -> UserOut:
    """
    取得單一使用者：
    - 路徑參數 user_id 由 FastAPI 轉成 int
    - 找到回 200；找不到回 404（拋 HTTPException）
    """
    for u in _FAKE_DB:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=404, detail="user not found")
