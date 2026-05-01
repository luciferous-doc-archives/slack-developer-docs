# タスク 0009: GitHub Actions で fetcher.py を実行するように整備する

**開始時刻**: 2026-05-01T16:40:00+09:00

## タスク概要

Pythonで実装した`fetcher.py`を GitHub Actions の`fetch-docs.yml`ワークフローに統合し、スケジュール実行（毎日 03:00 JST）および手動トリガーで自動実行できるようにする。

## 調査結果

### ワークフロー構成
- **ファイルパス**: `.github/workflows/fetch-docs.yml`
- **現在の状態**: スケルトン実装
- **実装済み**:
  - Checkout ステップ
  - タイムスタンプ生成（`date -u +'%Y%m%d-%H%M'` で UTC 形式）
  - タイムスタンプ表示（プレースホルダー）
- **未実装**: fetcher.py の実行

### Python 実装
- **エントリポイント**: `src/handlers/fetcher/__init__.py`
- **メイン処理**: `src/handlers/fetcher/main.py`
- **環境変数**: `BASE_TIMESTAMP`（必須）
- **PYTHONPATH**: `src`
- **出力形式**: `docs/slack-developer-docs-{BASE_TIMESTAMP}/` ディレクトリツリー
- **ZIP 生成**: 未実装（このタスクのスコープ外）

### 依存関係
- **Python バージョン**: 3.14+（pyproject.toml で指定）
- **パッケージマネージャー**: uv
- **依存ライブラリ**: aws-lambda-powertools[all]>=3.28.0

## 実装プラン

`.github/workflows/fetch-docs.yml` に以下のステップを「Set timestamp」の後に追加:

1. **Install uv**: `astral-sh/setup-uv@v3` アクション
   - Python 環境も自動セットアップされるため、`actions/setup-python` は不要

2. **Install dependencies**: `uv sync`
   - pyproject.toml の依存ライブラリをインストール

3. **Run fetcher**: `uv run src/handlers/fetcher.py`
   - 環境変数 `BASE_TIMESTAMP` と `PYTHONPATH=src` を設定

## プランニング経緯

初回提案がそのまま承認された。ただしユーザーからの フィードバック:
1. Setup Python ステップは不要（uv がセットアップ）
2. fetcher 実行は `uv run src/handlers/fetcher.py` で実行
3. 環境変数 `PYTHONPATH=src` を設定
4. ZIP アーカイブ作成はスコープ外

## 会話内容

### プランモード提案
- GitHub Actions ワークフロー構成を 2 つの Explore agent で調査
- 第1 agent: ワークフロー定義ファイルの調査 → スケルトン実装を確認
- 第2 agent: Python 実装の調査 → エントリポイント・環境変数・実行方法を確認

### ユーザーフィードバック
1. 「uv のセットアップで Python 環境もセットアップされるので Setup Python は必要ありません」
   → 計画から削除
2. 「Run fetcher については uv 経由で実行するようにしてください。また `PYTHONPATH=src` も設定してください」
   → 実行コマンドと環境変数を修正
3. 「zip アーカイブの作成は今回のスコープから外したい」
   → スコープを限定（fetcher 実行統合のみ）
4. 「Run fetcher については `uv run src/handlers/fetcher.py` で実行してください」
   → 実行コマンドを明確化

## 実装内容

### 修正ファイル

#### `.github/workflows/fetch-docs.yml`

**追加ステップ** (20 行目の後):

```yaml
      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Install dependencies
        run: uv sync

      - name: Run fetcher
        env:
          BASE_TIMESTAMP: ${{ steps.timestamp.outputs.value }}
          PYTHONPATH: src
        run: uv run src/handlers/fetcher.py
```

**変更理由**:
- `astral-sh/setup-uv@v3`: uv をインストール、Python 環境もセットアップ
- `uv sync`: 依存ライブラリをインストール
- `uv run src/handlers/fetcher.py`: Python スクリプト実行（uv を経由）
- `BASE_TIMESTAMP` env: タイムスタンプを fetcher に渡す
- `PYTHONPATH: src` env: Python モジュールパスを設定

### テスト検証

1. **手動実行**: GitHub Web UI から `workflow_dispatch` でワークフロー実行
2. **実行ログ確認**: 各ステップの成功・失敗を確認
3. **出力確認**: `docs/slack-developer-docs-{timestamp}/` ディレクトリにマークダウンファイルが保存されているか確認
4. **定期実行確認**: 次の定時実行（毎日 03:00 JST）が正常に実行されることを確認

## 完了サマリー

**完了日時**: 2026-05-01T16:40:00+09:00

GitHub Actions ワークフロー `fetch-docs.yml` に fetcher.py 実行ステップを統合しました。

**実装内容**:
- uv インストール（astral-sh/setup-uv@v3）
- 依存ライブラリインストール（uv sync）
- fetcher.py 実行（`uv run src/handlers/fetcher.py` で BASE_TIMESTAMP 環境変数を渡す）

**スコープ外**:
- ZIP ファイル生成
- GitHub Releases へのアップロード

ワークフローは手動トリガー（workflow_dispatch）および定期スケジュール実行（毎日 03:00 JST）で動作します。
