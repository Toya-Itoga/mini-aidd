from sqlalchemy.orm import Session
from src.models import User
from src.schemas import UserCreate, UserUpdate


# ==========================
# ユーザリポジトリ（DBアクセス）
# ==========================

def get_all(db: Session) -> list[User]:
    """全ユーザを登録日時の降順で取得する"""
    return db.query(User).order_by(User.created_at.desc()).all()


def get_by_username(db: Session, username: str) -> User | None:
    """ユーザ名でユーザを取得する"""
    return db.query(User).filter(User.username == username).first()


def create(db: Session, data: UserCreate) -> User:
    """ユーザを登録する"""
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, data: UserUpdate) -> User:
    """ユーザを更新する"""
    for field, value in data.model_dump().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user
