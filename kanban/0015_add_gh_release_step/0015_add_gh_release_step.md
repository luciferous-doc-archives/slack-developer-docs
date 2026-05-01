# GitHub Releaseステップの追加

## 目的
ドキュメントに更新があれば固めたドキュメントを配布できるように、リリースを作成したい

## 要望
fetch-doc.ymlのfetchジョブに `softprops/action-gh-release` を使ってリリースを作成するステップを追加してください

## プラン

1. `fetch` ジョブに `permissions: contents: write` を追加
2. `Set timestamp` の直後に `Set date` ステップを追加（UTC 日付 `YYYY/mm/dd` 形式）
3. `Create release zip` の直後に `Create GitHub Release` ステップを追加
   - `softprops/action-gh-release@v2` を使用
   - tag_name: タイムスタンプベース（重複防止）
   - name: 日付ベース（`YYYY/mm/dd document updated`）
   - body: 日付＋タイムスタンプを含むメッセージ
   - draft: false
   - files: dist/*.zip

## 完了サマリー

- **完了日時**: 2026-05-01T20:32:44+09:00
- **変更ファイル**: `.github/workflows/fetch-docs.yml`
- **実施内容**:
  - `fetch` ジョブに `permissions: contents: write` を追加
  - `Set timestamp` の次に `Set date` ステップを追加（UTC 日付 `YYYY/mm/dd` 形式）
  - `Create release zip` の次に `Create GitHub Release` ステップを追加
    - `softprops/action-gh-release@v2` を使用
    - ファイル変更時のみ実行（`if: steps.compare.outputs.files_changed == 'true'`）

## 詳細
- 日付をリリースの文面などに使うので、`Set timestamp`ステップの次に `Set date`ステップを作成しUTCでの日付を後続の処理で使える様にしてください (形式: `YYYY/mm/dd`)
- bodyには日付をつけてドキュメントが更新されたことを示す文面を作ってください
- draftはtrueにしてください
- nameは日付を使って `YYYY/mm/dd document updated` みたいな感じにしてください
- filesは `dist/*.zip`にしてください
