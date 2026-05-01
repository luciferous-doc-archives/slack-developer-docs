# url_to_file_path() を utils 配下に切り出す

## 目的
他で使うことも想定できるのでutils配下に切り出して再利用可能にしたい

## 要望
url_to_file_path()をutils配下に切り出してください

## 完了サマリー

**完了日時**: 2026-05-02T00:35:00+09:00

### 成果物

**新規作成モジュール**: `src/utils/path/`
- `src/utils/path/__init__.py` - 公開API定義
- `src/utils/path/converter.py` - `url_to_file_path()` 実装

**テスト移動**: `tests/unit/utils/path/test_converter.py`
- 既存の10個のテストケースを utils ディレクトリ構造に移動
- インポート変更：`from utils.path import url_to_file_path`

**既存コード修正**: `src/handlers/fetcher/main.py`
- `url_to_file_path()` インポート追加
- 関数定義削除
- 不要なインポート（`urllib.parse.urlparse`）削除

**古いテスト削除**: `tests/unit/handlers/fetcher/test_main.py`
- utils配下への移動に伴い削除

### 実装の詳細

#### モジュール構造
```
src/utils/
├── path/              ← 新規作成
│   ├── __init__.py
│   └── converter.py   # url_to_file_path() 実装
├── logger/
├── parser/
└── http/
```

#### 関数の再利用性

`url_to_file_path()` が utils 配下に公開されたことで、以下のように他のモジュールから利用可能になりました：

```python
from utils.path import url_to_file_path

# URL をファイルパスに変換
file_path = url_to_file_path(url="/api.md", all_urls=[...])
```

### テスト実行結果

```
============================== 10 passed in 0.10s ==============================
```

✓ 全テスト成功
✓ テストが utils 配下の正しい場所に移動
✓ インポート変更が正常に機能
✓ 既存の main.py が正常に動作

### 検証内容

- ✓ `url_to_file_path()` がutils配下に正しく移動
- ✓ テストもutils配下に移動し、すべてのテストケースが成功
- ✓ `main.py` のインポート変更で関数を正常に利用
- ✓ 古いテストファイルの削除確認
- ✓ 再利用可能な モジュール構造の実現
