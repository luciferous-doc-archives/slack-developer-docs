# 毎日03:00 JSTで起動するGithub Actionsワークフロー

## 目的
ドキュメントのフェッチを03:00に行いたいと思います。
また、今回のワークフローにはcheckoutとUTCでの実行日時 (年月日と時分までの文字列。例: `20260430-1211`)を後続のステップで使えるようにしてください。
一応手動実行もできるようにしてください。

## 要望
毎日03:00 JSTに起動するGithub Actionsを書いてください

## プラン

- `.github/workflows/fetch-docs.yml` を新規作成
- `schedule` cron: `0 18 * * *`（03:00 JST = 18:00 UTC）と `workflow_dispatch` を設定
- `actions/checkout@v4` で checkout
- `date -u +'%Y%m%d-%H%M'` で UTC タイムスタンプを生成し `$GITHUB_OUTPUT` 経由で後続ステップから参照可能に
- 現時点では後続処理未実装のため echo の placeholder ステップを配置

## 完了サマリー

- **完了日時**: 2026-04-30T12:54:32+09:00
- **作成ファイル**: `.github/workflows/fetch-docs.yml`
- **内容**: schedule（毎日 18:00 UTC = 03:00 JST）と workflow_dispatch で起動するワークフロー。checkout + タイムスタンプ生成（`steps.timestamp.outputs.value`）を含む。後続ステップの placeholder として echo を配置。
