# ワークフローにハッシュ更新ステップを追加

## 目的
file_hashes.txt を更新したい。

## 要望
fetch-docs.yml の fetch ジョブにおいて、リリースを作成する直前に file_hashes.txt を更新してコミット&プッシュしてください。

最新のハッシュリストは current_file_hashes.txt です。current_file_hashes.txt で file_hashes.txt を上書きし、コミット&プッシュしてください。

※ このファイル内でファイル名などタイポしているかもしれないので、間違えていたら正しいものを使ってください。

## プラン

リリース作成直前に file_hashes.txt を更新するステップを追加する。

**追加ステップ「Update file hashes」:**
- 位置: 「Create release zip」と「Create GitHub Release」の間
- 条件: `steps.compare.outputs.files_changed == 'true'`
- 処理:
  1. git config で user.email/user.name を設定
  2. `cp current_file_hashes.txt file_hashes.txt` で上書き
  3. git add/commit/push でリポジトリに反映
  4. コミットメッセージ: "Update file hashes for docs updated on ${{ steps.timestamp.outputs.value }}"

## 完了サマリー

**完了日時**: 2026-05-01T20:41:50+09:00

**実装内容**:
- `.github/workflows/fetch-docs.yml` に「Update file hashes」ステップを追加（63-71 行目）
- ステップの位置、条件、処理内容はプランに従って実装

**動作仕様**:
- ファイルハッシュの変更検出時のみ実行（`files_changed == 'true'`）
- 新しいハッシュ値を基準値として保存
- コミット&プッシュでリポジトリに反映
- リリース作成前に完了するため、リリース時点でハッシュが更新された状態になる

**テスト方法**:
1. ワークフローが正常に実行されることを確認
2. ドキュメント変更時にハッシュ更新コミットが作成されることを確認
3. GitHub Release が正常に作成されることを確認
