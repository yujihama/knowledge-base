---
title: "コミット421件がLoRA学習データになるまで — TiDB/ChromaDB/Pineconeで実測したAIデータ基盤"
url: "https://zenn.dev/hakaru/articles/tidb-rag-vectordb-htap-benchmark"
date: 2026-05-21
tags: [TiDB, ChromaDB, Pinecone, RAG, ベクトルDB, HTAP, LoRA, bge-large, ベンチマーク]
category: "infra"
related: [5650, 4477, 5645, 2794, 2103]
memo: "[Zenn LLM] コミット 421 件が LoRA 学習データになるまで — TiDB/ChromaDB/Pinecone で実測した AI データ基盤"
processed_at: "2026-05-21T09:06:56.866020"
---

## 要約

個人開発iOSアプリ（M2DX/1Take）の実コミット421件を対象に、RAGパイプラインで使用するベクトルDBとしてTiDB Serverless・ChromaDB・Pinecone Serverlessの3種を実測比較した報告。git diffをbge-large（1024次元）でベクトル化し、類似diff検索でllama3.3:70bのコードレビューを補強するパイプラインを構成。DBの性能差を正確に測るため、embeddingをキャッシュしてDB呼び出しのみを計測する設計を採用した。

Ingestスループット（70件）はChromaDB 2.6件/秒、TiDB 0.9件/秒、Pinecone 0.6件/秒。ローカルのChromaDBが圧倒的に速く、クラウド同士ではTiDBがPineconeの約1.5倍。検索レイテンシ（p50）はChromaDB 42ms、TiDB 1,157ms、Pinecone 1,623ms。PineconeはStarter planがus-east-1固定のため遅延が大きい。Top-K一致率はTiDB基準でChromaDB 99%、Pinecone 98%と、全DB同等の検索品質を示した。

最も注目すべきはHTAP（Hybrid Transactional/Analytical Processing）の検証。ChromaDBはベクトル専用のためAVG/GROUP BY等の分析クエリが書けず、実運用ではSQLite+ChromaDBの2システム構成が必要になる。一方TiDBはSQLとベクトル検索を同一DBで完結できる。検証ではINSERT負荷を0→10→30件/分と変化させながらOLAPクエリのレイテンシを計測。TiDBは30件/分INSERT中もp50 14ms台で安定（劣化なし）。SQLiteは10件/分でライトロック競合により3.5ms→5.0msに増加した。TiDBの行ストア（TiKV）と列ストア（TiFlash）の内部分離が、書き込みと分析の相互干渉を防いでいることが数字で確認された。

LoRAデータ収集パイプラインでは「書きながら集計する」ユースケースが頻出するため、TiDBの1システム完結は運用コストと整合性リスクの両面で有効。監査エージェント開発においても、コードレビューログのベクトル検索と集計分析（モデル世代比較・スコアトレンド追跡）を単一DBで扱えるアーキテクチャは、パイプライン管理の簡素化と不整合リスク低減に直結する。プロトタイプはChromaDB一択、クラウド本番・集計も必要な場合はTiDB、という使い分けが結論。

## アイデア

- embeddingキャッシュをDB呼び出しと分離してベンチマークする設計により、ネットワーク遅延とDB性能を独立して評価できる点
- TiDBのHTAP（TiKV行ストア＋TiFlash列ストア）がINSERT負荷下でもOLAPレイテンシを劣化させない構造的理由が実測で裏付けられた点
- ベクトル検索品質（Top-K一致率98〜99%）はDB選択に依存しないため、DB選定基準を性能・運用コスト・HTAP能力にシフトできるという判断軸の整理

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **ベクトルDB** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **HTAP** (TODO: 読むべき)
- **LoRA** → /deep_20 Mellea 0.4.0 と Granite Libraries リリース：構造化・検証可能・安全性対応AIワークフローの新展開
- **HNSW** → /deep_93 RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）

## 関連記事

- /deep_5650 ベクトルDB比較（TiDB/Chroma/Pinecone）：ローカルLLMコードレビューRAGへの適用実験
- /deep_4477 Fine-tuningとRAGはどちらを選ぶべきか：実務で判断するための5つの軸
- /deep_5645 AIエージェントの長期記憶問題を解決する次世代データ基盤アーキテクチャ：TiDB Serverlessによる統合ベクトルDB設計
- /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針
- /deep_2103 製造業RAG運用編：監査ログ + イベント駆動再インデックスを実装する

## 原文リンク

[コミット421件がLoRA学習データになるまで — TiDB/ChromaDB/Pineconeで実測したAIデータ基盤](https://zenn.dev/hakaru/articles/tidb-rag-vectordb-htap-benchmark)
