---
title: "Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】"
url: "https://zenn.dev/karaagedesu/articles/d51edc5a4d6ea3"
date: 2026-05-10
tags: [Ollama, ローカルLLM, RAG, MCP, ChromaDB, LangChain, ChatOllama, qwen2.5, nomic-embed-text, FastMCP, OpenAI互換API]
category: "infra"
related: [4177, 4325, 2404, 4043, 4612]
memo: "[Zenn LLM] Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】"
processed_at: "2026-05-10T12:45:05.461589"
---

## 要約

OllamaはLlama・Gemma・Qwenなど主要なオープンソースLLMをコマンド1行でローカル実行できるツール。GPUは必須ではなく、M1以降のMacBook上でも実用的な速度で動作する。2026年現在、個人開発のプロトタイピングフェーズでは「まずOllamaで無料検証 → 必要なら有料APIへ移行」が標準的なパターンになっている。

セットアップはbrewまたはcurlワンライナーで完了し、`ollama run qwen2.5:7b`でモデルを即起動できる。推奨モデルとしてはqwen2.5:7b（4.7GB・日本語対応）、qwen2.5:14b（9.0GB・高精度）、gemma3:4b（3.3GB・低スペック向け）、nomic-embed-text（274MB・RAG用埋め込み）が挙げられている。スペック目安は7BモデルでRAM 8GB以上、14BモデルでRAM 16GB以上。

OllamaはOpenAI互換のAPIエンドポイント（http://localhost:11434/v1）を提供しており、既存のOpenAI SDK利用コードのbase_urlを変えるだけでローカル動作に切り替えられる。LangChainとはChatOllamaクラスで接続でき、ストリーミング出力も標準サポート。

完全ローカルRAGはOllama（nomic-embed-textによるベクトル化）＋ChromaDBの組み合わせで実現できる。DirectoryLoaderでMarkdownドキュメントを読み込み、RecursiveCharacterTextSplitterでchunk_size=500にチャンク分割後、Chromaに永続化する構成。APIへのリクエストが一切発生しないため、社内機密ドキュメントや個人ノートへのRAG適用に有効。

MCP連携ではFastMCPを使ったMCPサーバーのLLMバックエンドとしてOllamaを使用できる。summarize_textやclassify_textといったツールをOllamaのOpenAI互換エンドポイントで実装し、Claude Desktopから呼び出すことで「Claudeがローカル別LLMに処理を投げる」構成が実現する。機密性の高い処理だけOllamaに委譲するハイブリッド運用が可能。

パフォーマンスチューニングとして、num_ctxパラメータでコンテキスト長を調整でき（デフォルト2048）、Mac M1/M2/M3はMetalを通じてGPUを自動利用する。Linux+NVIDIAはCUDAが自動検出される。並列リクエスト数はOLLAMA_NUM_PARALLEL環境変数で制御可能。

監査エージェント開発への示唆：社内の監査ドキュメントや内部統制手順書に対して完全ローカルRAGを構築することで、機密情報をクラウドに送出せずにLLMベースの検索・照合を実現できる。LangGraph＋ChatOllamaの組み合わせにより、既存エージェントアーキテクチャをAPIコストゼロで検証環境として動かすことも可能。

## アイデア

- OllamaのOpenAI互換エンドポイントにより、既存のOpenAI SDK資産をbase_urlの変更だけでローカルLLMに切り替えられる点は、ベンダー非依存の開発パターンとして汎用性が高い
- Claude Desktop → MCPサーバー → Ollamaというチェーン構成により、クラウドLLMがオーケストレーションを担い、機密処理だけローカルLLMに委譲するハイブリッドアーキテクチャが実現できる
- nomic-embed-text（274MB）による埋め込み生成をローカルで完結させることで、ベクトル化コストもゼロにした完全オフラインRAGパイプラインは、データガバナンス要件が厳しい企業環境で特に有効

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LangChain** → /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **ベクトルDB** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】

## 関連記事

- /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- /deep_4325 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第6回・完結）── ハルシネーションを4段ロケットで削る話
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入
- /deep_4612 Claude Code に Cognee グラフ記憶を追加する実用ツールキット

## 原文リンク

[Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】](https://zenn.dev/karaagedesu/articles/d51edc5a4d6ea3)
