# ファイル保存時のエンコーディングを明示 - 実行ログ

## ヘッダー

**開始日時**: 2026-05-01T15:57:24+09:00  
**タスク名**: ファイル保存時のエンコーディングを明示（0006_specify_file_encoding）  
**ステータス**: 進行中

---

## タスク概要

コードレビュー（タスク 0005）で発見された「**問題点(D): ファイルエンコーディングが明示されていない**」に対応するタスク。

対象ファイル:
- `src/utils/http/interval_fetcher.py` — HTTP レスポンス decode 時にエンコーディング未指定
- `src/handlers/fetcher/main.py` — ファイル書き込み時にエンコーディング未指定

---

## フェーズ1: プランニング結果

### 調査結果の要約

**プロジェクト内のファイル I/O 操作:**
- `main.py:51-52` で `open(file_path, "w")` でファイル書き込み（エンコーディング未指定）
- `interval_fetcher.py:35` で `body.decode()` で HTTP レスポンス decode（エンコーディング未指定）
- その他のファイル I/O 操作はない

**現状の問題:**
- システムデフォルトエンコーディングに依存（Windows: Shift-JIS、Unix: UTF-8）
- マルチプラットフォーム環境での予期しない文字化けリスク

**既存パターン:**
- プロジェクト内に encoding 指定パターンの統一がない
- テストファイルは存在しない

### プランニング結果（確定版）

**HTTP レスポンス decode:**
- `extract_charset_from_response(resp: HTTPResponse) -> str` 関数を追加
- Content-Type ヘッダーから charset を判定（RFC 2045 対応）
- charset 未指定時はデフォルト UTF-8
- 実装方法: 文字列分割による抽出（シンプルで堅牢）

**ファイル書き込み:**
- `open(file_path, "w", encoding="utf-8")` に変更（UTF-8 固定）
- Slack API ドキュメントが UTF-8 ベースであるため

### レビュー方針

ユーザーからのフィードバック:
- 「interval_fetcher.py についても対応してください」
- 「ここは utf-8 固定ではなく、きちんと HTTP のレスポンスから文字コードを判定してください」

対応: HTTP ヘッダーから charset を判定する仕様に変更（計画段階で確定）

---

## フェーズ2: 実装（進行中）

### 実装予定

1. `interval_fetcher.py` に `extract_charset_from_response()` 関数を追加
2. `interval_fetcher.py` の `body.decode()` を修正
3. `main.py` の `open()` に `encoding="utf-8"` を追加
4. `make format` でコード整形
5. ログファイルを最終化
6. kanban ファイルに完了サマリーを追記

### 実装内容（完了分）

#### 1. `interval_fetcher.py` に `extract_charset_from_response()` を追加

**変更内容:**
- 新規関数 `extract_charset_from_response(resp: HTTPResponse) -> str` を行 17-27 に追加
- Content-Type ヘッダーから charset パラメータを抽出
- charset 未指定時は UTF-8 をデフォルト値として返す
- RFC 2045 対応（ダブル・シングルクォート削除）

**実装コード（行 17-27）:**
```python
def extract_charset_from_response(resp: HTTPResponse) -> str:
    """HTTPレスポンスの Content-Type ヘッダーから charset を抽出"""
    content_type = resp.headers.get("Content-Type", "")

    for part in content_type.split(";"):
        part = part.strip()
        if part.lower().startswith("charset="):
            charset = part.split("=", 1)[1].strip()
            return charset.strip("\"'")

    return "utf-8"
```

#### 2. `interval_fetcher.py` の `body.decode()` を修正

**変更内容:**
- 行 48-49: `charset = extract_charset_from_response(resp)` を追加
- 行 49: `return body.decode(charset)` に変更（エンコーディング指定）

**修正前:**
```python
if isinstance(body, bytes):
    return body.decode()
```

**修正後:**
```python
if isinstance(body, bytes):
    charset = extract_charset_from_response(resp)
    return body.decode(charset)
```

#### 3. `main.py` の `open()` にエンコーディングを追加

**変更内容:**
- 行 51: `open(file_path, "w")` → `open(file_path, "w", encoding="utf-8")` に変更

**修正前:**
```python
with open(file_path, "w") as f:
    f.write(markdown)
```

**修正後:**
```python
with open(file_path, "w", encoding="utf-8") as f:
    f.write(markdown)
```

### フォーマット実行結果

- コマンド: `make format`
- 結果: `interval_fetcher.py` が black で整形
  - シングルクォートがダブルクォートに統一
  - その他の構文は変更なし
- `main.py`: 変更なし（既に整形済み）

---

## フェーズ3: 実装完了

**完了日時**: 2026-05-01T15:58:30+09:00（予定）

### 実装サマリー

修正ファイル:
- ✅ `src/utils/http/interval_fetcher.py` — charset 判定機能追加
- ✅ `src/handlers/fetcher/main.py` — ファイル保存時の encoding 指定

実装内容:
- HTTP レスポンスヘッダーから charset を判定して decode
- ファイル保存時は UTF-8 を明示的に指定

テスト:
- `make format` でエラーなし ✓
- コード構文確認済み ✓
