---
title: "ローカルLLMで「PoC止まり」にしない業務AIエージェント ― MCP＋RAG評価まで一気通貫"
url: "https://zenn.dev/th1khse/articles/e5b1d66f0c36fd"
date: 2026-06-04
tags: [LangGraph, MCP, RAG, Ollama, Ragas, ReAct, qwen2.5, LLM-as-judge, FastMCP, ローカルLLM]
category: "agent-arch"
related: [5027, 4177, 2404, 5264, 5472]
memo: "[Zenn LLM] ローカルLLMで“PoC止まり”にしない業務AIエージェント ― MCP＋RAG評価まで一気通貫"
processed_at: "2026-06-04T09:20:10.255229"
---

## 要約

生成AIがPoC（概念実証）で止まる主因として「精度を数値化できない」「コストが読めない」「運用・改善サイクルがない」の3点を挙げ、これらを最初から設計に組み込んだローカル動作の業務AIエージェントの実装例を示した記事。スタックはLangGraph（ReActエージェント）、Ollama（qwen2.5:7b＋nomic-embed-text）、langchain-mcp-adapters、Ragasで構成される。

アーキテクチャは2つのツールを持つ：①社内ドキュメントをInMemoryVectorStoreでインデックスしたRAG検索ツール（search_knowledge_base）、②FastMCPで実装したMCPサーバー経由の業務データ照会ツール（注文ステータス・顧客プラン）。MCPをstdioトランスポートで切り離すことで、将来的にDB/SaaS APIへの認可付きアクセスへの置換が容易になる設計。LLMプロバイダーは環境変数1行でollama/openai/geminiを切替可能とし、ベンダーロックインを回避している。

実装上の4つのハマりどころが具体的に記載されている。①小型ローカルモデルは曖昧な指示だとツールを呼ばず即答するため、システムプロンプトに対象トピックと対応ツールを明示列挙することで安定化。②LangGraphのバージョンによってcreate_react_agentのprompt=引数が反映されないため、system messageを入力メッセージとして渡す方法が確実。③qwen2.5:7bはtool呼び出しをテキストとして本文に漏らすことがあり、qwen2.5:14b以上への切替で改善。④依存関係の競合（langchain 1.x × ragas 0.4 × Python 3.14でimportエラー）はPython 3.12＋安定版ピン留め＋uv.lockコミットで解決。

RAG評価はRagasを用いてfaithfulness/answer_relevancy/context_recall/context_precisionの4指標を計測。ローカルqwen2.5:7bをジャッジにした実測値はfaithfulness 0.78、context_recall 1.00、context_precision 0.67、answer_relevancy 0.41。answer_relevancyの異常な低さはジャッジモデルの能力不足によるもので、JUDGE_PROVIDER=openaiに切替ることでエージェント本体はローカルのまま評価精度を担保できる設計になっている。「測る仕組みの信頼性を設計する」点をPoCと本番の分水嶺として強調している点は、監査エージェント開発においてLLM-as-judgeの品質保証設計に直結する示唆を持つ。

## アイデア

- エージェント本体はローカルLLMで動かしつつ、評価ジャッジだけ強力なモデル（GPT等）に切り替える分離設計により、データの外部流出ゼロを維持しながら評価精度を担保できる
- MCPサーバーをstdioトランスポートで独立プロセスとして切り出すことで、業務データアクセス層を認可・セキュリティ要件に応じて差し替え可能な疎結合アーキテクチャを実現している
- 小型ローカルモデルのツール呼び出し不安定性（曖昧指示での無視、テキストへの漏洩）に対してシステムプロンプト設計とモデルサイズ選択で対処する実践的なノウハウが蓄積されている

## 前提知識

- **LangGraph ReAct** (TODO: 読むべき)
- **MCP (Model Context Protocol)** → /deep_6357 LLMの拡張標準「MCP (Model Context Protocol)」入門：Pythonでカスタムサーバーを構築する
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Ragas評価指標** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境

## 関連記事

- /deep_5027 Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】
- /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_5264 Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS
- /deep_5472 LLMエンジニアとして最初の3ヶ月に何をするべきか：ロードマップと優先順位

## 原文リンク

[ローカルLLMで「PoC止まり」にしない業務AIエージェント ― MCP＋RAG評価まで一気通貫](https://zenn.dev/th1khse/articles/e5b1d66f0c36fd)
