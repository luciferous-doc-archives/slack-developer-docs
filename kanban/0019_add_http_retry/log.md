# ログファイル: HTTPリクエストにリトライ機構を追加

**開始時刻**: 2026-05-05T17:35:00+09:00

## タスク概要

HTTPリクエストにリトライ機構をつけてください。リトライは最大5回。5回連続で失敗したら例外を投げてください。エクスポーネンシャルバックオフを実装してください。

## 調査結果

### HTTPフェッチャーの現在の実装

**ファイル**: `src/utils/http/interval_fetcher.py`

現在のHTTPフェッチャーは以下の構成:
- `requests.Session()` と `HTTPAdapter` でコネクションプール管理（最大10接続）
- `make_interval_fetcher(sec: float)` で指定秒数の最小間隔を強制するファクトリ関数
- クロージャの `dt_prev` で前回リクエスト時刻を保持
- エラーハンドリング: `resp.raise_for_status()` で例外を上位層に伝播

**現在のコード構造**:
```python
_session = requests.Session()
_adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
_session.mount("http://", _adapter)
_session.mount("https://", _adapter)

def make_interval_fetcher(*, sec: float):
    dt_prev: datetime | None = None
    
    @logging_function(logger)
    def interval_fetcher(*, url: str) -> str:
        # 前回から指定秒以上経過していなければ待機
        # requests でGETを実行
        # charset を自動検出してデコード
        # dt_prev を更新
```

**リトライなし**: 現在は接続エラーやタイムアウトで即座に失敗します。

### HTTPフェッチャーの使用場所

**ファイル**: `src/handlers/fetcher/main.py`

使用パターン:
- `default_fetcher(url=SITEMAP_URL)` でサイトマップを取得
- 各URLを1秒間隔でシーケンシャルにフェッチ
- エラーは上位層（main関数またはLambda handler）で処理

### エラーハンドリング現況

- HTTP エラー: `resp.raise_for_status()` で HTTPError 例外
- 接続エラー: requests がそのまま ConnectionError を投げる
- タイムアウト: requests が Timeout 例外を投げる
- ロギング: `@logging_function` デコレータが自動的に例外とスタックトレースを記録

## 実装プラン

### アプローチ

`src/utils/http/interval_fetcher.py` の `make_interval_fetcher()` 関数を拡張し、以下を実装:

1. **リトライロジック**: 最大5回までリトライ
2. **エクスポーネンシャルバックオフ**: 待機時間を 1秒 × 2^(試行回数-1) で計算
3. **リトライ対象エラー**:
   - `requests.ConnectionError` - 接続失敗
   - `requests.Timeout` - タイムアウト
   - HTTP 5xx エラー（500, 502, 503, 504 など）
   - HTTP 429 エラー（レート制限）
4. **リトライ非対象**: HTTP 4xx、その他の例外は即座に例外を投げる
5. **間隔制御との統合**: リトライのバックオフと元々の間隔制御の両方を機能させる

### 実装詳細

**関数シグネチャ拡張**:
```python
def make_interval_fetcher(
    *,
    sec: float,
    max_retries: int = 5,
    initial_backoff: float = 1.0,
) -> IntervalFetcherProtocol:
```

**内部の `interval_fetcher()` 関数**: リトライループで以下を実行:
1. HTTPリクエストを実行
2. HTTP ステータスコードを確認（5xx or 429 の場合はリトライ対象）
3. レスポンスをデコード
4. リトライ対象エラーが発生した場合、最大リトライ回数に達するまで待機して再試行
5. 最大リトライ回数に達したら例外を投げる

### デフォルト設定

```python
default_fetcher = make_interval_fetcher(
    sec=1.0,
    max_retries=5,
    initial_backoff=1.0,
)
```

## プランニング経緯

**初回提案**: 上記のアプローチで提案され、ユーザーの承認が得られました。
リトライパラメータのデフォルト値（max_retries=5, initial_backoff=1.0）、リトライ対象エラーの定義、エクスポーネンシャルバックオフの計算式に変更なし。

## 会話内容

フェーズ1のプランニングでは以下を実施:
1. `src/utils/http/interval_fetcher.py` の実装を詳細に調査
2. `src/handlers/fetcher/main.py` でのHTTPフェッチャー使用箇所を確認
3. 現在のエラーハンドリングパターンを分析
4. requests ライブラリの使用方法（Session、HTTPAdapter）を確認
5. ロギングデコレータとの統合方法を検討

ユーザーからのフィードバック: 承認（修正なし）

## 実装フェーズ

### 編集したファイル

1. **`src/utils/http/interval_fetcher.py`**
   - インポート追加: `ConnectionError`, `RequestException`, `Timeout`
   - カスタム例外クラス `RetryableHTTPError` を定義
   - `make_interval_fetcher()` 関数にパラメータ追加:
     - `max_retries: int = 5` - 最大リトライ回数
     - `initial_backoff: float = 1.0` - 初期バックオフ時間（秒）
   - リトライループ実装:
     - HTTP 5xx および HTTP 429 エラーをリトライ対象に設定
     - `ConnectionError`, `Timeout`, `RetryableHTTPError` を捕捉してリトライ
     - エクスポーネンシャルバックオフ: `wait_time = initial_backoff * (2**attempt)`
     - ログ記録: リトライ試行番号、エラー情報、待機時間
   - 成功時のみ `dt_prev` を更新
   - 最初の試行のみ前回リクエスト時刻からの間隔制御を適用
   - `default_fetcher` のパラメータ更新: `sec=1, max_retries=5, initial_backoff=1.0`

### 実行したコマンド

1. `make format` - コードをフォーマット（isort + black）
   - 結果: `interval_fetcher.py` が 1 ファイルリフォーマット

2. `uv run python3 -c "..."` - モジュールインポートテスト
   - 結果: ✓ インポート成功、✓ カスタムフェッチャー生成成功

### 判断・意思決定

1. **リトライ対象エラーの定義**
   - HTTP 5xx エラーをリトライ対象に設定（サーバーエラーは一時的な可能性が高い）
   - HTTP 429 エラーをリトライ対象に設定（レート制限は時間経過で解消）
   - HTTP 4xx エラーはリトライ対象外（クライアントエラーは修正が必要）
   - `ConnectionError` と `Timeout` を捕捉（ネットワーク一時障害）

2. **間隔制御とリトライの統合**
   - 最初の試行のみ前回リクエスト時刻からの間隔を考慮
   - リトライ試行ではエクスポーネンシャルバックオフのみで待機
   - 両方の待機が必要な場合は、最初のリクエスト時にすべて完了してからリトライに進む

3. **成功時の `dt_prev` 更新**
   - `finally` ブロックを削除し、成功時のみ更新
   - これにより、リトライ試行中に前回リクエスト時刻が上書きされることを防止

4. **ログ記録**
   - 既存の `@logging_function` デコレータで自動ログ記録
   - リトライ試行時に `logger.info()` で試行番号、エラー情報、待機時間を記録

### エラー・問題

なし - 実装完了

## 完了日時

2026-05-05T17:45:00+09:00
