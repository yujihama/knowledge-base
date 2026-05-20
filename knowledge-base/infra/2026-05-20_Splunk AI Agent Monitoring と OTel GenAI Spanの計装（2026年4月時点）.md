---
title: "Splunk AI Agent Monitoring と OTel GenAI Spanの計装（2026年4月時点）"
url: "https://zenn.dev/gen_sobunya/articles/splunk-ai-agent-otel-attributes"
date: 2026-05-20
tags: [OpenTelemetry, Splunk, AIエージェント監視, GenAI Semantic Conventions, OTel計装, DeepEval, 可観測性, LLMトレーシング]
category: "infra"
related: [398, 3637, 3091, 3136, 3231]
memo: "[Zenn LLM] Splunk AI Agent Monitoring と OTel GenAI Spanの計装(2026/4時点)"
processed_at: "2026-05-20T21:01:48.320688"
---

## 要約

SplunkのObservability Solutions ArchitectによるSplunk AI Agent MonitoringとOpenTelemetry GenAI Semantic Conventionsの実装知見まとめ。Splunk Observability CloudでAIエージェントのトレース・評価を可視化するには、単にトレースを送信するだけでは不十分で、複数の設定が必要となる。具体的には、gen_ai.operation.nameを持つspan送信、signalfx.send_otlp_histograms: trueによるhistogramメトリクス収集、OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=trueとSPAN_AND_EVENTモードによるメッセージcapture、DeepEvalとsplunk_hec/logs exporterを使ったレスポンス評価、Log Observer ConnectによるSplunk Cloud/EnterpriseとObservability Cloudの連携が必要。サンプルアプリはorchestrator-api（プレイブック検索ツール実行）とworker-agent（LLM呼び出し）の2層構成で、vLLMまたはOllama（OpenAI互換API）をバックエンドとして使用。トレース構造はworkflow → execute_tool → invoke_agent → chatの階層で、GenAI spanはsplunk-otel-util-genaiで手動計装。最大のハマりポイントはCollectorのlogs pipelineで、アプリケーションログ（filelog receiver）とGenAI content logs/評価イベント（otlp receiver）を別々に処理する必要があった。gen_ai.input.messages等のAI Details用contentはOTLP logsとして出力されるため、otlp receiverなしではAI Detailsが表示されない。レスポンス評価はObservability Cloud側が直接プロンプトを評価するのではなく、instrumentation frameworkがDeepEvalで評価してCollectorが結果をSplunk Platformに送信する仕組み。使用パッケージはsplunk-otel-util-genai==0.1.11、splunk-otel-genai-evals-deepeval==0.1.7等。監査エージェントへの示唆として、AIエージェントの動作をAPMレイヤーでトレースし品質スコアで評価する本アーキテクチャは、監査エージェントのアクション説明責任とログ証跡確保に直接応用可能。特にDeepEvalによる自動評価とOTelトレースの紐付けは、LLM-as-judgeによる監査判断品質の継続的モニタリング基盤として活用できる。

## アイデア

- アプリケーションログとGenAI content logsを別receiverで処理する必要がある点は非自明で、filelog単独ではAI Detailsが表示されないという具体的な落とし穴が実務で重要
- レスポンス評価をObservability Cloud側ではなくinstrumentation framework（DeepEval）側で実施しスコアのみを送信するアーキテクチャは、プロンプト本文をクラウド側に渡さないプライバシー設計として注目に値する
- gen_ai.operation.name（chat/execute_tool/invoke_agent/invoke_workflow）によってSpan種別を識別し階層的なAIエージェントトレースを構築するパターンは、マルチエージェント監査システムの可視化設計に直接転用可能

## 前提知識

- **OpenTelemetry** → /deep_1349 ALTK-Evolve: AIエージェントのオンザジョブ学習システム
- **Splunk Observability Cloud** (TODO: 読むべき)
- **GenAI Semantic Conventions** → /deep_398 LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）
- **DeepEval** (TODO: 読むべき)
- **OTel Collector** (TODO: 読むべき)

## 関連記事

- /deep_398 LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）
- /deep_3637 NeMo Agent Toolkit 実践運用編 — Guardrails × Langfuse による本番品質管理
- /deep_3091 LiteLLM vs OpenRouter vs Portkey: LLMゲートウェイ完全比較【2026年版】
- /deep_3136 Langfuse v4 で LLM アプリを計測・改善する — Sessions / Users / Scores 実践ガイド
- /deep_3231 LLMルーターの自動プロファイル選択をrule-basedでどこまでやるか—CodeRouter v1.6 auto_router

## 原文リンク

[Splunk AI Agent Monitoring と OTel GenAI Spanの計装（2026年4月時点）](https://zenn.dev/gen_sobunya/articles/splunk-ai-agent-otel-attributes)
