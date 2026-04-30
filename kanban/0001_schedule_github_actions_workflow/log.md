# log: 0001_schedule_github_actions_workflow

## ヘッダー

- **タスク番号**: 0001
- **タスク名**: 毎日03:00 JSTで起動するGitHub Actionsワークフロー
- **開始日時**: 2026-04-30T12:53:51+09:00
- **完了日時**: 2026-04-30T12:54:32+09:00

---

## タスク概要

毎日 03:00 JST に自動起動するGitHub Actionsワークフローを新規作成する。

**要望**: 毎日03:00 JSTに起動するGithub Actionsを書いてください。ワークフローには checkout と UTCでの実行日時（年月日と時分までの文字列。例: `20260430-1211`）を後続のステップで使えるようにし、一応手動実行もできるようにする。

---

## 調査結果

### リポジトリ構造（ls 結果）

```
.claude/
.git/
.python-version
.venv/
CLAUDE.md
kanban/
  0001_schedule_github_actions_workflow/
main.py
Makefile
pyproject.toml
README.md
uv.lock
```

- `.github/` ディレクトリ: **存在しない（新規作成が必要）**

### main.py

7行のスタブのみ:

```python
def main():
    print("Hello from slack-developer-docs!")

if __name__ == "__main__":
    main()
```

### pyproject.toml

- Python: `>=3.14`
- runtime 依存: なし
- dev 依存: `black>=26.3.1`, `isort>=8.0.1`
- ビルドシステム: `hatchling`
- パッケージマネージャ: `uv`（uv.lock, .venv が存在）

### Makefile

```makefile
SHELL = /usr/bin/env bash -xeuo pipefail
.PHONY: format
format:
    uv run isort main.py
    uv run black main.py
```

### CLAUDE.md から確認した Architecture

- `workflow_dispatch` と `schedule` トリガーを使う
- `.github/workflows/` 配下に配置する
- zip ファイル名形式: `./dist/slack-developer-docs-YYYYmmdd-HHMM.zip`
  - 今回実装するタイムスタンプ形式 (`20260430-1211`) と一致している

---

## 実装プラン

### 新規作成するファイル

`.github/workflows/fetch-docs.yml`

### 設計上の判断

| 項目 | 決定内容 |
|------|---------|
| cron 表記 | `0 18 * * *`（03:00 JST = 18:00 UTC 前日扱い） |
| 手動起動 | `workflow_dispatch:` を入力なしで宣言 |
| checkout | `actions/checkout@v4`（現時点の最新メジャー） |
| タイムスタンプ | `date -u +'%Y%m%d-%H%M'` で UTC の `YYYYmmdd-HHMM` を生成、`$GITHUB_OUTPUT` 経由で後続から `${{ steps.timestamp.outputs.value }}` で参照可能 |
| placeholder | 現時点では後続処理未実装なので echo ステップを置く（次タスクで置き換え前提） |

### ワークフロー構成（承認済みプランと同一）

```yaml
name: Fetch Slack Developer Docs

on:
  workflow_dispatch:
  schedule:
    - cron: "0 18 * * *"  # 03:00 JST = 18:00 UTC

jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set timestamp
        id: timestamp
        run: echo "value=$(date -u +'%Y%m%d-%H%M')" >> "$GITHUB_OUTPUT"

      - name: Show timestamp (placeholder)
        run: echo "Run timestamp (UTC) = ${{ steps.timestamp.outputs.value }}"
```

---

## プランニング経緯

- 初回提案がそのまま承認された（リジェクトなし）
- プランモードで特に代替案の検討は不要なシンプルなタスクであった

---

## 会話内容

1. ユーザーが `/add-kanban` でタスク 0001 を作成し、`/kanban 0001` を実行
2. Explore エージェントでリポジトリ構造を調査（`.github/` 未存在を確認）
3. プランを立案し ExitPlanMode でユーザーに提示
4. ユーザーがプランを承認 → 実装フェーズへ移行

---

## 編集したファイル

| ファイル | 操作 | 内容 |
|---------|------|------|
| `.github/workflows/fetch-docs.yml` | 新規作成 | スケジュール・手動起動対応ワークフロー |
| `kanban/0001_schedule_github_actions_workflow/0001_schedule_github_actions_workflow.md` | 更新 | プランセクション・完了サマリー追記 |

---

## 実行したコマンド

```bash
TZ=Asia/Tokyo date +"%Y-%m-%dT%H:%M:%S+09:00"
# → 2026-04-30T12:53:51+09:00
```

---

## 判断・意思決定

- ワークフローファイル名: `fetch-docs.yml`（ドキュメント取得という目的を端的に表す）
- placeholder ステップを残す: `main.py` がまだスタブのため、次タスクで本実装に置き換える前提

---

## エラー・問題

特になし
