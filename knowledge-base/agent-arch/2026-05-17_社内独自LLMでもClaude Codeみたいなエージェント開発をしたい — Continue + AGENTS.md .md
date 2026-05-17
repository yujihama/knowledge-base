---
title: "社内独自LLMでもClaude Codeみたいなエージェント開発をしたい — Continue + AGENTS.md という解"
url: "https://zenn.dev/dx_pm_product/articles/continue-agents-md-internal-llm"
date: 2026-05-17
tags: [Continue, AGENTS.md, 社内LLM, OpenAI互換API, Skills, VSCode, MCP, エージェント開発, コンテキスト最適化]
category: "agent-arch"
related: [91, 5465, 5027, 4183, 4617]
memo: "[Zenn LLM] 社内独自LLMでもClaude Codeみたいなエージェント開発をしたい — Continue + AGENTS.md という解"
processed_at: "2026-05-17T09:01:19.467257"
---

## 要約

外部AIサービス（ChatGPT/Claude/Cursor等）をセキュリティ・コンプライアンス上の理由で利用できない企業環境において、VS Code拡張のOSSであるContinueと社内OpenAI互換LLMプロキシを組み合わせることで、Claude Codeに近いエージェンティックな開発体験を再現する実践手法を解説した記事。

ContinueはVS Code/JetBrains向けのオープンソースAIアシスタントで、接続先LLMを任意のOpenAI互換エンドポイントに変更できる点が最大の特徴。Agentモードによるファイル編集・コマンド実行・MCPサーバー呼び出し、Rulesによるシステムメッセージ常時注入、Promptsによるスラッシュコマンドテンプレートを備える。設定は `.continue/agents/<名前>.yaml` にYAML形式で記述し、YAML 1.1のアンカー機能でapiBaseや認証ヘッダーの共通定義をDRYに管理する。モデルはchat/autocomplete/edit/embedのrolesで用途別に使い分けが可能。

本記事の核心はContinueに存在しないSkills機能の代替手法として「AGENTS.md + SKILL.md」構成を採用した点にある。ContinueはプロジェクトルートのAGENTS.mdを自動的にRuleとして読み込む（公式ドキュメント未記載の動作）。この性質を利用し、AGENTS.mdにスキル一覧と「タスク内容が該当する場合は対応するSKILL.mdを読み込んでから進めよ」というルールを表形式で定義。SKILL.mdは `.github/skills/<スキル名>/` 配下にフォルダごとに配置し、接続情報・認証方式・エンドポイント・セキュリティルール・サンプルコードを記述する。これにより「Wikiのページを確認して」などのリクエスト時にAIが自律的に対応するSKILL.mdを読み込み、記載されたAPIルール・セキュリティ制約に従って処理を進める動作を実現。Claude Code Skillsの「必要なタイミングで必要なコンテキストだけをロード」という概念をプロンプトエンジニアリングで擬似的に再現している。監査エージェント開発への示唆として、社内チケット管理システムや監視システムとのMCP連携においても同様のSKILL.md構成で接続情報とセキュリティ制約を一元管理できる点が注目される。

## アイデア

- AGENTS.mdをContinueが自動でRuleとして読み込む未文書の挙動を逆手に取り、Skills相当の動的コンテキストロードをプロンプトルールで擬似実装する発想
- SKILL.mdをフロントマター付きで `.github/skills/<名前>/` に分割配置することで、スキル追加をファイル1枚の追加だけで完結させる運用設計
- YAML 1.1アンカー機能でapiBase・認証ヘッダーを共通化しつつ、rolesでchat/autocomplete/edit/embedを用途別モデルに割り振る構成管理パターン

## 前提知識

- **Continue拡張** (TODO: 読むべき)
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **AGENTS.md** → /deep_8 LLMに「マジカルバナナ」式連想想起を実装したら会話が変わった
- **YAML アンカー** (TODO: 読むべき)

## 関連記事

- /deep_91 Cortex Code CLI 実践カスタマイズガイド：Skills・SubAgents・Hooks・MCPによる拡張
- /deep_5465 OpenAI Codex徹底解説：CLI・Plan mode・Skills・MCP・Subagents・内部構造まで
- /deep_5027 Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】
- /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- /deep_4617 AI agentへの良いspecの書き方 ― 5原則と6つの落とし穴

## 原文リンク

[社内独自LLMでもClaude Codeみたいなエージェント開発をしたい — Continue + AGENTS.md という解](https://zenn.dev/dx_pm_product/articles/continue-agents-md-internal-llm)
