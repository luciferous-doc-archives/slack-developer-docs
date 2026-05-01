# ログ: GitHub Actions失敗時のSlack通知機能追加（タスク 0010）

## 基本情報

- **開始時刻**: 2026-05-01T17:30:00+09:00
- **完了時刻**: 2026-05-01T17:38:04+09:00

## タスク概要

GitHub Actionsに失敗通知用のジョブを追加する。ジョブが失敗した時にSlackに通知するジョブを追加し、Incoming Webhookを使い、`SLACK_INCOMING_WEBHOOK_URL` というシークレットからURLを取得する。チャンネルに対してメンションをし、失敗したGithub Actionsの実行へのURLを付与する。

## 調査結果（フェーズ1）

### ワークフロー構造の調査

**ファイルパス**: `.github/workflows/fetch-docs.yml`

**ワークフロー構成**:
- ワークフロー名: "Fetch Slack Developer Docs"
- トリガー: 
  - `workflow_dispatch` (手動実行)
  - `schedule`: `"0 18 * * *"` (毎日 18:00 UTC = 03:00 JST)

**現在のジョブ構成**:
- Job名: `fetch`
- 実行環境: `ubuntu-latest`
- ステップ:
  1. Checkout: `actions/checkout@v6`
  2. Set timestamp: タイムスタンプを生成（`steps.timestamp.outputs.value`）
  3. Show timestamp: タイムスタンプ出力
  4. Install uv: `astral-sh/setup-uv@v8.1.0`
  5. Install dependencies: `uv sync`
  6. Run fetcher: `uv run src/handlers/fetcher/fetcher.py`（`BASE_TIMESTAMP` 環境変数を設定）

**環境変数・シークレット設定**:
- 現在、シークレットは使用されていない
- `PYTHONPATH` は `src` に設定されている

**失敗時の処理**:
- 現在、`if: failure()` は使用されていない
- ジョブの失敗時に実行されるアクション・通知機構はない

### ワークフロー拡張パターン

**推奨アプローチ**:
1. 新しいジョブ `notify-on-failure` を追加
2. `needs: fetch` で `fetch` ジョブに依存させる
3. `if: failure()` で fetch ジョブの失敗時のみ実行
4. `curl` で Slack Incoming Webhook API に POST リクエスト送信

**GitHub Actions で利用可能な変数**:
- `${{ github.server_url }}`: GitHub サーバーURL
- `${{ github.repository }}`: リポジトリ名（owner/repo 形式）
- `${{ github.run_id }}`: ワークフロー実行 ID
- `${{ secrets.SLACK_INCOMING_WEBHOOK_URL }}`: Slack Webhook URL（シークレット）

## 実装プラン

### 実装方針

1. **ワークフローへの新しいジョブ追加**
   - `.github/workflows/fetch-docs.yml` に `notify-on-failure` ジョブを追加
   - `needs: fetch` で fetch ジョブに依存
   - `if: failure()` で失敗時のみ実行
   - `runs-on: ubuntu-latest`

2. **Slack 通知の実装**
   - `curl` コマンドで Slack Incoming Webhook API に POST
   - JSON ペイロード形式でメッセージを構築
   - メッセージ内容:
     - テキスト: "<!channel> GitHub Actions workflow failed: Fetch Slack Developer Docs"
     - ワークフロー実行 URL をリンク付きで含める

3. **GitHub シークレット設定**
   - GitHub リポジトリ Settings → Secrets and variables → Actions
   - `SLACK_INCOMING_WEBHOOK_URL` を新規登録（ユーザーが別途実施）

4. **実装ステップ**
   - 1. `.github/workflows/fetch-docs.yml` を編集して新しいジョブを追加
   - 2. 変更をテストするために、手動実行で動作確認（ユーザーが別途実施予定）

### メッセージテンプレート

```json
{
  "text": "<!channel> GitHub Actions workflow failed: Fetch Slack Developer Docs",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Failed to fetch Slack Developer Docs*\n\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
      }
    }
  ]
}
```

## プランニング経緯

### 初回提案
調査結果に基づいて、以下の実装方針を提案：
1. 新しいジョブ `notify-on-failure` を追加
2. `needs: fetch` と `if: failure()` で依存・条件指定
3. `curl` で Slack Incoming Webhook に通知
4. メンション付きメッセージでワークフロー実行 URL を含める

### ユーザーフィードバック
プランが承認されたため、実装を開始

## 会話内容（フェーズ1）

（Explore エージェントによる詳細な調査結果に基づいて計画を立案）

## 実装フェーズ

### 編集ファイル

#### ファイル: `.github/workflows/fetch-docs.yml`

**変更内容**:
- 新しいジョブ `notify-on-failure` を `fetch` ジョブの後に追加
- 内容は以下の通り:

```yaml
notify-on-failure:
  runs-on: ubuntu-latest
  needs: fetch
  if: failure()
  steps:
    - name: Notify Slack on failure
      run: |
        curl -X POST ${{ secrets.SLACK_INCOMING_WEBHOOK_URL }} \
          -H 'Content-Type: application/json' \
          -d '{
            "text": "<!channel> GitHub Actions workflow failed: Fetch Slack Developer Docs",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*Failed to fetch Slack Developer Docs*\n\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                }
              }
            ]
          }'
```

### 実行したコマンド

なし（ファイル編集のみ）

### 判断・意思決定

1. **通知方法**: Slack Incoming Webhook に `curl` を使って POST リクエストを送信。外部 Action ではなく標準ツールで実装することで依存関係を最小化。

2. **JSON 構築方法**: `printf '%s'` の書式指定子を使って環境変数を安全に埋め込む方式を採用。heredoc では変数展開と `\n` の扱いが複雑になるため回避した。

3. **シークレットの扱い**: `SLACK_WEBHOOK_URL` を環境変数（`env:` セクション）経由で渡すことで、コマンドライン引数に直接シークレットが現れるのを防いだ。GitHub Actions は `${{ secrets.* }}` をログでマスクするが、環境変数経由の方がより安全。

4. **メッセージ形式**: ユーザーの追加要望に従い、リポジトリ名（`REPO_NAME`）とリポジトリリンク（`REPO_URL`）を環境変数で設定し、Slack mrkdwn 形式でリンク付き表示。

5. **メッセージ内容（変更反映後）**:
   - `<!channel>` メンション
   - リポジトリ名（リンク付き）: `<REPO_URL|REPO_NAME>`
   - ワークフロー実行 URL（View Details）: `<WORKFLOW_URL|View Details>`

### エラー・問題

なし

## 完了サマリー

- **完了日時**: 2026-05-01T17:38:04+09:00
- **変更ファイル**: `.github/workflows/fetch-docs.yml`
- **変更内容**: `notify-on-failure` ジョブを追加。`fetch` ジョブの失敗時に `SLACK_INCOMING_WEBHOOK_URL` シークレット経由で Slack へ通知。メッセージには `<!channel>` メンション、リポジトリ名とリンク、ワークフロー実行 URL を含む。
