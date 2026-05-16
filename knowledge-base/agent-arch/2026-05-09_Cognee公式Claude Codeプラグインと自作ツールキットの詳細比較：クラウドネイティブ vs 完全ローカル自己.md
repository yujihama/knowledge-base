---
title: "Cognee公式Claude Codeプラグインと自作ツールキットの詳細比較：クラウドネイティブ vs 完全ローカル自己完結"
url: "https://zenn.dev/japannomu/articles/20260503_cognee-official-vs-toolkit"
date: 2026-05-09
tags: [Cognee, MCP, Claude Code, グラフ記憶, Ollama, KuzuDB, LanceDB, FastEmbed, ローカルLLM, context injection]
category: "agent-arch"
related: [4612, 2404, 2950, 4177, 430]
memo: "[Zenn LLM] Cognee 公式 Claude Code プラグインと自作ツールキットを比較してみた"
processed_at: "2026-05-09T12:50:49.904610"
---

## 要約

Cogneeのグラフ記憶をClaude Codeに統合する2つのアプローチを詳細比較した記事。公式プラグイン（cognee-integrations/claude-code）は6つのライフサイクルhook（SessionStart/UserPromptSubmit/PostToolUse/Stop/PreCompact/SessionEnd）を持ち、クラウドLLM API（OpenAI/Anthropic）前提のクラウドネイティブ設計。一方、自作ツールキット（JapanNomu/tools）はOllamaローカルLLM（qwen2.5:14b、num_ctx=8192）+ KuzuDB + LanceDB + FastEmbedによる完全ローカル構成を採用。両者ともMCPツールはcognee-mcpのremember/recall/forget 3つを共通利用するが、差異は以下の6点。①ローカルLLM動作実証：公式はOllamaサポート未明記、自作はRTX 4060 Laptop GPU（VRAM 8GB）での実機検証済み。②大量ナレッジ取り込み：公式はslash commandによる1件ずつ登録のみ、自作はimport_to_graph.pyで任意ディレクトリ丸ごと取り込み可能。③大量投入時の安全機構：公式にはなし、自作はsplit_knowledge.py（H2見出し単位で分割）+ import_knowledge.py（cognify失敗時最大3回リトライ・--dry-run対応）を実装。④サンプル知識：公式は空、自作は4ファイル同梱（git pushルール/設計判断/開発教訓/よくあるエラー）でインストール直後に動作確認可能。⑤日本語ドキュメント：公式は英語のみ、自作はJapanNomu/tools-jaで完全日本語化。⑥MCP起動時の環境変数問題：claude mcp add経由でcognee-mcpを手動起動すると.envの変数が子プロセスに渡らずLLMAPIKeyNotSetError（Status 422）が発生するが、自作のstart_cognee_mcp.pyはos.environへの明示的読み込み後にexecvで継承する独自実装で回避。逆に公式が優位な点は、UserPromptSubmit hookでのcontext injection（関連情報の自動注入・3秒タイムアウト）、PostToolUseによるツール実行結果の自動キャプチャ、SessionEndでcognee.improve()を自動呼び出すグラフ同期、slash command 3つ（cognee-remember/cognee-search/cognee-sync）の提供。両者は競合ではなく補完関係で、完全ローカル・日本語環境・大量ナレッジ投入ニーズには自作、クラウド連携・自動セッション記憶・UI整備には公式が適合する。監査エージェント開発においては、過去のツール実行結果（PostToolUse）や設計判断をグラフ記憶として蓄積・再利用する仕組みが、エージェントの一貫性維持とコンテキスト継続に直接応用できる。

## アイデア

- SessionEnd hookでcognee.improve()を自動呼び出してセッションデータを永続グラフに反映する設計は、エージェントの長期記憶をセッション単位で段階的に構築するアーキテクチャパターンとして応用できる
- cognee-mcp子プロセス起動時に.envの環境変数がcwdの不一致で渡らない問題をos.environ + execvで解決する手法は、MCP統合全般で発生しうる共通の落とし穴への対処として汎用性が高い
- H2見出し単位でMarkdownを分割してcognifyに渡すchunk戦略は、ローカルLLMのPydantic検証失敗率を下げる実践的な工夫で、大規模RAGパイプライン構築時の信頼性向上に直結する

## 前提知識

- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **Cognee** → /deep_3943 AIエージェントのメモリ管理完全ガイド 2026 — Mem0 vs Zep vs Letta vs Cognee
- **KuzuDB / LanceDB** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Claude Code hooks** (TODO: 読むべき)

## 関連記事

- /deep_4612 Claude Code に Cognee グラフ記憶を追加する実用ツールキット
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話

## 原文リンク

[Cognee公式Claude Codeプラグインと自作ツールキットの詳細比較：クラウドネイティブ vs 完全ローカル自己完結](https://zenn.dev/japannomu/articles/20260503_cognee-official-vs-toolkit)
