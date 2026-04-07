# /deploy

テストを実行しパスした場合のみGitHubにpushする。

## 手順

1. テストを実行する
pytest tests/ -v

2. テストが通った場合のみ以下を実行する
git add .

3. コミットメッセージを確認してコミットする
git commit -m "メッセージ"

4. GitHubにpushする
git push

## 確認事項

- テストが全て通っていること
- コミットメッセージがConventional Commitsに沿っていること
.claude/commands/start.md
markdown# /start

開発サーバを起動する。

## 手順

1. 依存ライブラリをインストールする
pip install -r requirements.txt

2. 開発サーバを起動する
python -m uvicorn src.main:app --reload

## 確認事項

- .envファイルが存在しDATABASE_URLが設定されていること
- .venvが有効化されていること
- ポート8000が空いていること
.claude/commands/review.md
markdown# /review

コードの品質をレビューする。

## 観点

1. CLAUDE.mdのコーディング規約に沿っているか
2. RESTを遵守しているか
3. テストが書かれているか
4. 不要なコメントがないか
5. .envや機密情報がコードに含まれていないか

## 結果

- 問題がある場合は修正箇所を具体的に指摘する
- 問題がない場合は「レビュー完了」と報告する

Claude Codeに
.claude/commands/を上記の内容で修正して
と指示すれば一括で更新してくれます。