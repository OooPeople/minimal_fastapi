from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Minimal API", version="0.1.0")

class UserIn(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=120)
    email: str | None = None

class UserOut(BaseModel):
    id: int
    name: str
    age: int
    email: str | None = None


# 最小健康檢查
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# 先用記憶體假資料庫
_FAKE_DB: list[UserOut] = []

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn) -> UserOut:
    new = UserOut(id=len(_FAKE_DB) + 1, **user.model_dump())
    _FAKE_DB.append(new)
    return new




