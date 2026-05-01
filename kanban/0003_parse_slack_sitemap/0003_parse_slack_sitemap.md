# Slack Developer Docs サイトマップのダウンロード・パース関数

## 目的
slack developer docsのドキュメント一覧を上記URLから取得する。マークダウンファイルなのでパースする関数を書いて欲しい。どうやってパースするかは実際に上記URLのマークダウンファイルを読み込んでから考えてください。

## 要望
`https://docs.slack.dev/llms-sitemap.md` をダウンロードしてURLの一覧をパースする関数を書いてください。

## プラン

- `src/utils/parser/sitemap_parser.py` に `interval_fetcher.py` のパターンで実装
- ファクトリ関数 `make_sitemap_parser()` と `default_parser` インスタンスを定義
- 正規表現でハイフン箇条書き形式からURL抽出・バリデーション
- `src/handlers/fetcher/main.py` の `main()` にフェッチ＋パース呼び出しを統合

## 完了サマリー

- **完了日時**: 2026-05-01T14:59:17+09:00
- **作成ファイル**:
  - `src/utils/parser/__init__.py`
  - `src/utils/parser/sitemap_parser.py`
- **編集ファイル**:
  - `src/handlers/fetcher/main.py`
- **確認結果**: `PYTHONPATH=src uv run src/handlers/fetcher/fetcher.py` で 2,938 件の URL を正常に取得・パース
