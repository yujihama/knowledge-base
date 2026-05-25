---
title: "AI技術情報が多すぎるので、ObsidianをAIの外部記憶にして情報収集を自動化した"
url: "https://zenn.dev/en3/articles/obsidian-vault-mcp-ai-memory"
date: 2026-05-25
tags: [MCP, Obsidian, 外部記憶, Node.js, 知識管理, Claude Code, VaultIndex]
category: "agent-arch"
related: [430, 2688, 4520, 6126, 2404]
memo: "[Zenn LLM] AI技術情報が多すぎるので、ObsidianをAIの外部記憶にして情報収集を自動化した"
processed_at: "2026-05-25T09:01:36.611850"
---

## 要約

AI関連情報の爆発的増加に対処するため、ObsidianノートをAIが読み書きできるMCPサーバー（Vault MCP）として公開するNode.jsサーバーを実装した事例。

【課題】LLMの新モデルリリース、MCPの仕様更新、Zenn記事、Xの話題など情報量が多く、「同じ技術情報を毎回調べ直す」という非効率が発生していた。

【実装】GitHubリポジトリ `EN3Project/knowledge-nexus` として公開。`http://127.0.0.1:3100/mcp` でSSE形式のHTTPエンドポイントを提供し、MCP対応クライアント（Claude Code、Gemini CLI等）から利用可能。提供ツールは3つ：`vault_search(query)`（インデックスから関連ノートを検索）、`vault_read(path)`（ノート全文読み取り）、`vault_write(path, content)`（ノート書き込み）のみ。

【技術的特徴】データベースやベクトルストアを使わず、MarkdownファイルをNode.jsの`fs`モジュールで直接読み書きする。検索は全文検索ではなく、事前生成した`VaultIndex.md`（各ノートのパス・タグ・要約を集約した1ファイル）を使うことでトークン消費を抑制。iCloud/DropboxによるObsidian同期とそのまま共存できる。

【効果】調査時間が1〜2時間から20〜30分に短縮。調査結果が自動的に構造化ノートとして保存されるため、翌週以降は前回の続きから参照可能。複数のLLMを使い分けても同一の知識ベースを参照できる。ユーザーの役割が「情報を集める」から「判断する」に変化した。

【監査エージェント開発への示唆】MCPを用いてエージェントに永続的な外部記憶を持たせるパターンは、監査エージェントシステムにも直接応用可能。監査ナレッジ（法令解釈、過去の調査結果、リスク評価基準）をObsidianで管理し、LangGraphエージェントからMCP経由でアクセスする構成により、監査対話のたびに同じ前提知識を再調査するコストを削減できる。VaultIndex.mdによるトークン効率化は、コンテキスト長制限のある実務エージェントで特に有効。

## アイデア

- VaultIndex.mdによる2段階検索（インデックス検索→必要なノートのみ全文読み込み）でトークン消費を最小化する設計は、コンテキスト長制約のある実務エージェントに転用できる
- データベース・ベクトルストア不使用でMarkdownの直接読み書きのみにすることで、Obsidianの既存同期インフラ（iCloud/Dropbox）と競合せずに動作する最小実装を実現している
- HTTPエンドポイントをMCP仕様に準拠させることで、Claude/Gemini/その他MCPクライアントからLLM非依存で同一の知識ベースにアクセスできるマルチLLM対応アーキテクチャになっている

## 前提知識

- **MCP (Model Context Protocol)** → /deep_6357 LLMの拡張標準「MCP (Model Context Protocol)」入門：Pythonでカスタムサーバーを構築する
- **Obsidian Vault** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- **SSE (Server-Sent Events)** (TODO: 読むべき)
- **外部記憶 (External Memory)** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門

## 原文リンク

[AI技術情報が多すぎるので、ObsidianをAIの外部記憶にして情報収集を自動化した](https://zenn.dev/en3/articles/obsidian-vault-mcp-ai-memory)
