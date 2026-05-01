# url_to_file_path() を utils 配下に切り出す - 作業ログ

**開始日時**: 2026-05-02T00:00:00+09:00

## タスク概要

`src/handlers/fetcher/main.py` に実装されている `url_to_file_path()` 関数を `src/utils/path/` に切り出し、再利用可能にする。テストもutils配下に移動する。

## 調査結果

### 対象関数の詳細

**ファイルパス**: `src/handlers/fetcher/main.py` (31-40行目)

**関数シグネチャ**:
```python
@logging_function(logger)
def url_to_file_path(*, url: str, all_urls: list[str]) -> str:
```

**実装内容**（詳細）:
```python
@logging_function(logger)
def url_to_file_path(*, url: str, all_urls: list[str]) -> str:
    path = urlparse(url).path[1:]

    if path.endswith(".md"):
        stem = path[:-3]
        prefix = f"/{stem}/"
        if any(urlparse(u).path.startswith(prefix) for u in all_urls):
            return f"{stem}/index.md"

    return path
```

**依存関係**: `urllib.parse.urlparse` のみ

**デコレータ**: `@logging_function(logger)` で装飾されている

### 使用箇所確認

1. **src/handlers/fetcher/main.py** (21行目): `main()` 関数内で `fetch_and_save()` にパス計算用に使用
2. **tests/unit/handlers/fetcher/test_main.py**: インポートして10個のテストケースで検証

### utils配下の構造確認

```
src/utils/
├── __init__.py (空)
├── logger/     (ロギング機能)
├── parser/     (マークダウンパース)
└── http/       (HTTP通信)
```

### インポート・使用パターン

既存のutils モジュール（logger, parser, http）の構造に揃える：
- `from utils.logger import create_logger, logging_function`
- `from utils.parser import parse_sitemap_markdown`
- `from utils.http.interval_fetcher import default_fetcher`

## 実装プラン

### ステップ 1: utils/path モジュール作成

実装内容：
- `src/utils/path/converter.py` を作成：関数実装とロギングデコレータを移動
- `src/utils/path/__init__.py` を作成：public API定義

### ステップ 2: テストをutils配下に移動

実装内容：
- `tests/unit/utils/path/test_converter.py` を新規作成：既存テストを移動
- インポートを `from utils.path import url_to_file_path` に変更
- 既存テストファイル削除

### ステップ 3: main.py を更新

実装内容：
- `url_to_file_path()` 関数定義を削除
- `from utils.path import url_to_file_path` でインポート追加

### ステップ 4: テスト実行と検証

実行予定：
```bash
make test-unit
```

## プランニング経緯

- **初回提案**: テストファイルは handlers 配下に残す
- **ユーザーフィードバック**: テストファイルについてもutils配下としてのファイルごと変えてください
- **最終プラン**: テストをutils配下に完全に移動

## 実装フェーズ

### 実装内容の詳細

#### ファイル作成: src/utils/path/converter.py

#### ファイル作成: src/utils/path/__init__.py

#### ファイル作成: tests/unit/utils/path/test_converter.py

#### ファイル修正: src/handlers/fetcher/main.py

#### ファイル削除: tests/unit/handlers/fetcher/test_main.py

### ステップ 1: utils/path モジュール作成

完了日時：2026-05-02T00:15:00+09:00

実装内容：
- `src/utils/path/converter.py` を作成
  - `urllib.parse.urlparse` をインポート
  - `utils.logger` から `create_logger`, `logging_function` をインポート
  - `url_to_file_path()` 関数を実装（既存の実装をそのまま移動）
  - `@logging_function(logger)` デコレータで装飾

- `src/utils/path/__init__.py` を作成
  - `url_to_file_path` を公開API として定義
  - `__all__` で公開インターフェース明示

### ステップ 2: テストをutils配下に移動

完了日時：2026-05-02T00:20:00+09:00

実装内容：
- `tests/unit/utils/path/test_converter.py` を新規作成
  - インポート変更：`from utils.path import url_to_file_path`
  - 既存の10個のテストケースをそのまま移動
  - テスト内容の変更なし

### ステップ 3: main.py を更新

完了日時：2026-05-02T00:25:00+09:00

実装内容：
- インポート追加：`from utils.path import url_to_file_path`
- インポート削除：`from urllib.parse import urlparse` （使用場所がなくなったため）
- 関数定義削除：`url_to_file_path()` 関数を削除

修正内容（詳細）：
- 1行目-7行目：インポート修正
  - `from urllib.parse import urlparse` を削除
  - `from utils.path import url_to_file_path` を追加

- 31-40行目：関数定義削除
  - `url_to_file_path()` 関数定義全体を削除

### ステップ 4: テスト実行と検証

完了日時：2026-05-02T00:30:00+09:00

テスト実行結果（古いテストと新しいテストの両方が存在する状態）：
```
============================== 20 passed in 0.17s ==============================
```
- 古いテストファイル（handlers/fetcher 配下）: 10 個 PASSED
- 新しいテストファイル（utils/path 配下）: 10 個 PASSED

古いテストファイル削除後のテスト実行結果：
```
tests/unit/utils/path/test_converter.py: 10 個 PASSED
============================== 10 passed in 0.10s ==============================
```

### ファイル削除

完了日時：2026-05-02T00:32:00+09:00

削除ファイル：
- `tests/unit/handlers/fetcher/test_main.py`（古いテストファイル）

理由：テスト機能が utils 配下の新しいテストファイルに完全に移動したため。

## 完了日時：2026-05-02T00:35:00+09:00
