from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import UserCreate, UserUpdate, UserResponse
from src.services import user_service

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="src/templates")


# ==========================
# ユーザAPIルート
# ==========================

@router.get("")
def list_users(request: Request, db: Session = Depends(get_db)):
    """ユーザ一覧を返す。HTMXリクエストの場合はパーシャルHTML、直接アクセスはトップへリダイレクト"""
    users = [UserResponse.model_validate(u).model_dump(mode="json") for u in user_service.get_users(db)]
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(request, "users.html", {"users": users})
    return RedirectResponse(url="/", status_code=302)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    """ユーザを新規登録する"""
    return user_service.create_user(db, data)


@router.patch("/{username}", response_model=UserResponse)
def update_user(username: str, data: UserUpdate, db: Session = Depends(get_db)):
    """ユーザを更新する"""
    return user_service.update_user(db, username, data)


@router.get("/{username}", response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    """ユーザ名でユーザを取得する"""
    return user_service.get_user(db, username)
