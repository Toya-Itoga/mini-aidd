from sqlalchemy.orm import Session
from src.models import Lot
from src.schemas import LotCreate, LotUpdate


# ==========================
# ロットリポジトリ（DBアクセス）
# ==========================

def get_all(db: Session) -> list[Lot]:
    """全ロットを登録日時の降順で取得する"""
    return db.query(Lot).order_by(Lot.created_at.desc()).all()


def get_by_lot_id(db: Session, lot_id: str) -> Lot | None:
    """ロットIDでロットを取得する"""
    return db.query(Lot).filter(Lot.lot_id == lot_id).first()


def create(db: Session, data: LotCreate) -> Lot:
    """ロットを登録する"""
    lot = Lot(**data.model_dump())
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot


def update(db: Session, lot: Lot, data: LotUpdate) -> Lot:
    """ロットを更新する"""
    for field, value in data.model_dump().items():
        setattr(lot, field, value)
    db.commit()
    db.refresh(lot)
    return lot
