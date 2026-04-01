from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories import lot_repository
from src.schemas import LotCreate, LotUpdate, LotResponse


# ==========================
# ロットサービス（ビジネスロジック）
# ==========================

def get_lots(db: Session) -> list[LotResponse]:
    """全ロットを取得する"""
    return lot_repository.get_all(db)


def get_lot(db: Session, lot_id: str) -> LotResponse:
    """ロットIDでロットを取得する。存在しない場合は404を返す"""
    lot = lot_repository.get_by_lot_id(db, lot_id)
    if not lot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ロットが見つかりません")
    return lot


def create_lot(db: Session, data: LotCreate) -> LotResponse:
    """ロットを登録する。ロットIDが重複する場合は409を返す"""
    if lot_repository.get_by_lot_id(db, data.lot_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ロットIDが既に存在します")
    return lot_repository.create(db, data)


def update_lot(db: Session, lot_id: str, data: LotUpdate) -> LotResponse:
    """ロットを更新する。存在しない場合は404を返す"""
    lot = lot_repository.get_by_lot_id(db, lot_id)
    if not lot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ロットが見つかりません")
    return lot_repository.update(db, lot, data)
