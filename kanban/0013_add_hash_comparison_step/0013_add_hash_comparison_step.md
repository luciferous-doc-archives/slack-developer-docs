# ハッシュ値比較ステップの追加

## 目的
二つのファイルに違いがあれば後続の処理を行い、同じであれば終了するようにしたい。そのために比較しつつ、違いがあるかどうかを後続に使えるようにしたい。

## 要望
fetch-docs.ymlのfetchジョブにcurrent_file_hashes.txtとfile_hashes.txtのハッシュを比較するステップを追加してください。

## 備考
`Upload hashes artifact` というステップを削除してください。

## 完了サマリー

**完了日時**: 2026-05-01T15:10:00+09:00

### 実施内容
- `.github/workflows/fetch-docs.yml` に `Compare hashes` ステップを追加
- `diff -q` で `file_hashes.txt` と `current_file_hashes.txt` を比較
- 出力値 `files_changed`（true/false）を定義
- `Upload hashes artifact` ステップを削除

### 実装の詳細
**追加したステップ** (`Compare hashes`):
```yaml
- name: Compare hashes
  id: compare
  run: |
    if diff -q file_hashes.txt current_file_hashes.txt >/dev/null 2>&1; then
      echo "files_changed=false" >> "$GITHUB_OUTPUT"
      echo "Files are identical. No update needed."
    else
      echo "files_changed=true" >> "$GITHUB_OUTPUT"
      echo "Files have changed. Proceeding with update."
    fi
```

### 後続での利用方法
後続ステップで条件付き実行を実装可能：
```yaml
if: steps.compare.outputs.files_changed == 'true'
```

### テスト・検証方法
1. ワークフロー手動実行（workflow_dispatch）で動作確認
2. ログで `Compare hashes` ステップの出力（files_changed の値）を確認
3. ハッシュ値に変更がない場合と変更がある場合で動作確認

### 成果
- ✅ ハッシュ値比較機能を実装
- ✅ タスク要望の全項目を完了
- ✅ 後続ステップでの条件付き実行が可能に
