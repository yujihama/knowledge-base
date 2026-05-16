---
title: "ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門"
url: "https://zenn.dev/patakuti/articles/c70505fe275bc6"
date: 2026-04-20
tags: [RAG, MCP, pgvector, Claude Code, Ollama, LiteLLM, ローカルLLM, 埋め込み, PostgreSQL, 知識ベース]
category: "agent-arch"
related: [2257, 9, 1242, 430, 2209]
memo: "[Zenn LLM] ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門"
processed_at: "2026-04-20T12:14:09.171123"
---

## 要約

Local Knowledge RAG MCP ServerはローカルのMarkdown/テキストファイルをRAGで横断検索し、Claude CodeからMCP経由でレポートを自動生成するOSSツール。既存のDifyやRAGFlowに対して「Knowledge Base管理の煩雑さ」「引用箇所の確認しづらさ」「回答再利用の困難さ」という3つの課題を解消することを目的に設計されている。

アーキテクチャは4コンポーネント構成。①MCPサーバ本体（Claude CodeからのリクエストをRAGパイプラインに橋渡し）、②PostgreSQLのpgvector拡張をベクトルDBとして使用（HNSWインデックスによる近似最近傍探索）、③埋め込みプロバイダ（OpenAI API・LiteLLM経由のOpenAI互換・Ollamaの3種から選択可能）、④Index Manager（localhost:3456で起動するWeb UI）。

セットアップはDockerでpgvectorを起動し、リポジトリをcloneして`npm install && npm run build`、.envに`DATABASE_URL`と埋め込みプロバイダの設定を行い、`claude mcp add`でClaude Codeに登録する5ステップ。APIキー等の機密情報は.envから自動読み込みされるためMCP設定ファイルには記載不要。

日本語デモではWikipedia「日本のアニメ作品」8,863ファイル（約67MB）、英語デモではCShorten/ML-ArXiv-Papers 117,592ファイル（約463MB）で動作確認済み。レポートはbasic（文中引用埋め込み）とpaper（論文形式・番号参照）の2テンプレートを切り替え可能で、ユーザ定義テンプレートの追加も対応。引用箇所はファイルシステム内のファイルへのリンクとして保存され、markdown-proxyと組み合わせるとブラウザで引用箇所のハイライト表示が可能。

Git連携では共有Knowledge Baseをリポジトリにコミットしてチームでpullし、各自がIndex ManagerでUpdate Indexするだけでチーム共有のRAG環境が構築できる。対応ファイル形式はテキストとMarkdownのみで、PDFやWord文書は事前変換が必要。これはファイル内の特定箇所へリンクを張る機能要件と、多様なフォーマットの自動処理の困難さを理由とする設計上の判断。

監査エージェント開発への示唆：監査調書やナレッジをMarkdown化してローカルRAGの知識源とすることで、過去の監査手続き・指摘事項の意味検索と引用付きレポート自動生成が実現できる。Ollamaによる完全オフライン動作は機密情報を扱う監査環境での利用に適しており、pgvectorのワークスペース分離機能は監査クライアントごとの知識ベース分離にも応用可能。

## アイデア

- ファイルシステムとKnowledge Baseを一体化させることで、通常のファイル管理操作（作成・更新・削除）がそのままKnowledge Baseのメンテナンスになる設計思想が実用的
- レポート内の引用をファイルシステム上のファイルへのリンクとして保存することで、後からでも引用元の文脈を追跡可能にする点が既存RAGツールとの差別化になっている
- Gitをチーム共有のKnowledge Base管理基盤として使い、各自がローカルでRAGインデックスを構築するアーキテクチャはサーバ型RAGツール不要でチーム共有を実現する

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **pgvector / HNSW** (TODO: 読むべき)
- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **テキスト埋め込み (Embedding)** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境

## 関連記事

- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_1242 AI AgentメモリーOSS「MemPalace」徹底解説 — 記憶の宮殿アーキテクチャとベンチマーク論争
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2209 書類からのテキスト抽出精度をオープンソースのAIモデルで比較してみた

## 原文リンク

[ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門](https://zenn.dev/patakuti/articles/c70505fe275bc6)
