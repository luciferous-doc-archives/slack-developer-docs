# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

[Slack Developer Docs](https://docs.slack.dev/) のマークダウンを定期取得し、GitHub Release に zip で配布するツール。

`https://docs.slack.dev/llms-sitemap.md` を参照してダウンロード対象 URL の一覧を取得し、各ページをダウンロードして zip に固める。GitHub Actions の `workflow_dispatch` か `schedule` で実行する。

## Commands

```bash
# フォーマット（isort + black を src/ に適用）
make format

# スクリプト実行
uv run src/handlers/fetcher/fetcher.py

# 依存関係の追加
uv add <package>

# 開発用依存関係の追加
uv add --dev <package>
```

## Kanban ワークフロー

開発のタスク管理にカンバン方式を採用し、`sinofseven/luciferous-plugins-for-claude-code` の `kanban-kit` を使用する。

Claude Code に作業させるときは原則 `/kanban-kit:kanban` スキルを使用する。

- `kanban/{xxxx}_{title}/{xxxx}_{title}.md` にタスクファイルを配置する
- `kanban/{xxxx}_{title}/log.md` にログファイルを生成する
- **タスク開始時は `/kanban-kit:kanban` スキルを使用すること**
- `/kanban-kit:kanban` はプランモードで計画を立て、承認後に実装に移る
- **タスク作業中は、各ステップ完了時に必ずログファイルを更新すること**
- kanban ファイルへの追記時・ログへの記録時は JST タイムゾーンの ISO 8601 形式で日時を記載する
- 備考
  - `{xxxx}` は 0 パディングした連番（例: `0011`, `0101`）
  - `{title}` はタイトルの文字列

## Architecture

- Python 3.14+ が必要（`pyproject.toml` で指定済み）
- エントリポイントは `src/handlers/fetcher/fetcher.py`（`fetcher.main()` を呼び出す）
- 処理フロー:
  1. `https://docs.slack.dev/llms-sitemap.md` を取得し、ダウンロード対象 URL の一覧を得る
  2. 各 URL のマークダウンファイルをダウンロードする
  3. `./dist/slack-developer-docs-YYYYmmdd-HHMM.zip` にまとめる
     - `YYYY`: 4 桁の年
     - `mm`: 2 桁 0 パディングの月
     - `dd`: 2 桁 0 パディングの日
     - `HH`: 2 桁 24 時間制で 0 パディングの時
     - `MM`: 2 桁 0 パディングの分

### パッケージ構造

```
src/
├── handlers/fetcher/
│   ├── fetcher.py    # エントリポイント（fetcher.main() を実行）
│   └── main.py       # 主実装ロジック
└── utils/
    ├── http/interval_fetcher.py   # HTTP フェッチャー（間隔制御付き）
    └── logger/                    # AWS Lambda Powertools ベースのロギング基盤
        ├── create_logger.py       # ロガーファクトリ
        ├── logging_function.py    # 関数実行ログデコレータ
        └── logging_handler.py     # Lambda ハンドラーログデコレータ
```

### 環境変数

| 変数名 | 説明 |
|---|---|
| `BASE_TIMESTAMP` | 出力 zip ファイル名に使用するタイムスタンプ（GitHub Actions で設定） |

### GitHub Actions

`.github/workflows/fetch-docs.yml` — 毎日 03:00 JST（18:00 UTC）と手動トリガーで実行。`steps.timestamp.outputs.value` に UTC タイムスタンプ（`YYYYmmdd-HHMM`）を出力する。
