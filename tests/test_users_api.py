"""
ユーザ管理 API テスト

対象エンドポイント:
  GET    /users              — 一覧取得（HTMX経由）
  POST   /users              — 新規登録
  GET    /users/{username}   — 個別取得
  PATCH  /users/{username}   — 更新
"""
from fastapi.testclient import TestClient


# ==========================
# テストデータ
# ==========================
USER_PAYLOAD = {
    "username": "yamada_taro",
    "full_name": "山田 太郎",
    "role": "管理者",
}

HTMX_HEADERS = {"HX-Request": "true"}


# ==========================
# GET /users — 一覧取得
# ==========================

class TestListUsers:
    def test_empty_returns_200(self, client: TestClient):
        """登録データなしでも 200 を返す"""
        res = client.get("/users", headers=HTMX_HEADERS)
        assert res.status_code == 200

    def test_empty_shows_empty_state(self, client: TestClient):
        """ユーザが0件の場合、空状態メッセージを含む"""
        res = client.get("/users", headers=HTMX_HEADERS)
        assert "ユーザが登録されていません" in res.text

    def test_redirect_on_direct_access(self, client: TestClient):
        """HX-Request ヘッダーなしの直接アクセスは / へリダイレクトする"""
        res = client.get("/users", follow_redirects=False)
        assert res.status_code == 302
        assert res.headers["location"] == "/"

    def test_lists_registered_users(self, client: TestClient):
        """登録済みユーザが一覧に表示される"""
        client.post("/users", json=USER_PAYLOAD)

        res = client.get("/users", headers=HTMX_HEADERS)
        assert res.status_code == 200
        assert USER_PAYLOAD["username"] in res.text
        assert USER_PAYLOAD["full_name"] in res.text


# ==========================
# POST /users — 新規登録
# ==========================

class TestCreateUser:
    def test_create_returns_201(self, client: TestClient):
        """正常登録で 201 を返す"""
        res = client.post("/users", json=USER_PAYLOAD)
        assert res.status_code == 201

    def test_create_response_body(self, client: TestClient):
        """レスポンスに登録内容が含まれる"""
        res = client.post("/users", json=USER_PAYLOAD)
        data = res.json()
        assert data["username"] == USER_PAYLOAD["username"]
        assert data["full_name"] == USER_PAYLOAD["full_name"]
        assert data["role"] == USER_PAYLOAD["role"]

    def test_create_duplicate_returns_409(self, client: TestClient):
        """同一ユーザ名の二重登録は 409 を返す"""
        client.post("/users", json=USER_PAYLOAD)
        res = client.post("/users", json=USER_PAYLOAD)
        assert res.status_code == 409

    def test_create_missing_field_returns_422(self, client: TestClient):
        """必須フィールドが欠けている場合は 422 を返す"""
        res = client.post("/users", json={"username": "yamada_taro"})
        assert res.status_code == 422


# ==========================
# GET /users/{username} — 個別取得
# ==========================

class TestGetUser:
    def test_get_existing_user(self, client: TestClient):
        """登録済みユーザを正常に取得できる"""
        client.post("/users", json=USER_PAYLOAD)
        res = client.get(f"/users/{USER_PAYLOAD['username']}")
        assert res.status_code == 200
        assert res.json()["username"] == USER_PAYLOAD["username"]

    def test_get_nonexistent_user_returns_404(self, client: TestClient):
        """存在しないユーザ名は 404 を返す"""
        res = client.get("/users/not_exist")
        assert res.status_code == 404


# ==========================
# PATCH /users/{username} — 更新
# ==========================

class TestUpdateUser:
    def test_update_returns_200(self, client: TestClient):
        """正常更新で 200 を返す"""
        client.post("/users", json=USER_PAYLOAD)
        res = client.patch(f"/users/{USER_PAYLOAD['username']}", json={
            "full_name": "山田 花子",
            "role": "作業員",
        })
        assert res.status_code == 200

    def test_update_reflects_new_values(self, client: TestClient):
        """更新後のレスポンスに新しい値が反映されている"""
        client.post("/users", json=USER_PAYLOAD)
        update_payload = {"full_name": "山田 花子", "role": "作業員"}
        res = client.patch(f"/users/{USER_PAYLOAD['username']}", json=update_payload)
        data = res.json()
        assert data["full_name"] == "山田 花子"
        assert data["role"] == "作業員"

    def test_update_nonexistent_user_returns_404(self, client: TestClient):
        """存在しないユーザの更新は 404 を返す"""
        res = client.patch("/users/not_exist", json={
            "full_name": "存在しない",
            "role": "作業員",
        })
        assert res.status_code == 404
