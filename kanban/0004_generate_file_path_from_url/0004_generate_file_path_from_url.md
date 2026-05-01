# URLからファイルパスを生成する

## 目的
URLからファイル保存用のパスが欲しい。単純にURLからパスを生成するのではなく一部修正して欲しい。

## 要望
ドキュメントのURLからファイル保存用のパスを生成する関数を書いて欲しい。
main.pyに定義して欲しい。

## 修正方針
### 原則

- URLのパスから一文字目の `/` を除外する

### 特殊

```text
- https://docs.slack.dev/admins.md
- https://docs.slack.dev/admins/admin-oversight-api.md
- https://docs.slack.dev/admins/audit-logs-api.md
```

上記のようにディレクトリと同名のファイル名のものがある。

このときは下記パスのようにして欲しい。

```text
- admins/index.md
- admins/admin-oversight-api.md
- admins/audit-logs-api.md
```

## プラン

`src/handlers/fetcher/main.py` に `url_to_file_path(url: str, all_urls: list[str]) -> str` 関数を追加する。

- 原則: `urlparse(url).path[1:]` で先頭の `/` を除外
- 特殊ケース: `.md` を除いた stem と同名のディレクトリが `all_urls` に存在する場合は `{stem}/index.md` を返す

## 完了サマリー

- 完了日時: 2026-05-01T15:12:06+09:00
- 実装内容: `src/handlers/fetcher/main.py` に `url_to_file_path` 関数を追加し、`from urllib.parse import urlparse` をインポート追加
- フォーマット: `make format` 実行済み（main.py への変更なし）