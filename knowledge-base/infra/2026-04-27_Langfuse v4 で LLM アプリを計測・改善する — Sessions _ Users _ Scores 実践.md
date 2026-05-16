---
title: "Langfuse v4 で LLM アプリを計測・改善する — Sessions / Users / Scores 実践ガイド"
url: "https://zenn.dev/takish/articles/ebb7cb6a230e2a"
date: 2026-04-27
tags: [Langfuse, LLMOps, Observability, OpenTelemetry, LLM-as-a-judge, Tracing, Python SDK]
category: "infra"
related: [398, 1349, 897, 2214, 2061]
memo: "[Zenn LLM] Langfuse v4 で LLM アプリを計測・改善する — Sessions / Users / Scores 実践ガイド"
processed_at: "2026-04-27T12:37:39.432099"
---

## 要約

Langfuse v4 は OSS の LLMOps プラットフォームで、LLM アプリの「計測と改善のループ」を最小コストで構築するための4機能（Tracing・Sessions・Users・Scores）を提供する。Python SDK v4 系は OpenTelemetry ベースに刷新されており、`@observe` デコレータ1行で関数全体を trace に変換できる。OpenAI・Anthropic・Gemini・LangChain・LlamaIndex への自動計装も提供され、ラッパー SDK に差し替えるだけで全呼び出しが自動記録される。

Sessions 機能では `propagate_attributes(session_id=...)` を使い、マルチターン会話や RAG パイプラインの複数ステージを1セッションにグループ化できる。UI 上ではセッション全体のトータルコスト・レイテンシ・会話フローが時系列で確認可能。Users 機能は `user_id` を同じ `propagate_attributes()` に渡すことで有効になり、ユーザー別の総コスト・累計トークン数・エラー率・最終アクティビティをダッシュボードで把握できる（GDPR 対応としてメールアドレス等の個人情報ではなくハッシュ化 ID を推奨）。

Scores 機能は LLMOps の核で、trace に品質数値を付与する仕組み。ソースは3種類：①チャット UI の👍/👎ボタン等のユーザーフィードバック（`langfuse.create_score()` で POST）、②LLM-as-a-judge（別モデルが 0〜1 でスコアリングし `span.score()` で保存）、③Human-In-The-Loop での編集率（`hitl.edit_rate` として変更フィールド数/全フィールド数を記録）。Score 名は `<カテゴリ>.<指標名>` 形式で自由命名でき、時系列プロットでプロンプト変更・モデル変更の効果を定量比較できる。

Dataset + Experiments 機能でゴールデンケースへの自動評価も可能。Cloud 版は Hobby プランの無料枠あり、Self-hosted 運用にも対応するため機微データの内部管理も実現できる。監査エージェント開発への示唆として、ReAct エージェントの各ステップ（Retrieve→Rerank→Generate）を `@observe` でネストした span として記録し、LLM-as-a-judge でステップごとの精度を Score 化する構成が、エージェント品質の継続的モニタリングに直接応用できる。

## アイデア

- LLM-as-a-judge を非同期でバックグラウンド実行し、本番レスポンスのレイテンシに影響させずスコアを蓄積する設計パターン
- HITL ワークフローの編集率（edit_rate）を Score 化することで、プロンプト改善の定量評価ループを自動化できる点
- OpenTelemetry ベースの SDK により、既存の分散トレーシング基盤（Jaeger, Tempo 等）とも統合しやすい可能性がある

## 前提知識

- **OpenTelemetry** → /deep_1349 ALTK-Evolve: AIエージェントのオンザジョブ学習システム
- **LLM-as-a-judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **RAG パイプライン** (TODO: 読むべき)
- **FastAPI** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **デコレータパターン** (TODO: 読むべき)

## 関連記事

- /deep_398 LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）
- /deep_1349 ALTK-Evolve: AIエージェントのオンザジョブ学習システム
- /deep_897 時系列説明のためのLLM-as-a-Judge：参照なし評価フレームワーク
- /deep_2214 偏好対からLLMは何を学ぶか：Delta分解でDPOを効率化
- /deep_2061 プロンプト改善は後回し: LangGraphでさっさと実装、MLflowで誤りから暗黙知を吸収&改善

## 原文リンク

[Langfuse v4 で LLM アプリを計測・改善する — Sessions / Users / Scores 実践ガイド](https://zenn.dev/takish/articles/ebb7cb6a230e2a)
