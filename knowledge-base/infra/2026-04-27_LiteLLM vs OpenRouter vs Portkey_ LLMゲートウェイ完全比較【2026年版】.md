---
title: "LiteLLM vs OpenRouter vs Portkey: LLMゲートウェイ完全比較【2026年版】"
url: "https://zenn.dev/agdexai/articles/llm-gateway-comparison-2026"
date: 2026-04-27
tags: [LiteLLM, OpenRouter, Portkey, LLMゲートウェイ, フォールバック, ロードバランシング, 可観測性, セルフホスト, OpenAI互換API, コスト最適化]
category: "infra"
related: [1641, 2592, 1427, 2544, 609]
memo: "[Zenn LLM] LiteLLM vs OpenRouter vs Portkey: LLMゲートウェイ完全比較【2026年版】"
processed_at: "2026-04-27T12:12:54.575876"
---

## 要約

AIエージェントの本番運用において欠かせないLLMゲートウェイの3大ツール（LiteLLM・OpenRouter・Portkey）を機能・用途・コスト観点で比較した記事。LLMゲートウェイとは、複数のLLMプロバイダーを統一APIで扱い、フォールバック・ロードバランシング・コスト追跡・レート制限管理を自動化するミドルウェア層。プロバイダーロックインやコスト爆発、可観測性の欠如といった本番運用課題をまとめて解決する。

LiteLLMはオープンソース（Apache 2.0）のセルフホスト型で、100以上のモデル（OpenAI / Anthropic / Gemini / Mistral / Ollama等）をOpenAI互換APIで統一。プロキシサーバーとして起動することで既存コードを変更せず導入でき、Kubernetes環境との親和性が高い。データが外部に出ないためセキュリティ重視のエンタープライズ向け。弱点は運用コストとUIのシンプルさ。

OpenRouterはクラウドマネージド型で300以上のモデルを単一APIで横断利用できる。Llama 3・Mistral・Gemmaなど無料モデルが多数あり、セットアップ5分・費用ゼロで実験可能。自動コスト最安ルーティング機能を持つが、クラウド経由のためデータプライバシーへの配慮が必要で、本番環境の細かい制御は苦手。スタートアップや個人開発者のプロトタイプ段階に最適。

Portkeyはクラウド＋セルフホストのハイブリッド型で250以上のモデルに対応。詳細なトレース・ログ・コスト分析ダッシュボード、プロンプトのバージョン管理、A/Bテストのネイティブサポートが強み。MLOps・プロダクションチーム向けだが、高度な機能は有料プランが必須でセットアップがやや複雑。

機能比較では、セルフホスト対応はLiteLLMとPortkey（一部）のみ、プロンプト管理とガードレールはPortkeyが最も充実。ユースケース別の推奨は、実験段階→OpenRouter、社内/エンタープライズ→LiteLLMセルフホスト、プロダクション運用→Portkey。コスト最適化にはOpenRouter（自動ルーティング）＋LiteLLM（フォールバック制御）の組み合わせも有効とされている。

2026年のトレンドとして、LLMゲートウェイは単純なプロキシから、Tool calling標準化・セマンティックキャッシュ・ガードレール統合・マルチモーダル対応へと役割が拡大している。監査エージェント開発への示唆として、LiteLLMのセルフホストは社内データを外部送信せずに複数LLMを切り替えられる点で監査用途に適しており、PortkeyのトレースとA/Bテスト機能はLLM-as-judgeの品質管理や監査ログの要件を満たす可能性がある。

## アイデア

- OpenRouter（実験）→ LiteLLM（本番セルフホスト）→ Portkey（可観測性レイヤー）という段階的な組み合わせ戦略は、ツールを排他的に選ぶ必要がなく、開発フェーズに応じてゲートウェイを使い分けられる実践的なアーキテクチャパターン
- セマンティックキャッシュ（同意の質問を検出してAPI呼び出しを削減）はLLMゲートウェイレイヤーで実装することで、アプリケーションコードを変更せずにコスト削減を実現できる点が興味深い
- LiteLLMのプロキシサーバーモード（既存コード無変更で導入可能）は、LangGraphベースの監査エージェントに対してインフラレイヤーで透過的にフォールバック・ロードバランシングを追加できる設計として応用価値が高い

## 前提知識

- **OpenAI互換API** → /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- **フォールバック戦略** → /deep_972 論文「Learning to Reason with LLMs」を実運用視点で解説：企業導入で注意すべき5つのリスク
- **LLMプロキシ** (TODO: 読むべき)
- **MLOps** → /deep_1645 雰囲気でML運用してない？Google流「ML Test Score」でMLパイプラインの信頼性を数値化する
- **レート制限** → /deep_2215 Claudeの指示に従ったらGitHub・Hacker News・RedditでBANされた話

## 関連記事

- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_2592 LiteLLM 入門 ── 複数 LLM を統一インターフェースで扱う AI Gateway
- /deep_1427 Claude Code CLIをGLM/MiniMaxで代替した話（コスト大幅削減の実測）
- /deep_2544 1回答0.03円で営業メールを分類する -- Next.js after() + OpenRouter の非同期分類パイプライン
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話

## 原文リンク

[LiteLLM vs OpenRouter vs Portkey: LLMゲートウェイ完全比較【2026年版】](https://zenn.dev/agdexai/articles/llm-gateway-comparison-2026)
