# Basic認証が必要なURLをスキップする

## 目的
この4つのURLはBasic認証を求められるためスキップするようにして欲しい。スキップ対象は配列でグローバル領域に保持して欲しい (できるだけソースコードの上部に持ってて欲しい)。

## 要望
下記URL4つを処理対象外としてスキップするようにして欲しい

### 処理対象外のURL
- https://docs.slack.dev/super-secret.md
- https://docs.slack.dev/super-secret/maintainers-guide.md
- https://docs.slack.dev/super-secret/onboarding.md
- https://docs.slack.dev/super-secret/style-guide.md

## 完了サマリー

**完了日時**: 2026-05-01T16:15:00+09:00

**変更内容**:
- `src/handlers/fetcher/main.py` に以下を追加:
  - グローバル定数 `SKIP_URL_PREFIXES` （プリフィックスマッチ方式）
  - フィルター関数 `_should_skip_url()`
  - `main()` 関数内でのフィルタリング処理
  - スキップされたURLのログ出力

**テスト**: シンタックスチェック実施（エラーなし）
