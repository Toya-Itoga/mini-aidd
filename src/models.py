from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.database import Base


# ==========================
# ロットモデル
# ==========================
class Lot(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lot_id = Column(String, unique=True, nullable=False)       # ロットID
    farm_name = Column(String, nullable=False)                  # 農場名
    house_name = Column(String, nullable=False)                 # ハウス名
    plant_count = Column(Integer, nullable=False)               # 栽培本数
    created_at = Column(DateTime, server_default=func.now())   # 登録日時


# ==========================
# ユーザモデル
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)     # ユーザ名
    full_name = Column(String, nullable=False)                  # 氏名
    role = Column(String, nullable=False)                       # 役割
    created_at = Column(DateTime, server_default=func.now())   # 登録日時
