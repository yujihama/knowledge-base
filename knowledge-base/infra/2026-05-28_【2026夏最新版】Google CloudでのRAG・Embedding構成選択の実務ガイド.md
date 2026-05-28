---
title: "【2026夏最新版】Google CloudでのRAG・Embedding構成選択の実務ガイド"
url: "https://zenn.dev/fp16/articles/c3a080a68b3b59"
date: 2026-05-28
tags: [RAG, pgvector, AlloyDB, Cloud SQL, ScaNN, Vertex AI Vector Search, Agent Search, Reranking, gemini-embedding, Google Cloud]
category: "infra"
related: [5435, 6353, 2404, 93, 1116]
memo: "[Zenn LLM] 【2026・夏最新版】皆様にGoogle CloudでのRAG・Embeddingの最強を、お伝えしたかった。"
processed_at: "2026-05-28T09:06:54.172272"
---

## 要約

株式会社FP16による、Google Cloud上でRAGを構築する際のベクトルDB・インフラ選択を実務視点で整理した記事。2026-05-26時点の公式情報に基づく。

主な選択肢として6構成を比較している。①Cloud SQL + pgvector：小〜中規模RAGの出発点。PostgreSQL上にchunk・metadata・embeddingを一元管理でき、HNSWインデックスで検索可能。安価で理解しやすい反面、大規模vectorや高QPSになるとチューニングが必要。②AlloyDB + AlloyDB AI / ScaNN：PostgreSQL互換を保ちながら性能を引き上げる選択肢。ScaNN（Google製大規模近似最近傍探索）を利用でき、高QPS・低レイテンシ要件に対応しやすい。固定費はCloud SQLより高め。③Agent Search（旧Vertex AI Search）：検索・生成回答・managed indexingを丸ごと委託できるが、query課金が増えると高コストになりやすい。④RAG Engine：自作とmanagedの中間で、裏側のDB/Spannerコスト把握が必要。⑤Vertex AI Vector Search / Agent Retrieval：高QPS・低レイテンシ・大規模vector servingに特化。Classic版はsource DBとの同期設計が必要で、Vector Search 2.0 / Agent Retrievalではpayload統合管理が進化。⑥BigQuery vector search：分析系RAGや評価基盤向き。

記事の核心は「後から構成変更したとき何を作り直すか」という実務的論点。Cloud SQLからAlloyDBへの移行はDB migrationとindex再作成が必要だが、embeddingモデル名・バージョン・次元数・正規化フラグ・距離メトリクス・ソーステキストハッシュ・chunkバージョン等をDBに保存しておけば、embedding再生成は不要。ただしgemini-embedding-001からgemini-embedding-2への移行は空間非互換のため全件再embeddingが必須。

FAQ・PDFマニュアル・スライドを含む業務マニュアルcorpusで18問ベンチマークを実施。A/B/Cの3構成でSource Hit@3は全て100%達成。B・CはMRR 1.000だが、CはP95レイテンシが33.375秒まで悪化。Rerankingの効果と引き換えに速度が犠牲になることが示された。

推奨デフォルトは「まずCloud SQL + pgvectorで構築し、query量と評価を見てAlloyDBに逃げられる設計を維持する」こと。chunk tableのembeddingメタデータ設計が移行コストを左右する。監査AIのような業務RAGでは、chunking・評価・Rerank・DB設計を細かく制御したい場合、Agent Searchより Cloud SQL/AlloyDB系の方が設計の説明責任を果たしやすい。

## アイデア

- embeddingの「作り直し不要条件」を明示化したこと——モデル名・バージョン・次元数・正規化フラグ・距離メトリクス・chunkバージョンをDBカラムとして保存することで、DB移行とembedding再生成を切り離せるという設計パターンは監査エージェントのRAG基盤設計にそのまま応用できる
- Cloud SQL→AlloyDB移行をDB migrationとして捉え直すアプローチ——「RAGの作り直し」ではなくPostgreSQL→PostgreSQLの移行として扱うことで、提案時のリスク説明が具体的になり、将来の技術的負債を見積もりやすくなる
- P95レイテンシ33.375秒という実測値がRerankingの代償として示されていること——精度（MRR 1.000）とレイテンシのトレードオフを同一benchmarkで可視化した設計が実務的で、エージェントシステムのSLA設計に直接使える指標

## 前提知識

- **pgvector / HNSW** (TODO: 読むべき)
- **近似最近傍探索 (ANN)** (TODO: 読むべき)
- **Embedding次元・正規化** (TODO: 読むべき)
- **RAGパイプライン** → /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針
- **Reranking** → /deep_5435 検索を超えて：コード検索のためのマルチタスクベンチマークとモデル（CoREB）

## 関連記事

- /deep_5435 検索を超えて：コード検索のためのマルチタスクベンチマークとモデル（CoREB）
- /deep_6353 同じAIが感情モードを変えると同じ知識を全く別の使い方をした ― Soul-Twin 感情モード×座談会4回比較実験
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_93 RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング

## 原文リンク

[【2026夏最新版】Google CloudでのRAG・Embedding構成選択の実務ガイド](https://zenn.dev/fp16/articles/c3a080a68b3b59)
