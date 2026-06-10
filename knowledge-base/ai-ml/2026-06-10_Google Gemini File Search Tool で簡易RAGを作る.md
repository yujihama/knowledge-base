---
title: "Google Gemini File Search Tool で簡易RAGを作る"
url: "https://zenn.dev/khisa/articles/9e3850ee4b03c9"
date: 2026-06-10
tags: [RAG, Gemini API, File Search Tool, Embedding, gemini-embedding-2, ベクトル検索, Python, マルチモーダル]
category: "ai-ml"
related: [7286, 5261, 5394, 1787, 5761]
memo: "[Zenn LLM] Google Gemini File Search Tool で簡易RAGを作る"
processed_at: "2026-06-10T09:06:20.090953"
---

## 要約

Google Gemini APIが提供するFile Search Toolを使い、ベクトルDBの構築・管理を一切不要にした簡易RAGの実装方法を解説した記事。従来のRAG構築では、PDFからのテキスト抽出・チャンク分割・Embedding生成・ベクトルDB格納という複数ステップが必要だったが、File Search Toolではファイルをストア（File Search Store）にアップロードするだけで、これらすべてがAPI側で自動処理される。

Embeddingモデルにはマルチモーダル対応の`gemini-embedding-2`を使用し、PDF内の図表を含む検索も可能。チャンク設定は`max_tokens_per_chunk`（デフォルト400トークン）と`max_overlap_tokens`（デフォルト40トークン）のみ指定可能で、ページ・セクション単位の分割など細かなカスタマイズはできない点が現時点の最大の制約。

コスト面では、File Search Storeの保存料・検索時のクエリEmbeddingが無料で、課金対象はアップロード時のEmbedding生成コストと回答生成時のLLMトークンコストのみ。ストア容量はTier 1で10GB（有料）。ストアサイズは元データの約3倍が目安。

利用方法は`generate_content`の`tools`引数に`FileSearch`オブジェクトを渡すだけで、LLMが自律的にナレッジ検索の要否を判断して回答を生成する。レスポンスには`grounding_metadata`として参照チャンクの情報も含まれ、回答の根拠を追跡可能。

監査エージェント開発への示唆として、PoC段階で社内規程・監査基準書・過去調書などのPDFを手軽にRAG化する手段として有効。ただしチャンキング戦略のカスタマイズ性が低いため、本番運用では精度要件に応じて自前RAGへの移行判断が必要。

## アイデア

- ベクトルDBのホスティングコストをゼロにしつつRAGを構築できる点で、PoC・小規模用途のコスト構造を根本から変える可能性がある
- マルチモーダルEmbedding（gemini-embedding-2）により、PDF内の図表・画像も検索対象にできる点は、図表が多い技術文書や財務報告書の検索に有効
- grounding_metadataで参照チャンクを取得できるため、回答の根拠トレーサビリティが確保でき、監査・コンプライアンス用途での説明責任対応に使いやすい

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Embedding** → /deep_33 2時間ごとに自分を再構築する — 自律AIエージェントの記憶アーキテクチャ
- **ベクトルDB** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **Gemini API** → /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- **チャンク分割** → /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話

## 関連記事

- /deep_7286 誰も教えてくれないベクトル検索RAGの真実
- /deep_5261 『三国志』を使って最小構成のRAGを実装してみた
- /deep_5394 semantic chunkingが負けていた — RAGチャンク戦略を論文ベースで整理した
- /deep_1787 LLMの2大カテゴリ：質疑応答モデルとEmbeddingモデルの違い
- /deep_5761 論文メモ：BERTからEmbeddingを整理する

## 原文リンク

[Google Gemini File Search Tool で簡易RAGを作る](https://zenn.dev/khisa/articles/9e3850ee4b03c9)
