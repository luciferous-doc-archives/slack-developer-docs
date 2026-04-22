# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

[Slack Developer Docs](https://docs.slack.dev/)

上記ドキュメントをダウンロードし、GithubのReleaseにzipで固めて配布する。

ドキュメントは [llms-sitemap.md](https://docs.slack.dev/llms-sitemap.md) を参照して、ダウンロード対象のマークダウン一覧を取得し、各ページをダウンロードしzipで固める。

ダウンロードしてzipで固めるのはGithub Actionsで行い、 `workflow_dispatch` か `schedule` で実行する。

## Commands

```bash
# フォーマット (isort + black を main.py に適用)
make format

# スクリプト実行
uv run main.py

# 依存関係の追加
uv add <package>

# 開発用依存関係の追加
uv add --dev <package>
```

## Kanban ワークフロー

開発のタスク管理にカンバン方式を採用し、 `sinofseven/luciferous-plugins-for-claude-code` の `kanban-kit` を使用する。

Claude Codeに作業させるときは原則 `/kanban-kit:kanban` スキルを使用する。

ワークフローの詳細は該当スキルに含まれるreferenceを参照してください。

- `kanban/{xxxx}_{title}/{xxxx}_{title}.md` にタスクファイルを配置する
- `kanban/{xxxx}_{title}/log.md` にログファイルを生成する
- **タスク開始時は `/kanban-kit:kanban` スキルを使用すること**
- `/kanban-kit:kanban` はプランモードで計画を立て、承認後に実装に移る
- **タスク作業中は、各ステップ完了時に必ずログファイルを更新すること**
- kanbanファイルへの追記時・ログへの記録時は JST タイムゾーンのISO 8601形式で日時を記載する
- 備考
  - `{xxxx}`は0パディングした連番 (例: `0011`, `0101`)
  - `{title}`はタイトルの文字列

## Architecture

- Python 3.14+ が必要（`pyproject.toml` で指定済み）
- `main.py` が実装のエントリポイントで、`uv run main.py` を実行することでドキュメントをダウンロードし zip を生成する
- 処理フロー：
  1. `https://docs.slack.dev/llms-sitemap.md` を取得し、ダウンロード対象 URL の一覧を得る
  2. 各 URL のマークダウンファイルをダウンロードする
  3. `./dist/slack-developer-docs-YYYYmmdd-HHMM.zip` にまとめる
     - `YYYY`: 4桁の年
     - `mm`: 2桁0パディングの月
     - `dd`: 2桁0パディングの日
     - `HH`: 2桁24時間制で0パディングの時
     - `MM`: 2桁0パディングの分

- GitHub Actions ワークフローは `.github/workflows/` 配下に配置し、`workflow_dispatch` と `schedule` トリガーで動作させる
