---
title: "AIシステムを社内に導入するならLangfuseも一緒に入れておくべき理由"
url: "https://zenn.dev/bloomblock_blog/articles/langfuse-ai-system-observability"
date: 2026-05-12
tags: [Langfuse, LLMOps, オブザーバビリティ, プロンプト管理, セルフホスト, トレース, RAG, AWS ECS Fargate, GPT-5]
category: "infra"
related: [2692, 3233, 3096, 3637, 3104]
memo: "[Zenn LLM] AIシステムを社内に導入するならLangfuseも一緒に入れておくべき理由"
processed_at: "2026-05-12T09:15:36.856595"
---

## 要約

社内AIシステムの運用において、LLMの入出力・コスト・レイテンシーを可視化するオブザーバビリティツール「Langfuse」の実践的な活用事例を紹介した記事。BloomBlockが1年以上使い続けた知見をもとに、特にトラブル対応とモデル変更判断での効果を解説している。

LangfuseはオープンソースのLLM engineering platformで、トレース可視化・プロンプト管理・評価・メトリクスを統合的に扱える。セルフホストに対応しており、Docker Compose・Kubernetes・AWS/Azure/GCP向けTerraformなど複数の構成が公式ドキュメントで案内されている。BloomBlockはAWS ECS Fargateで運用している。社内業務のAIシステムではセンシティブな社内情報や個人情報がLLMに入力されるため、外部SaaSにトレースデータを送信しない構成が取れる点は重要な採用理由となる。

トレース機能では、Pythonの`@observe()`デコレーターを関数に付与するだけで計装でき、RAGにおけるコンテキスト取得・LLM呼び出し・後処理など複数ステップをひとつのトレースとしてGUIのツリー構造で確認できる。これにより「期待と異なる回答が出た」際の原因調査が、散在するアプリログを手動で追う作業からトレースIDの確認へと変わる。トラブル対応ではトレースIDをサポートチケットと紐づけることで、問題のある応答の入出力をLangfuse GUI上で即座に特定できる。

モデル変更時の判断支援として、Azure OpenAIのGPT-4oからGPT-5への切り替え検討時に`reasoning_effort: low`設定でも10秒以上のレスポンスが発生していたことをLangfuseのlatency記録で定量的に確認し、採用を見送った具体的な事例が紹介されている。その後GPT-5.1で`reasoning_effort: none`が追加されてlatencyが許容範囲になったため5.1に移行したという判断も、ダッシュボードのデータに基づいている。

プロンプト管理機能では、バージョン管理と`production`/`staging`などのラベル制御により、アプリケーションコードを変更せずにプロンプトの切り替えとロールバックが可能になる。プロンプトをリポジトリの外に置くことで、開発者以外のステークホルダー（業務担当者・プロダクトオーナー）も差分確認に参加しやすくなる点も強調されている。

監査エージェント開発への示唆として、複数LLMコール・ツール呼び出しを組み合わせるReActエージェントやLangGraphワークフローのデバッグ・品質管理にLangfuseのトレース機能は直接応用できる。各ステップの入出力・コスト・レイテンシーを記録することで、エージェントの判断根拠を事後的に追跡できるため、監査証跡としての活用も検討に値する。

## アイデア

- @observe()デコレーターによる非侵襲的な計装設計：既存コードへの変更を最小化しながらLLMコール・任意関数の両方をトレース対象にできる設計が、段階的な導入を容易にする
- トレースIDとサポートチケットの紐づけパターン：ユーザーが問題報告時にトレースIDを含める運用フローは、LLM障害対応のSLAを改善するための実践的なプラクティスとして汎用性が高い
- promptのバージョン管理をコード外に出すことで非エンジニアを改善ループに参加させる設計：productionラベルの張り替えによるロールバック機能付きで、プロンプトエンジニアリングのガバナンスと俊敏性を両立する

## 前提知識

- **LLMオブザーバビリティ** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **OpenTelemetry/トレーシング** (TODO: 読むべき)
- **LangChain/LangGraph** (TODO: 読むべき)
- **Docker/Kubernetes** (TODO: 読むべき)

## 関連記事

- /deep_2692 Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】
- /deep_3233 Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】
- /deep_3096 そのAIアプリはテストされているか：LLMアプリの自動テスト実践論
- /deep_3637 NeMo Agent Toolkit 実践運用編 — Guardrails × Langfuse による本番品質管理
- /deep_3104 MathNet：数学的推論と検索のためのグローバル・マルチモーダルベンチマーク

## 原文リンク

[AIシステムを社内に導入するならLangfuseも一緒に入れておくべき理由](https://zenn.dev/bloomblock_blog/articles/langfuse-ai-system-observability)
