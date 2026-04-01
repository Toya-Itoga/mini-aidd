from datetime import datetime
from pydantic import BaseModel, ConfigDict


# ==========================
# ロットスキーマ
# ==========================
class LotCreate(BaseModel):
    lot_id: str
    farm_name: str
    house_name: str
    plant_count: int


class LotUpdate(BaseModel):
    farm_name: str
    house_name: str
    plant_count: int


class LotResponse(LotCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================
# ユーザスキーマ
# ==========================
class UserCreate(BaseModel):
    username: str
    full_name: str
    role: str


class UserUpdate(BaseModel):
    full_name: str
    role: str


class UserResponse(UserCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
