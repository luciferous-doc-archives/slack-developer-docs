# ダウンロードファイルのハッシュリスト生成

## 目的
後続の処理に進むかどうかの判定に使う。 `find . -type f | sort | xargs sha256sum`で算出する。ワーキングディレクトリは `docs/slack-developer-docs-{base_timestamp}`とする。ハッシュリストのテキストファイルはリポジトリルートに出力する。

## 要望
`Run fetcher`のあと、ダウンロードしたファイルのハッシュリストのテキストファイルを作成するステップを追加してください

## プラン

GitHub Actions ワークフロー `.github/workflows/fetch-docs.yml` に以下 2 つのステップを追加：

1. **Generate file hashes**: `docs/slack-developer-docs-{base_timestamp}` ディレクトリで全ファイルのハッシュを生成
   - コマンド: `find . -type f | sort | xargs sha256sum > ../../current_file_hashes.txt`
   - 出力: `current_file_hashes.txt` (リポジトリルート)

2. **Upload hashes artifact**: ハッシュリストをアーティファクトとしてアップロード
   - アーティファクト名: `file-hashes`
   - 対象ファイル: `current_file_hashes.txt`

## 完了サマリー
完了日時: 2026-05-01T18:28:00+09:00

実装内容:
- `.github/workflows/fetch-docs.yml` に `Generate file hashes` と `Upload hashes artifact` の 2 つのステップを追加
- `working-directory` で処理対象ディレクトリを指定
- ハッシュリストを `current_file_hashes.txt` として出力
- アーティファクトとしてアップロード
