import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import engine, get_db
from src import models
from src.routers import lots, users
from src.services import lot_service
from src.schemas import LotResponse

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
def index(request: Request, db: Session = Depends(get_db)):
    """ロット一覧画面"""
    # SQLAlchemy オブジェクトを tojson で扱えるよう dict に変換する
    lots_list = [LotResponse.model_validate(lot).model_dump(mode="json") for lot in lot_service.get_lots(db)]
    return templates.TemplateResponse(request, "index.html", {"lots": lots_list})


# ==========================
# エントリーポイント
# ==========================
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    uvicorn.run("src.main:app", host=host, port=port, reload=True)
