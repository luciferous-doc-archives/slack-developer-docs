# Renovate設定でGithub ActionsのSHAハッシュを有効化する

## 目的
安全のため。

## 要望
renovate.jsonにGithub ActionsでSHAハッシュを使うように設定してください

## プラン
Renovate 公式プリセット `helpers:pinGitHubActionDigests` を `renovate.json` の `extends` 配列に追加する。これにより GitHub Actions マネージャーに対して `pinDigests: true` 相当の設定が自動適用され、コミット SHA によるピン留めが実現される。

変更対象: `renovate.json` — `extends` 配列に `"helpers:pinGitHubActionDigests"` を追加

## 完了サマリー

**完了日時**: 2026-04-30T13:17:31+09:00

**実施内容**:
- `renovate.json` の `extends` 配列に `"helpers:pinGitHubActionDigests"` プリセットを追加

**変更内容**:
- ファイル: `renovate.json`
  - `extends` に `"helpers:pinGitHubActionDigests"` を追加（合計 2 要素の配列に変更）

**検証**:
- JSON 構文チェック: ✓ OK

**詳細**: ログファイル `log.md` を参照
