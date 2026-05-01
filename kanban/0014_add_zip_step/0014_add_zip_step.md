# docs ディレクトリを zip 圧縮するステップを追加

## 目的
ハッシュ比較後に変更があるとわかったときに、ダウンロードしたドキュメントを zip ファイルとして出力したい

## 要望
fetch-doc.yml の fetch ジョブに `docs` ディレクトリで `slack-developer-docs-{base_timestamp}` ディレクトリを `dist/slack-developer-docs-{base_timestamp}.zip` というzipファイルに固めるステップを追加してください。

## プラン
`.github/workflows/fetch-docs.yml` の `Compare hashes` ステップ（行 39-48）の直後に、`Create release zip` ステップを追加。

**追加ステップ**:
- ステップ名: `Create release zip`
- 条件: `if: steps.compare.outputs.files_changed == 'true'`
- 処理:
  ```yaml
  mkdir -p dist
  cd docs
  zip -r -9 ../dist/slack-developer-docs-${{ steps.timestamp.outputs.value }}.zip slack-developer-docs-${{ steps.timestamp.outputs.value }}/
  ```

**実装理由**:
- `zip -r -9`: 再帰的に最高圧縮で zip 作成
- `cd docs`: 作業ディレクトリ移動で zip 内パス構造を制御
- 条件付き実行: ハッシュ比較で変更あり時のみ実行

## 完了サマリー

**完了日時**: 2026-05-01T22:40:00+09:00

**実施内容**:
- `.github/workflows/fetch-docs.yml` に `Create release zip` ステップを追加（行 50-55）
- ハッシュ比較で変更検出時のみ zip 作成する条件付き実行を実装
- `-9` フラグで最高圧縮レベルに設定

**出力**: `dist/slack-developer-docs-{YYYYmmdd-HHMM}.zip`

**検証**: YAML 構文確認済み、ワークフロー構造に問題なし

**参考資料**: `kanban/0014_add_zip_step/log.md`
