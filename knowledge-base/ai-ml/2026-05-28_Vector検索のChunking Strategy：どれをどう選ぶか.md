---
title: "Vector検索のChunking Strategy：どれをどう選ぶか"
url: "https://zenn.dev/yasunami_daichi/articles/vector-chunking-strategy"
date: 2026-05-28
tags: [RAG, chunking, embedding, vector-search, RecursiveCharacterTextSplitter, LangChain, Amazon-Bedrock, Contextual-Retrieval]
category: "ai-ml"
related: [6356, 5761, 5435, 2518, 2901]
memo: "[Zenn LLM] Vector 検索の chunking strategy、どれをどう選ぶか"
processed_at: "2026-05-28T09:00:36.598364"
---

## 要約

RAGシステムにおけるchunkingは、embeddingモデルやvector DBの選択より上流にある根本的な設計要素。chunking戦略が誤っていると、検索エラーも例外もなく「それっぽい間違った答え」が返り続けるため、気づきにくく後から効いてくる。

主要戦略は以下の通り。①Fixed-size：512トークン単位で機械的に分割。オーバーラップで境界の文脈消失を緩和するが、意味境界を無視するためPoC向け。②Recursive：`RecursiveCharacterTextSplitter`（LangChain）に代表される、段落→文→単語の優先順位で再帰的に分割する手法。chunk_size=512、chunk_overlap=64が初期値の定番。③構造認識（Document-structure-aware）：Markdownの見出し、HTMLタグ、コードの関数定義で切る。`MarkdownHeaderTextSplitter`で見出し階層をmetadataに保持することで、後段のフィルタ検索にも活用可能。④Semantic：隣接文をembeddingして意味類似度が落ちる地点で分割。FAQでは「質問」と「回答」の意味が異なるためQ&Aを割ってしまう逆説的な失敗がある。⑤Hierarchical（親子chunk）：Amazon Bedrockが公式提供。子chunkで高精度検索し、ヒット時は親chunkをLLMに渡すことで精度と文脈量を両立。⑥Agentic：LLM自身に分割判断をさせる。精度は最高だがコストとレイテンシが桁違いのため少量・高価値ドキュメント専用。

データ構造による選択指針：構造が強いMarkdown/コード/PDFは「構造認識chunking」だけで精度が大幅改善。FAQ・用語集・商品マスタは「1レコード=1chunk（割らない）」のレコード単位が最適で、splitterを通すこと自体が誤り。一般的なドキュメントは「Recursive + 10〜15%オーバーラップ」がデフォルト選択。

補助テクニックとして、Contextual Retrieval（各chunkに文脈を前置きしてから埋め込む手法）と親子取得（small-to-big：小さく検索して大きく返す）がchunking戦略と組み合わせると特に効果的。

監査エージェント開発への示唆：監査調書・内部統制文書・規程集はMarkdown変換後の構造認識chunkingが適合度高い。FAQや用語集形式の内部ルールはレコード単位で管理することで、検索精度の根本的な安定性を確保できる。LangGraphベースのRAGパイプライン構築時は、RecursiveCharacterTextSplitterのseparatorsに日本語区切り文字（「。」「、」）を追加する設定が必要。

## アイデア

- SemanticChunkingがFAQで逆効果になる逆説：意味類似度で切ることでQ&Aペアが分断され、質問文にヒットしても回答がない断片chunkが生成される。データ構造とアルゴリズムのミスマッチが精度劣化の原因になる典型例
- 「割らない」という戦略の重要性：FAQ・用語集などレコード単位のデータは、splitterを通さず1レコード=1chunkとして扱うことが最適。精度問題の原因が「切り方」ではなく「そもそも切るべきでない」という設計判断にある
- Hierarchical chunkingによる精度・文脈量のトレードオフ解消：子chunkで高精度ベクトル検索し、LLMには親chunkを渡すことで、chunk sizeのジレンマを2階層構造で構造的に回避するAmazon Bedrockのマネージド設計

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **embedding** → /deep_33 2時間ごとに自分を再構築する — 自律AIエージェントの記憶アーキテクチャ
- **vector DB** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- **LangChain TextSplitter** (TODO: 読むべき)
- **トークン長制約** (TODO: 読むべき)

## 関連記事

- /deep_6356 RAGはLong Contextに駆逐されるのか？2026年の設計判断
- /deep_5761 論文メモ：BERTからEmbeddingを整理する
- /deep_5435 検索を超えて：コード検索のためのマルチタスクベンチマークとモデル（CoREB）
- /deep_2518 制約の多い公共部門環境でAIを実用化する：SLMという現実解
- /deep_2901 制約の多い公共部門環境でAIを実用化する：SLMという現実解

## 原文リンク

[Vector検索のChunking Strategy：どれをどう選ぶか](https://zenn.dev/yasunami_daichi/articles/vector-chunking-strategy)
