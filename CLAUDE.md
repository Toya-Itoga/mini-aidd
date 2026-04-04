# CLAUDE.md — このリポジトリ向け Claude Code 設定

## ディレクトリ構成 / フォルダの意図
- `/src/main.py` - アプリ本体Python
- `.venv` - Pythonライブラリ
- `/src/routers` — REST API
- `/src/services` —  ビジネスロジック
- `/src/repositories` - DBアクセス処理
- `/src/templates/` - HTMLファイル
- `/src/templates/static/css` - CSSファイル
- `/src/templates/static/js` - JavaScriptファイル
- `designs/wireframes/` - Claude Codeが生成したモック
- `designs/screenshots/` - Playwrightが自動生成したスクショ

## コーディング規約 / スタイルガイド
- コメントを書く
- コードを機能単位のブロックで分割する
- RESTを遵守する

## 技術スタック / ライブラリ
- FastAPI - サーバサイドレンダリングで画面描画
- uvicorn
- Jinja2
- Pydantic - 型アノテーションでバリデーション
- HTMX / Alpine
- SQLite
- SQLAlchemy

## データベース
- 環境ごとにDBを分ける
- 開発環境: dev.db
- テスト環境: test.db
- .envで切り替えられるようにすること

## 禁止事項 / 注意点
- `any` 型の乱用禁止
- 大きなファイルのインライン化は避ける
- 生成されたコードには必ずレビューを入れる
- config/のファイルは読み取り専用とし編集しないこと
- .envファイルの参照
- 生成するコードはsrc/に配置すること

## 更新ポリシー
- `CLAUDE.md` はリポジトリと同じように変更・バージョン管理
- AI が間違った動作をしたらここに反映し、次回以降に活かす
- 機能追加・変更の際は必ずREADME.mdを更新すること
- README.mdには機能一覧・起動方法・ディレクトリ構成を記載すること