from fastapi import APIRouter, Depends, Request, status
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
    """全ロット一覧をHTML描画する"""
    lots = [LotResponse.model_validate(l).model_dump(mode="json") for l in lot_service.get_lots(db)]
    return templates.TemplateResponse(request, "lots.html", {"lots": lots})


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
