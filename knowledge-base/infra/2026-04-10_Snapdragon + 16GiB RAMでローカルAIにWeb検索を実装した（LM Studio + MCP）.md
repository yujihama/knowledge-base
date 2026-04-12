---
title: "Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）"
url: "https://zenn.dev/tos_kamiya/articles/3c164da01a89b5"
date: 2026-04-10
tags: [LM Studio, MCP, Gemma4, ローカルLLM, ARM64, Snapdragon, web-search-mcp, Node.js, GGUF]
category: "infra"
memo: "[Zenn LLM] Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）"
processed_at: "2026-04-10T12:26:43.235103"
---

## 要約

ARM64アーキテクチャ（Snapdragon X 12-core X1E80100）・RAM 16GiBのWindows 11ノートPC上で、Gemma 4 E4BモデルとMCP（Model Context Protocol）を組み合わせたWeb検索付きローカルAIチャットを構築した事例。LM StudioでGemma 4を実行し、LM Studio内蔵のMCPクライアントを経由してweb-search-mcpサーバを呼び出す構成。構成要素は①LM Studio（LLM実行環境）、②MCPクライアント（LM Studio内蔵）、③web-search-MCPサーバ（Node.js製、Playwrightによるブラウザ操作でWeb検索を実現）の3層。セットアップ手順は、LM StudioのARM64版インストール→gemma-4-E4B-it-GGUFモデルのダウンロード→Node.js（v24.14.1）とGitのインストール→web-search-mcpをgit cloneしてnpm install・npx playwright install・npm run buildでビルド→LM Studioのmcp.jsonにサーバのdist/index.jsパスを登録して有効化、という流れ。公式手順のzipダウンロード方式ではビルドが止まるためgit cloneが必須という注意点あり。モデルサイズはGemma 4 E4B（Effective 4Billion相当）でGGUF量子化版を使用しており、16GiB RAMでも快適に動作することを確認。Web検索ツールと組み合わせることで、軽量モデル単体では困難なリアルタイム情報が必要なタスクへの対応が可能になる点を実証している。MCPはLLMから外部ツールを呼び出す標準プロトコルであり、LM Studio側がMCPクライアントを内蔵しているため、サーバ側の実装さえあれば任意のツールを追加できる拡張性がある。

## アイデア

- MCPクライアントをLM Studioが内蔵しているため、サーバ実装だけで任意のツール（DB検索、社内API呼び出し等）をローカルLLMに追加できるアーキテクチャの汎用性
- Gemma 4 E4B（実効4B規模）がARM64・16GiBで快適動作するという事実は、ローカル推論の最低ハードウェア要件が大幅に下がっていることを示す
- Playwright（ヘッドレスブラウザ）をMCPサーバ内で使うことで、JavaScript動的レンダリングが必要なサイトも含めたWeb検索を実現している設計
## 関連記事

- /deep_1420 秘匿環境で使うAI議事録の構成を考える - パイプライン型とLLM完結型の検証
- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）
- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_710 OlympicCoder をローカルで使う方法：LM Studio + VS Code による構築ガイド
- /deep_1242 AI AgentメモリーOSS「MemPalace」徹底解説 — 記憶の宮殿アーキテクチャとベンチマーク論争

## 原文リンク

[Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）](https://zenn.dev/tos_kamiya/articles/3c164da01a89b5)
