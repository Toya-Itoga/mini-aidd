import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.database import engine
from src import models
from src.routers import lots, users

load_dotenv()

# ==========================
# アプリ初期化
# ==========================
app = FastAPI(title="農場日報管理アプリ")

# DBテーブル作成
models.Base.metadata.create_all(bind=engine)

# 静的ファイル配信
app.mount("/static", StaticFiles(directory="src/templates/static"), name="static")

# テンプレートエンジン
templates = Jinja2Templates(directory="src/templates")

# ==========================
# ルーター登録
# ==========================
app.include_router(lots.router)
app.include_router(users.router)


# ==========================
# 画面ルート
# ==========================

@app.get("/")
def index(request: Request):
    """メイン画面（コンテンツはHTMX経由でロード）"""
    return templates.TemplateResponse(request, "index.html", {})


# ==========================
# エントリーポイント
# ==========================
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    uvicorn.run("src.main:app", host=host, port=port, reload=True)
