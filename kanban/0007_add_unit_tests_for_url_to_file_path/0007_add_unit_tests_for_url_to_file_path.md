# url_to_file_path() の単体テストを追加

## 目的
今回のリポジトリではここの処理が重要なのでテストを書きたい。

## 要望
url_to_file_path()について単体テストを書いてください

## 完了サマリー

**完了日時**: 2026-05-01T23:15:00+09:00

### 成果物

- **テストファイル作成**: `tests/unit/handlers/fetcher/test_main.py`
  - 10個のテストケースを実装
  - パラメータ化テスト (`@pytest.mark.parametrize`) で複数シナリオをカバー

### テストケース一覧

1. `test_url_to_file_path[single_file_no_prefix]` - 単一ファイル（プレフィックスなし）
2. `test_url_to_file_path[single_file_guide]` - ガイドの単一ファイル
3. `test_url_to_file_path[directory_api_v1]` - API v1 のディレクトリ化
4. `test_url_to_file_path[directory_guide_python]` - Python ガイドのディレクトリ化
5. `test_url_to_file_path[root_level_md]` - ルート直下の Markdown ファイル
6. `test_url_to_file_path[partial_match_no_prefix]` - プレフィックス部分一致なし
7. `test_url_to_file_path[deep_path_hierarchy]` - 深いパス階層
8. `test_url_to_file_path[multiple_md_files_mixed]` - 複数の `.md` ファイル混在
9. `test_url_to_file_path[different_prefixes]` - 異なるプレフィックス
10. `test_url_to_file_path[multiple_files_same_stem]` - 同じステムを持つ複数ファイル

### テスト実行結果

```
============================== 10 passed in 0.18s ==============================
```

**全テスト成功** ✓

### 検証内容

- ✓ 単一のMarkdownファイルの処理
- ✓ 複数URLが存在する場合のディレクトリ化判定
- ✓ プレフィックスマッチングロジック
- ✓ 複雑なパス階層での処理
- ✓ 複数の `.md` ファイルが混在する場合の処理
