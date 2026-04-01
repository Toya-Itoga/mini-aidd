from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories import user_repository
from src.schemas import UserCreate, UserUpdate, UserResponse


# ==========================
# ユーザサービス（ビジネスロジック）
# ==========================

def get_users(db: Session) -> list[UserResponse]:
    """全ユーザを取得する"""
    return user_repository.get_all(db)


def get_user(db: Session, username: str) -> UserResponse:
    """ユーザ名でユーザを取得する。存在しない場合は404を返す"""
    user = user_repository.get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ユーザが見つかりません")
    return user


def create_user(db: Session, data: UserCreate) -> UserResponse:
    """ユーザを登録する。ユーザ名が重複する場合は409を返す"""
    if user_repository.get_by_username(db, data.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ユーザ名が既に存在します")
    return user_repository.create(db, data)


def update_user(db: Session, username: str, data: UserUpdate) -> UserResponse:
    """ユーザを更新する。存在しない場合は404を返す"""
    user = user_repository.get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ユーザが見つかりません")
    return user_repository.update(db, user, data)
