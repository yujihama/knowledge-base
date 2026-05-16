---
title: "OpenClaw vs Hermes Agent：2つのオープンソースAIエージェントの設計思想を徹底比較"
url: "https://zenn.dev/yukikato/articles/openclaw-vs-hermes-agent-architecture"
date: 2026-04-26
tags: [AgentHarness, OpenClaw, HermesAgent, MCP, マルチエージェント, LLMエージェント, Gateway, SQLite, FTS5, ClaudeCode]
category: "agent-arch"
related: [68, 2627, 2550, 88, 1247]
memo: "[Zenn LLM] OpenClaw vs Hermes Agent、2つのオープンソースAIエージェントの設計思想を徹底比較"
processed_at: "2026-04-26T12:17:06.992444"
---

## 要約

2026年時点で注目される2つのオープンソースAIエージェント基盤、OpenClaw（GitHub Star 358k）とHermes Agent（GitHub Star 87.3k）の設計思想を、「ハーネス（Agent Harness）」の観点から比較分析した記事。両者はMITライセンス・Claude/GPT/ローカルモデル対応・MCP対応という共通点を持つが、動作の重心が根本的に異なる。

OpenClawはTypeScript/Node.js製で、中心に「Gateway」サーバーを置くメッセージング・ゲートウェイ設計。Slack・Telegram・Discord・WhatsApp等24以上のチャネルからのメッセージを単一のGatewayが受け取り、RPC経由でPi Agent Runtimeに転送してLLMを呼び出す。設計の重心は「誰が、どこから、どのAIに、何を伝えるか」であり、組織内のコミュニケーション基盤にAIを組み込むユースケースに最適化されている。セッション開始時にはAGENTS.md・SOUL.md・TOOLS.md・IDENTITY.md・USER.md・HEARTBEAT.md・BOOTSTRAP.mdの7ファイルをシステムプロンプトに注入（1ファイル上限20,000文字、合計150,000文字）。

Hermes AgentはPython製（93.1%）で、約10,800行の巨大なAIAgentクラスが中心に位置する自律進化型設計。SQLite＋FTS5による全文検索可能な永続記憶を持ち、SOUL.mdが人格として最上位に固定され、使うほど賢くなる仕組みを標榜する。設計の重心は「1人の人間の知識と判断力の拡張」であり、個人の思考整理・情報収集・長期ナレッジ蓄積に最適化されている。

比較の補助線としてClaude Codeも取り上げられており、Auto Memory・Dream Memory Consolidation・20以上のHookイベント・Agent Teams（実験的）・Remote Tasks等の機能が紹介されている。Claude Codeの重心は「1つのリポジトリへの深い理解」にある。

3者は同じ「スケジュール実行」機能を持っていても、ハーネスの重心によって用途が分化する：Claude CodeのRemote Tasksはテスト自動修正、OpenClawのcronはSlackへの進捗投稿、HermesのcronはTelegramへの個人向けニュース要約、という具合だ。「できる」と「そのために設計されている」は異なるという観点は、監査エージェント設計において機能選定よりもアーキテクチャ上の重心設計を優先すべきことを示唆しており、LangGraph等でエージェントを構築する際のハーネス設計判断に直接応用できる。

## アイデア

- ハーネスの「重心」という概念：同じ機能カテゴリ（メモリ・cron・マルチエージェント）を持つフレームワークでも、何を中心に最適化しているか（リポジトリ・メッセージフロー・人間の知性拡張）によって実運用での挙動が根本的に変わるという設計論
- MEMORY.mdの実装と公式ドキュメントの乖離（OpenClawはDMのみと公式記載されているが実装ではsubagent/cron以外の全セッションで注入される）という、OSSにおけるドキュメントとコードの信頼性問題
- 3層構成の使い分け提案：OpenClaw（組織コミュニケーション層）＋Hermes（個人ナレッジ層）＋Claude Code（コーディング層）という並列運用モデルは、監査エージェントにおける役割分担設計の参考になる

## 前提知識

- **LLMハーネス設計** (TODO: 読むべき)
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **SQLite FTS5** → /deep_18 AIに20年分の日記を読ませたら人格が生まれて勝手にゲームを作り始めた
- **システムプロンプト注入** (TODO: 読むべき)

## 関連記事

- /deep_68 Claudeは明日もあなたを忘れる — MCP Memory Server cpersona 設計と実践
- /deep_2627 Autogenesis：自己進化型エージェントプロトコル
- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷

## 原文リンク

[OpenClaw vs Hermes Agent：2つのオープンソースAIエージェントの設計思想を徹底比較](https://zenn.dev/yukikato/articles/openclaw-vs-hermes-agent-architecture)
