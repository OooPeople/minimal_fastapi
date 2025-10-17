# Minimal FastAPI Demo

一個展示 FastAPI 核心功能的簡潔示範專案，包含 RESTful API 設計、資料驗證、測試覆蓋等現代 Python Web 開發最佳實踐。

## 🚀 專案特色

- **FastAPI 框架**：使用最新的 FastAPI 0.119.0，提供自動 API 文件生成
- **Pydantic 資料驗證**：強型別資料模型與自動驗證
- **完整測試覆蓋**：使用 pytest 進行單元測試
- **現代 Python**：支援 Python 3.13+ 與型別提示
- **依賴管理**：使用 uv 進行快速且可靠的套件管理

## 📋 API 端點

### 健康檢查
```http
GET /health
```
回傳服務狀態資訊

### 用戶管理
```http
POST /users
```
建立新用戶，支援以下欄位：
- `name` (必填): 用戶姓名，長度至少 1 字元
- `age` (必填): 年齡，範圍 0-120
- `email` (選填): 電子郵件地址

## 🛠️ 技術架構

### 核心技術棧
- **FastAPI**: 現代、快速的 Web 框架
- **Pydantic**: 資料驗證與序列化
- **Uvicorn**: ASGI 伺服器
- **pytest**: 測試框架
- **httpx**: HTTP 客戶端（測試用）

### 專案結構
```
minimal_fastapi/
├── app/
│   ├── __init__.py
│   └── main.py          # 主要應用程式邏輯
├── tests/
│   ├── __init__.py
│   └── test_api.py      # API 測試
├── pyproject.toml       # 專案配置與依賴
├── requirements.lock.txt # 鎖定的依賴版本
└── README.md
```

## 🚀 快速開始

### 環境需求
- Python 3.13+
- uv (推薦) 或 pip

### 安裝與執行

1. **複製專案**
```bash
git clone https://github.com/OooPeople/minimal_fastapi.git
cd minimal_fastapi
```

2. **安裝依賴**
```bash
# 使用 uv (推薦)
uv sync

# 或使用 pip
pip install -r requirements.txt
```

3. **啟動開發伺服器**
```bash
# 使用 uv
uv run uvicorn app.main:app --reload

# 或直接執行
uvicorn app.main:app --reload
```

4. **存取 API**
- API 文件：http://localhost:8000/docs
- 健康檢查：http://localhost:8000/health

### 執行測試
```bash
# 使用 uv
uv run pytest

# 或直接執行
pytest
```

## 📖 API 使用範例

### 建立用戶
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "張三",
       "age": 25,
       "email": "zhang@example.com"
     }'
```

### 健康檢查
```bash
curl http://localhost:8000/health
```

## 🧪 測試

專案包含完整的測試套件，涵蓋：
- ✅ 健康檢查端點測試
- ✅ 用戶建立功能測試
- ✅ 資料驗證測試
- ✅ 錯誤處理測試

執行測試：
```bash
uv run pytest -v
```

## 🔧 開發說明

### 資料模型
- `UserIn`: 輸入資料模型，包含驗證規則
- `UserOut`: 輸出資料模型，包含自動生成的 ID

### 資料儲存
目前使用記憶體儲存作為示範，實際專案中可替換為：
- PostgreSQL + SQLAlchemy
- MongoDB
- Redis
- 其他資料庫解決方案

### 擴展建議
- 新增用戶查詢、更新、刪除端點
- 實作資料庫整合
- 加入身份驗證與授權
- 新增日誌記錄
- 實作 API 限流
- 加入 Docker 容器化

## 📄 授權

此專案僅供學習與示範用途。

---

**開發者**: 彭品仁  
**聯絡方式**: alex040755@outlook.com  
**最後更新**: 2025年10月
