---
title: "LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）"
url: "https://zenn.dev/baobao1219/articles/76afbe3dc37815"
date: 2026-03-30
tags: [OpenTelemetry, Langfuse, Arize Phoenix, LLM Observability, GenAI Semantic Conventions, Evals, Structured Outputs, トレーシング, コスト監視, HITL]
category: "infra"
memo: "[Zenn LLM] LLMで“見える運用”へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix)"
processed_at: "2026-03-30T12:09:33.312001"
---

## 要約

本記事は、LLMをプロダクション環境で運用する際に必要な可観測性（Observability）の設計と実装を実務視点でまとめたものである。観測対象は「3信号（トレース・メトリクス・イベント）×5項目（リクエストトレース・レイテンシ・コスト・品質・逸脱兆候）」に整理される。スタック構成は、OpenTelemetry GenAIの標準規約に準拠した収集レイヤー（Python Contrib GenAIによるOpenAIクライアントの自動トレース）と、LLM特化の集約・探索レイヤー（LangfuseまたはArize Phoenix）の2層で最小構成を取る。LangfuseはOTelネイティブSDKを持ち、スパンをgenerations/eventsへ自動変換できる点が特徴。LLMそのものを可観測性強化に活用する手法として、①自然言語によるメトリクス探索（Honeycombの事例）、②膨大なスパンのクラスタリング→要約→原因候補抽出（Arize PhoenixやArize AI推奨のワークフロー）、③Structured Outputs（JSON Schema）によるLLM出力の構造化と可観測基盤への直接連携（パースエラー対策として再試行・フォールバック設計が必要）の3パターンが紹介されている。ダッシュボードはSRE向け（p95/p99・エラー率・ツール失敗）、PM向け（有効応答率・コスト/会話・HITL率）、開発向け（プロンプト改版ごとの品質・コスト・レイテンシ回帰）の役割別に薄く作ることを推奨し、いずれも同一トレースから属性名（OTel GenAI準拠）の違いで切り出す設計を取る。Evals（評価）はトレースと結合し、品質低下断面のトレースをデータセット化→プロンプト最適化・Retrieval改善・モデル切替へ送るフィードバックループを構築する。LLMアプリ特有のインシデント切り分け観点として、prefill/decode遅延の分離、KVキャッシュ溢れによる再試行嵐の検知、ツール呼び出し待ち（トレースの枝で確認）、評価スコアのドリフト（モデル更新・プロンプト改版履歴との突き合わせ）が挙げられている。OTel準拠のスキーマ設計により、ツール乗り換えコストを低く保ちながら、将来のダッシュボード再利用が可能になる点が本記事の核心的な主張である。

## アイデア

- OTel GenAI属性をスキーマの共通語彙として固定することで、LangfuseやPhoenixなどツールを乗り換えても既存ダッシュボードが生き続ける「語彙先行設計」の考え方
- LLM自身を可観測性パイプラインに組み込み、膨大なスパンをクラスタリング→要約→異常の「物語」として抽出する自己参照的な運用ループ
- Structured Outputs（JSON Schema）でLLM出力を構造化し可観測基盤に直接連携する設計と、パース失敗を前提とした再試行・フォールバックの必要性
## 関連記事

- /deep_1349 ALTK-Evolve: AIエージェントのオンザジョブ学習システム
- /deep_1516 責任経路設計はMeaningful Human Controlと何が違うのか―軍事AIのaccountability議論との接点とは
- /deep_1426 RACI / HITL / Guardrails / 責任経路設計の違い
- /deep_146 OpenAI、LLMテスト・評価フレームワーク「Promptfoo」を買収
- /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）

## 原文リンク

[LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）](https://zenn.dev/baobao1219/articles/76afbe3dc37815)
