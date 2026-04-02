"""
ロット一覧 API テスト

対象エンドポイント:
  GET    /lots           — 一覧取得（HTMX経由）
  POST   /lots           — 新規登録
  GET    /lots/{lot_id}  — 個別取得
  PATCH  /lots/{lot_id}  — 更新
"""
from fastapi.testclient import TestClient


# ==========================
# テストデータ
# ==========================
LOT_PAYLOAD = {
    "lot_id": "LOT-001",
    "farm_name": "第一農場",
    "house_name": "A棟",
    "plant_count": 500,
}

HTMX_HEADERS = {"HX-Request": "true"}


# ==========================
# GET /lots — 一覧取得
# ==========================

class TestListLots:
    def test_empty_returns_200(self, client: TestClient):
        """登録データなしでも 200 を返す"""
        res = client.get("/lots", headers=HTMX_HEADERS)
        assert res.status_code == 200

    def test_empty_shows_empty_state(self, client: TestClient):
        """ロットが0件の場合、空状態メッセージを含む"""
        res = client.get("/lots", headers=HTMX_HEADERS)
        assert "ロットが登録されていません" in res.text

    def test_redirect_on_direct_access(self, client: TestClient):
        """HX-Request ヘッダーなしの直接アクセスは / へリダイレクトする"""
        res = client.get("/lots", follow_redirects=False)
        assert res.status_code == 302
        assert res.headers["location"] == "/"

    def test_lists_registered_lots(self, client: TestClient):
        """登録済みロットが一覧に表示される"""
        client.post("/lots", json=LOT_PAYLOAD)

        res = client.get("/lots", headers=HTMX_HEADERS)
        assert res.status_code == 200
        assert LOT_PAYLOAD["lot_id"] in res.text
        assert LOT_PAYLOAD["farm_name"] in res.text


# ==========================
# POST /lots — 新規登録
# ==========================

class TestCreateLot:
    def test_create_returns_201(self, client: TestClient):
        """正常登録で 201 を返す"""
        res = client.post("/lots", json=LOT_PAYLOAD)
        assert res.status_code == 201

    def test_create_response_body(self, client: TestClient):
        """レスポンスに登録内容が含まれる"""
        res = client.post("/lots", json=LOT_PAYLOAD)
        data = res.json()
        assert data["lot_id"] == LOT_PAYLOAD["lot_id"]
        assert data["farm_name"] == LOT_PAYLOAD["farm_name"]
        assert data["house_name"] == LOT_PAYLOAD["house_name"]
        assert data["plant_count"] == LOT_PAYLOAD["plant_count"]

    def test_create_duplicate_returns_409(self, client: TestClient):
        """同一ロットIDの二重登録は 409 を返す"""
        client.post("/lots", json=LOT_PAYLOAD)
        res = client.post("/lots", json=LOT_PAYLOAD)
        assert res.status_code == 409

    def test_create_missing_field_returns_422(self, client: TestClient):
        """必須フィールドが欠けている場合は 422 を返す"""
        res = client.post("/lots", json={"lot_id": "LOT-001"})
        assert res.status_code == 422

    def test_create_invalid_plant_count_returns_422(self, client: TestClient):
        """plant_count に文字列を渡した場合は 422 を返す"""
        payload = {**LOT_PAYLOAD, "plant_count": "invalid"}
        res = client.post("/lots", json=payload)
        assert res.status_code == 422


# ==========================
# GET /lots/{lot_id} — 個別取得
# ==========================

class TestGetLot:
    def test_get_existing_lot(self, client: TestClient):
        """登録済みロットを正常に取得できる"""
        client.post("/lots", json=LOT_PAYLOAD)
        res = client.get(f"/lots/{LOT_PAYLOAD['lot_id']}")
        assert res.status_code == 200
        assert res.json()["lot_id"] == LOT_PAYLOAD["lot_id"]

    def test_get_nonexistent_lot_returns_404(self, client: TestClient):
        """存在しないロットIDは 404 を返す"""
        res = client.get("/lots/NOT-EXIST")
        assert res.status_code == 404


# ==========================
# PATCH /lots/{lot_id} — 更新
# ==========================

class TestUpdateLot:
    def test_update_returns_200(self, client: TestClient):
        """正常更新で 200 を返す"""
        client.post("/lots", json=LOT_PAYLOAD)
        res = client.patch(f"/lots/{LOT_PAYLOAD['lot_id']}", json={
            "farm_name": "第二農場",
            "house_name": "B棟",
            "plant_count": 300,
        })
        assert res.status_code == 200

    def test_update_reflects_new_values(self, client: TestClient):
        """更新後のレスポンスに新しい値が反映されている"""
        client.post("/lots", json=LOT_PAYLOAD)
        update_payload = {"farm_name": "第二農場", "house_name": "B棟", "plant_count": 300}
        res = client.patch(f"/lots/{LOT_PAYLOAD['lot_id']}", json=update_payload)
        data = res.json()
        assert data["farm_name"] == "第二農場"
        assert data["house_name"] == "B棟"
        assert data["plant_count"] == 300

    def test_update_nonexistent_lot_returns_404(self, client: TestClient):
        """存在しないロットの更新は 404 を返す"""
        res = client.patch("/lots/NOT-EXIST", json={
            "farm_name": "農場",
            "house_name": "棟",
            "plant_count": 100,
        })
        assert res.status_code == 404
