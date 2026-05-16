---
title: "Harness Engineering Meetup に参加して、AIエージェントの「ハーネス」について考えた"
url: "https://zenn.dev/naomine_egawa/articles/harness-engineering-meetup-and-agent-harness"
date: 2026-05-08
tags: [Harness Engineering, Claude Agent SDK, A2A, MCP, Kubernetes, Scion, AWS Bedrock AgentCore, 状態管理, べき等性, マルチエージェント]
category: "agent-arch"
related: [2550, 3638, 2627, 3514, 16]
memo: "[Zenn LLM] Harness Engineering Meetup に参加して、AIエージェントの「ハーネス」について考えた"
processed_at: "2026-05-08T09:45:16.290499"
---

## 要約

2026年4月24日に六本木ヒルズのメルカリ本社で開催された「Harness Engineering Meetup Tokyo #1」（参加者1,700名超）のレポートと、そこから派生したハーネス設計論の整理。

「Harness Engineering」とは、AIモデルの周囲を包むインフラ層（ツール連携・状態管理・障害回復・セキュリティ・可観測性）の設計・実装を指す。2026年2月にMitchell Hashimoto（HashiCorp共同創業者）が提唱し、2026年4月には学術論文も発表された。

ミートアップで紹介された事例として、Claude Codeで10万字の長編小説を執筆するパイプラインが取り上げられた。設計書23万字・伏線47本を管理しつつ、執筆Agentとは独立した別Agentでlint相当の機械採点とコードレビュー相当のフィードバックを実施。設計書間の依存管理ツール（sdcoh）と設計RAG（OpenViking）を自作しており、「一発の精度より、揮発しない手順」という知見を示した。

AWSの公開サンプル「sample-long-running-app-harness」も分析。Claude Agent SDKを用いてGitHub IssueからフルスタックアプリをAWS Bedrock AgentCore上で最大7時間自律構築するシステム。解決されている課題は以下の5点：①Gitを真のソースとしたセッション跨ぎの状態復元、②セッション上限2分前のWIP commitによるグレースフルな終了、③commit/IssueコメントURLバッチ/S3スクリーンショットの3チャネルによる進捗可視化、④Issue完了後の優先度順バックログ自動消化、⑤GitHubラベルによる排他制御。これらはほぼすべてアプリケーション層で実装されており、AgentCore固有機能への依存は少ない。

標準化の動向として、Googleが「社内ツール→OSS→財団寄贈→デファクト標準」のパターンをエージェント領域でも展開中。A2A（Agent-to-Agent Protocol）を2025年4月に発表後Linux Foundationに寄贈（150社超参加）、ADKをOSS化、2026年4月にはK8sクラスタ対応の実行基盤Scion（experimental）を公開。通信→開発→運用の順で標準化が進む構造はgRPC→Kubernetes→Istioと同じ。

まだ標準化されていない領域として、エージェントのライフサイクル管理・セッション跨ぎの状態復元・長時間タスクのチェックポイント・ヘルスチェック・セキュリティ境界が挙げられる。著者は陳腐化しにくい知識として①ハーネスのパターン自体、②Kubernetes、③A2AとMCPへの投資を推奨している。

5つの流派（Hashimoto=失敗駆動の思想、OpenAI/Codex=コードパイプライン、Stripe=組織ガードレール、Anthropic=インターフェース層、Google=インフラ標準化）は競合でなく補完関係にあり、これらを重ね合わせた全体像がHarness Engineeringとされる。監査エージェント開発への示唆：べき等性・グレースフルな終了・状態復元・排他制御のパターンは、長時間・無人で動くエージェントに共通の設計原則であり、監査ワークフローへの適用価値が高い。

## アイデア

- 「一発の精度より、揮発しない手順」という原則：長時間エージェントタスクでは単発の高精度より再現可能な手順の設計が重要であり、設計書・ブリーフ・独立レビューAgentによるパイプライン化が小説執筆でも有効だった
- Gitを状態管理の真のソースとして使い、WIP commitによるグレースフルな終了とセッション復元を実現するパターン：DB不要で実装できる汎用的な長時間エージェント設計のカタログとして参照価値が高い
- Googleの「社内→OSS→財団→標準」パターンがエージェント領域でも進行中：通信（A2A/Linux Foundation）→開発（ADK）→運用（Scion/K8s）の順で標準化が進んでおり、現時点でまだ標準化されていない「ライフサイクル管理・チェックポイント・ヘルスチェック」領域に次の標準化ターゲットがある

## 前提知識

- **Claude Agent SDK** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **A2A Protocol** (TODO: 読むべき)
- **Kubernetes** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **GitHub Actions** → /deep_1428 AIがソフトウェア開発を変える——2026年、エンジニアリングの自動化最前線

## 関連記事

- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_3638 NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン
- /deep_2627 Autogenesis：自己進化型エージェントプロトコル
- /deep_3514 AIとAIをつなぐ意味のパイプライン設計：会話ではなく、正典・制約・実ファイルで状態を継承する
- /deep_16 長期実行アプリケーション開発のためのハーネス設計

## 原文リンク

[Harness Engineering Meetup に参加して、AIエージェントの「ハーネス」について考えた](https://zenn.dev/naomine_egawa/articles/harness-engineering-meetup-and-agent-harness)
