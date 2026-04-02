from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import LotCreate, LotUpdate, LotResponse
from src.services import lot_service

router = APIRouter(prefix="/lots", tags=["lots"])
templates = Jinja2Templates(directory="src/templates")


# ==========================
# ロットAPIルート
# ==========================

@router.get("")
def list_lots(request: Request, db: Session = Depends(get_db)):
    """ロット一覧を返す。HTMXリクエストの場合はパーシャルHTML、直接アクセスはトップへリダイレクト"""
    lots = [LotResponse.model_validate(l).model_dump(mode="json") for l in lot_service.get_lots(db)]
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(request, "lots.html", {"lots": lots})
    return RedirectResponse(url="/", status_code=302)


@router.post("", response_model=LotResponse, status_code=status.HTTP_201_CREATED)
def create_lot(data: LotCreate, db: Session = Depends(get_db)):
    """ロットを新規登録する"""
    return lot_service.create_lot(db, data)


@router.patch("/{lot_id}", response_model=LotResponse)
def update_lot(lot_id: str, data: LotUpdate, db: Session = Depends(get_db)):
    """ロットを更新する"""
    return lot_service.update_lot(db, lot_id, data)


@router.get("/{lot_id}", response_model=LotResponse)
def get_lot(lot_id: str, db: Session = Depends(get_db)):
    """ロットIDでロットを取得する"""
    return lot_service.get_lot(db, lot_id)
