---
title: "OpenAI Codex徹底解説：CLI・Plan mode・Skills・MCP・Subagents・内部構造まで"
url: "https://zenn.dev/dokusy/articles/99af2fae0f1291"
date: 2026-05-12
tags: [OpenAI Codex, Codex CLI, MCP, Subagents, AGENTS.md, Plan mode, codex exec, sandbox, approval policy, コーディングエージェント]
category: "agent-arch"
related: [91, 4624, 4373, 2880, 4661]
memo: "[Zenn LLM] codexにcodexの徹底解説をしてもらった"
processed_at: "2026-05-12T09:17:07.176999"
---

## 要約

本記事はcodex-cli 0.130.0（2026-05-11時点）を用い、Codex自身に自己解説させた内容をまとめたものである。Codexは「コード補完ツール」ではなく「コーディングエージェント」であり、コードベースの読解・方針立案・ファイル編集・コマンド実行・テスト・レビュー・PR作成まで一貫して行う。入口は①Codex CLI（ターミナル対話型TUI）②IDE extension（VS Code/Cursor/Windsurf）③Codex app（GUI）④Codex web（クラウドタスク委譲）⑤GitHub連携⑥codex exec（非対話自動化）⑦App Server/MCP Serverの7種類に分かれる。CLIの基本コマンドとして`codex`（対話TUI）、`codex exec`（CI・定期ジョブ向け非対話モード、stderrに進捗・stdoutに最終出力）、`codex review`（diff専用レビューエージェント）、`codex cloud`（クラウドタスク管理）が存在する。安全設計の中核はsandbox mode（read-only / workspace-write / danger-full-access）とapproval policy（untrusted / on-request / never）の2層構造で、日常実装では`workspace-write + on-request`が推奨される。AGENTS.mdはリポジトリルートに置くプロジェクト固有の指示書で、技術スタック・禁止事項・テスト方法・権限ポリシーを記述し、Codexがセッション開始時に自動読み込みする。Skillsは繰り返しタスクをスラッシュコマンド化する仕組み、Pluginsは外部ツール呼び出しの拡張機構、MCPはModel Context Protocolによるサーバー接続でファイルシステム・DB・外部API・別エージェントとの連携を担う。Subagentsは複雑タスクを複数の専門エージェントに分割して並列実行する機構で、オーケストレーター型（Codexが指示）と委譲型（完全独立）の2形態がある。Plan modeではCodexが変更前に実装計画を提示し、承認後に実行する。config.tomlで設定を永続化でき、デフォルトモデル・sandboxモード・approval policyを記述可能。監査エージェント開発への示唆として、`codex exec --json`のJSON Lines出力（thread.started / turn.completed / item.* / error等のイベント型）はLangGraphのステートマシンと組み合わせた証跡ログ設計に直接応用できる。また、AGENTS.mdによるエージェント権限の宣言的管理はReActエージェントのツール制限ポリシー設計と同じ問題を別アプローチで解決しており、監査AI向けの権限制御設計の参考になる。

## アイデア

- codex exec --jsonのJSON Lines出力（thread.started / turn.completed / item.*）は機械可読な証跡ログとして活用でき、監査エージェントの実行ログ設計に直接応用可能
- AGENTS.mdによる権限・禁止事項・テスト方法の宣言的記述は、エージェントの振る舞いをコードではなくドキュメントで制御する「Policy-as-Document」パターンの実例
- sandbox mode（read-only / workspace-write / danger-full-access）とapproval policy（untrusted / on-request / never）の直交する2軸設計は、エージェント権限管理の汎用フレームワークとして他システムにも移植できる

## 前提知識

- **AIエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **CI/CD** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_91 Cortex Code CLI 実践カスタマイズガイド：Skills・SubAgents・Hooks・MCPによる拡張
- /deep_4624 .codexとは？OpenAI Codex CLIの設定フォルダとAGENTS.mdの使い分け
- /deep_4373 効果的なAIエージェントの作り方 — Anthropic Barry Zhangが語る3つの原則
- /deep_2880 Local-Splitter: コーディングエージェントのクラウドLLMトークン使用量を削減する7つの戦術の測定研究
- /deep_4661 Codex CLIを使った議事録→日報・週報・管理資料の自動生成アーキテクチャ

## 原文リンク

[OpenAI Codex徹底解説：CLI・Plan mode・Skills・MCP・Subagents・内部構造まで](https://zenn.dev/dokusy/articles/99af2fae0f1291)
