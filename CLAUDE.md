# Claude Code設定

## ディレクトリ構成
- `src/` - アプリ本体
- `src/routers/` - REST API
- `src/services/` - ビジネスロジック
- `src/repositories/` - DBアクセス処理
- `src/templates/` - HTML/CSS/JS
- `designs/wireframes/` - モック
- `designs/screenshots/` - スクショ

## コーディング規約
- コメントを書く
- コードを機能単位のブロックで分割する
- RESTを遵守する
- `any`型の乱用禁止
- 生成するコードはsrc/に配置すること
- config/のファイルは読み取り専用

## 技術スタック
- FastAPI / uvicorn / Jinja2
- Pydantic / HTMX / Alpine.js
- SQLite / SQLAlchemy

## データベース
- 開発環境: dev.db / テスト環境: test.db
- .envで切り替えること

## 更新ポリシー
- 機能追加時はREADME.mdを更新すること
- AIが間違った動作をしたらここに反映すること