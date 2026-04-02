# 農場日報管理アプリ

農場のロット・ユーザをブラウザから管理するWebアプリケーションです。

## 機能

- **ロット管理** — ロットの一覧表示・新規登録・編集
- **ユーザ管理** — ユーザの一覧表示・新規登録・編集
- **ダークモード** — ライト / ダークの切り替え（localStorage に保持）

## 技術スタック

| レイヤー | 使用技術 |
|---|---|
| サーバ | FastAPI + uvicorn |
| DB | SQLite + SQLAlchemy |
| バリデーション | Pydantic v2 |
| テンプレート | Jinja2 (SSR) |
| フロントエンド | HTMX + Alpine.js |

## ディレクトリ構成

```
mini-aidd/
├── src/
│   ├── main.py              # アプリ初期化・ルート定義
│   ├── database.py          # DB接続
│   ├── models.py            # SQLAlchemyモデル
│   ├── schemas.py           # Pydanticスキーマ
│   ├── routers/
│   │   ├── lots.py          # ロット API (/lots)
│   │   └── users.py         # ユーザ API (/users)
│   ├── services/
│   │   ├── lot_service.py   # ロットビジネスロジック
│   │   └── user_service.py  # ユーザビジネスロジック
│   ├── repositories/
│   │   ├── lot_repository.py
│   │   └── user_repository.py
│   └── templates/
│       ├── index.html       # メイン画面（サイドバーレイアウト）
│       ├── lots.html        # ロット一覧パーシャル（HTMX用）
│       ├── users.html       # ユーザ一覧パーシャル（HTMX用）
│       ├── component/
│       │   ├── lot_dialog.html
│       │   └── user_dialog.html
│       └── static/
│           ├── css/style.css
│           └── js/
│               ├── app.js   # Alpine.jsコンポーネント定義
│               └── theme.js # ダークモード切替
├── config/
│   ├── requirements.md
│   └── implement.md
├── .env                     # 環境変数（APP_HOST, APP_PORT）
├── requirements.txt
└── CLAUDE.md
```

## セットアップ

```bash
# 仮想環境を作成・有効化
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt
```

## 起動

```bash
uvicorn src.main:app --reload
```

ブラウザで `http://localhost:8000` を開きます。

環境変数でホスト・ポートを変更できます:

```
APP_HOST=0.0.0.0
APP_PORT=8000
```

## API エンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/lots` | ロット一覧（HTMX: パーシャルHTML、直接: `/` へリダイレクト） |
| POST | `/lots` | ロット新規登録 |
| GET | `/lots/{lot_id}` | ロット取得 |
| PATCH | `/lots/{lot_id}` | ロット更新 |
| GET | `/users` | ユーザ一覧（HTMX: パーシャルHTML、直接: `/` へリダイレクト） |
| POST | `/users` | ユーザ新規登録 |
| GET | `/users/{username}` | ユーザ取得 |
| PATCH | `/users/{username}` | ユーザ更新 |
