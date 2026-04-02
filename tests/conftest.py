"""
テスト共通フィクスチャ

- テスト環境では test.db を使用する（CLAUDE.md の環境分離ルールに従う）
- .env より先に環境変数を設定することで dotenv による上書きを防ぐ
- 各テスト関数は独立したDBセッションを持ち、テスト後にデータをロールバックする
"""
import os
import pytest

# dotenv より先に設定することで .env の値に上書きされない
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.database import Base, get_db

# ==========================
# テスト用DBエンジン
# ==========================
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ==========================
# セッションスコープ: DBテーブルをセットアップ / 破棄
# ==========================
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """テストセッション開始時にテーブルを作成し、終了時に削除する"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ==========================
# 関数スコープ: 各テスト後にデータをロールバック
# ==========================
@pytest.fixture
def db_session():
    """各テストで独立したトランザクションを使用し、終了後にロールバックする"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ==========================
# テストクライアント（get_db を差し替え）
# ==========================
@pytest.fixture
def client(db_session):
    """テスト用DBセッションで get_db をオーバーライドした TestClient を返す"""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
