# GitHub Actions失敗時のSlack通知機能追加

## 目的
Github Actionsにジョブが失敗した時にSlackに通知するジョブを追加して欲しい。Incoming Webhookを使い、 `SLACK_INCOMING_WEBHOOK_URL` というシークレットからURLを取得してください。チャンネルに対してメンションをしてください。失敗の内容は必要ありませんが、失敗したGithub Actionsの実行へのURLを付与してください。

## 要望
Github Actionsに失敗通知用のジョブを追加して欲しい

## 完了サマリー

- **完了日時**: 2026-05-01T17:38:04+09:00
- **変更ファイル**: `.github/workflows/fetch-docs.yml`
- `.github/workflows/fetch-docs.yml` に `notify-on-failure` ジョブを追加
  - `needs: fetch` + `if: failure()` で `fetch` ジョブ失敗時のみ実行
  - `SLACK_INCOMING_WEBHOOK_URL` シークレットから Webhook URL を取得
  - `curl` で Slack Incoming Webhook API に POST
  - メッセージに `<!channel>` メンション、リポジトリ名（リンク付き）、ワークフロー実行 URL を含む
