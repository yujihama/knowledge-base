---
title: "製造業RAGの本番運用設計：Evals・Observability・Prompt Versioning・Fallback【コード付き】"
url: "https://zenn.dev/kukyotolab/articles/llm_production_ops"
date: 2026-05-22
tags: [RAG, LLM-as-Judge, Observability, Prompt Versioning, Fallback, 製造業, Evals, ChromaDB, Cohere, claude-sonnet-4-6]
category: "audit-ai"
related: [2103, 5460, 5472, 1334, 112]
memo: "[Zenn LLM] 製造業RAGの本番運用設計：Evals・Observability・Fallback【コード付き】"
processed_at: "2026-05-22T09:05:05.036729"
---

## 要約

製造業向けRAGシステムを本番環境で継続稼働させるための4フェーズ実装を解説した記事。ChromaDB + Cohere + Claude（claude-sonnet-4-6）を対象に、PoCと本番の差分として「品質測定・障害追跡・プロンプト変更管理・フォールバック」の4課題に実装で答える。

Phase 1（Evals）では、LLM-as-a-JudgeによるModel GraderとルールベースのCode Graderを組み合わせる。評価軸はAccuracy×0.30・Grounding×0.20・Safety×0.20・Consistency×0.15・Uncertainty×0.15の加重平均。Judgeモデルにtemperature=0を指定し評価の安定性を確保。11件のテストケースで攻撃系クエリ（Prompt Injection・機密データ要求）が正常系より低スコアとなることを確認し、評価軸の機能を検証した。Code Graderでは正規表現でPII（メールアドレス・電話番号）・APIキー候補・スクリプトインジェクションを検出。

Phase 2（Observability）では、ログ・トレーシング・メトリクスの3層を分離。request_idを全ログに付与し1リクエストの全ステップを追跡可能にする。トレーシングはコンテキストマネージャ実装でspan単位のレイテンシを計測し、1リクエスト内でvector_search（142ms）・llm_call（1847ms）・output_filter（1.2ms）のボトルネック分布を可視化。出力はJSONLで、CloudWatch Logs/Datadog/OpenTelemetryへの転送はlogger.log()の出力先差し替えで対応可能な設計。

Phase 3（Prompt Versioning）では、YAMLでバージョン付きプロンプトを管理するPromptRegistry・A/Bテスト用のVersionSelector・旧バージョンへのロールバック機能を実装。プロンプトを「設定」ではなく「コード」として扱い、変更前後のスコア比較を可能にする。

Phase 4（Fallback/SLA/SLO）では、Claude APIダウン時の自動切り替えとSLA/SLO閾値監視・アラート機構を実装。ローカル動作確認を前提としており、本番ではSIEM連携・PagerDuty/Slack通知・外部プロンプトストアが追加で必要と明示。監査エージェント開発への示唆として、LLM-as-a-Judge評価パイプラインはRAG回答品質の継続的測定に直接転用可能であり、request_idベースのトレーシングは監査ログの証跡管理設計とほぼ同構造。

## アイデア

- Model Grader（LLM-as-Judge）とCode Grader（ルールベース正規表現）を組み合わせることで、意味的品質とフォーマット準拠を独立して評価し、combined_scoreの構成を透明化している設計
- request_idを全ログ・トレーシングに付与してエンドツーエンド追跡を可能にする構造は、監査エージェントの証跡管理（誰がいつ何を問い合わせたか）と同一アーキテクチャパターンで転用できる
- Prompt VersioningをYAML管理＋A/Bテスト＋ロールバックとして実装することで、プロンプトをコードと同様にCI/CDパイプラインに組み込む基盤となる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LLM-as-a-Judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **ChromaDB** → /deep_1242 AI AgentメモリーOSS「MemPalace」徹底解説 — 記憶の宮殿アーキテクチャとベンチマーク論争
- **Prompt Injection防御** (TODO: 読むべき)
- **SLA/SLO** (TODO: 読むべき)

## 関連記事

- /deep_2103 製造業RAG運用編：監査ログ + イベント駆動再インデックスを実装する
- /deep_5460 3つのLLMプロバイダーで同一RAGを実装して比較——セキュリティ境界はアプリケーション層に置くべき理由
- /deep_5472 LLMエンジニアとして最初の3ヶ月に何をするべきか：ロードマップと優先順位
- /deep_1334 製造業向けRAGシステムのアクセス制御設計
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた

## 原文リンク

[製造業RAGの本番運用設計：Evals・Observability・Prompt Versioning・Fallback【コード付き】](https://zenn.dev/kukyotolab/articles/llm_production_ops)
