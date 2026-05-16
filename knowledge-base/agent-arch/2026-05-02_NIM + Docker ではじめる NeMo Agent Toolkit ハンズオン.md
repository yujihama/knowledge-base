---
title: "NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン"
url: "https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson"
date: 2026-05-02
tags: [NeMo Agent Toolkit, NIM, Docker, NVIDIA, RAG, Milvus, マルチエージェント, A2A, MCP, Phoenix, YAML]
category: "agent-arch"
related: [2627, 3514, 2550, 88, 1914]
memo: "[Zenn LLM] NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン"
processed_at: "2026-05-02T12:37:14.493162"
---

## 要約

本書はNVIDIAのNeMo Agent Toolkit（NAT）をNIM（NVIDIA Inference Microservices）とDockerを用いてローカル環境で動かすための実践的ハンズオンガイド（約14万字）。全15章＋付録2本で構成され、環境構築から本番Web API化まで段階的に解説している。

技術スタックは、Colima（macOS向け軽量VM）+ Docker + NGC（NVIDIA GPU Cloud）を基盤とし、NIMコンテナ経由でLLM推論をローカル実行する。NeMo Agent Toolkitは、YAMLベースのワークフロー定義でエージェントを宣言的に構築できるフレームワークで、Python実装に比べてエージェント設定の見通しが良い点が特徴。

主要トピックは以下の通り：(1) 最短構成の「Hello Agent」から始め、YAMLワークフローの構造（ステップ定義・ツール連携・条件分岐）を段階的に読み解く。(2) 組み込みツール（Web検索・コード実行等）の組み合わせによる複合エージェント構築。(3) Routerパターンによるマルチエージェントのタスク振り分けと、A2A（Agent-to-Agent）プロトコルによるエージェント間通信。(4) MilvusベクトルデータベースへのNATドキュメント投入によるRAG構築、永続化・メタデータフィルタ・top_kチューニングを含む運用設計。(5) Phoenixによるエージェント動作の可観測性（トレース・スパン可視化）。(6) nat evalコマンドによる自動採点パイプライン、nat serveによるOpenAI互換Web API化。

監査エージェント開発への示唆として、YAMLワークフローによる宣言的エージェント定義はLangGraphのグラフ定義に近い概念であり、ステップの可視化・テスト・再現性確保が容易。A2Aプロトコルは複数の専門エージェント（証拠収集・リスク評価・レポート生成）を疎結合に連携させる監査ワークフロー設計に直接応用可能。nat evalの自動採点機構はLLM-as-judgeパターンの実装例として参照価値が高い。RAGのメタデータフィルタは監査基準書や法令の年度・カテゴリ別検索に有効なアーキテクチャ選択肢。

## アイデア

- YAMLベースのワークフロー定義でエージェントを宣言的に構築するアプローチは、コードではなく設定として管理できるため、非エンジニアとの協働やバージョン管理・差分レビューが容易になる
- A2AプロトコルによるAgent-to-Agent通信は、専門特化した複数エージェントを疎結合で連携させる設計パターンであり、監査ワークフローのような多段階・多役割タスク分解に直接応用できる
- nat evalによる自動採点パイプラインとPhoenixの可観測性統合により、エージェントの品質評価とトレース分析を一貫して行えるMLOps的な開発サイクルが実現できる

## 前提知識

- **NeMo Agent Toolkit** → /deep_63 NVIDIAがDGX SparkとReachy Miniでエージェントを現実世界に具現化
- **NIM（NVIDIA Inference Microservices）** (TODO: 読むべき)
- **RAG / Milvus** (TODO: 読むべき)
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **Docker / Colima** (TODO: 読むべき)

## 関連記事

- /deep_2627 Autogenesis：自己進化型エージェントプロトコル
- /deep_3514 AIとAIをつなぐ意味のパイプライン設計：会話ではなく、正典・制約・実ファイルで状態を継承する
- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1914 現在多くのAI memory製品は、実際には少し高度なチャット履歴に過ぎない

## 原文リンク

[NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン](https://zenn.dev/himorishige/books/nemo-agent-toolkit-nim-handson)
