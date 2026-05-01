# ログ: URLからファイルパスを生成する

## ヘッダー

- 開始時刻: 2026-05-01T15:11:22+09:00
- 完了時刻: 2026-05-01T15:12:06+09:00

## タスク概要

ドキュメントのURLからファイル保存用のパスを生成する関数を書いて欲しい。
main.pyに定義して欲しい。

修正方針:
- 原則: URLのパスから一文字目の `/` を除外する
- 特殊: ディレクトリと同名のファイル名のもの（例: `admins.md` と `admins/`）は `{stem}/index.md` に変換する

## 調査結果

### `src/handlers/fetcher/main.py`

現在の内容（22行）:
- インポート: `os.environ`, `utils.http.interval_fetcher.default_fetcher`, `utils.logger.*`, `utils.parser.default_parser`
- 定数: `SITEMAP_URL = "https://docs.slack.dev/llms-sitemap.md"`
- 関数 `main()`: SITEMAP_URL をフェッチ → パース → URL一覧を返す
- 関数 `get_base_timestamp()`: 環境変数 `BASE_TIMESTAMP` から値を取得

ファイル保存パスを生成する関数は現時点では存在しない。

### `src/utils/http/interval_fetcher.py`

- `make_interval_fetcher(sec: float)` で間隔制御付きフェッチャーを生成
- `default_fetcher` は 1秒間隔のインスタンス

### `src/handlers/fetcher/fetcher.py`

- エントリポイント。`main()` を呼び出すだけ

## 実装プラン

### 関数シグネチャ

```python
def url_to_file_path(url: str, all_urls: list[str]) -> str:
```

- `url`: 変換対象の URL
- `all_urls`: 全 URL のリスト（特殊ケース判定用）
- 戻り値: ローカル保存用パス文字列

### 実装コード

```python
from urllib.parse import urlparse

def url_to_file_path(url: str, all_urls: list[str]) -> str:
    path = urlparse(url).path[1:]  # 先頭の "/" を除外

    if path.endswith(".md"):
        stem = path[:-3]  # ".md" を除いた部分
        prefix = f"/{stem}/"
        if any(urlparse(u).path.startswith(prefix) for u in all_urls):
            return f"{stem}/index.md"

    return path
```

### 変換例

| URL | 期待するパス |
|-----|------------|
| `https://docs.slack.dev/admins.md` | `admins/index.md` |
| `https://docs.slack.dev/admins/admin-oversight-api.md` | `admins/admin-oversight-api.md` |
| `https://docs.slack.dev/messaging.md`（サブページなし） | `messaging.md` |

ネストが深いケース（例: `admins/sub.md` と `admins/sub/page.md`）も同じロジックで正しく処理できる。

## プランニング経緯

初回提案がそのまま承認された。ただし「サブディレクトリのサブディレクトリでも問題ないか？」の確認に対し、`stem` がパス全体を含むため正しく動作すると説明し、了承された。

## 会話内容

1. ユーザーが `/kanban-kit:kanban 0004` でタスク開始
2. Claude がコードベース調査（main.py, interval_fetcher.py, fetcher.py を確認）
3. Claude がプランを提示: `url_to_file_path(url, all_urls)` 関数を main.py に追加
4. ユーザーから「サブディレクトリのサブディレクトリでも問題ないか？」の確認
5. Claude が `stem` がパス全体を含む（例: `admins/sub`）ため、ネスト深さに関係なく正しく動作すると説明
6. ユーザーがプランを承認

## 編集したファイル

- [x] `src/handlers/fetcher/main.py` — `url_to_file_path` 関数を追加、`urllib.parse.urlparse` をインポート

## 実行したコマンド

- `make format` — isort + black でフォーマット確認（main.py への変更なし）

## 判断・意思決定

（記録なし）

## エラー・問題

（記録なし）
