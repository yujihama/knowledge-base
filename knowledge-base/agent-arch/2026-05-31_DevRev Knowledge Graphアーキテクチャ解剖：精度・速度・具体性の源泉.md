---
title: "DevRev Knowledge Graphアーキテクチャ解剖：精度・速度・具体性の源泉"
url: "https://zenn.dev/knowledge_graph/articles/devrev-kg-architecture-deep-dive"
date: 2026-05-31
tags: [KnowledgeGraph, DuckDB, CDC, Text-to-SQL, OntologyAnnotation, RAG, RBAC, OpenSearch, Kafka, QueryRouter]
category: "agent-arch"
related: [4747, 5264, 1116, 5769, 6224]
memo: "[Zenn LLM] DevRev Knowledge Graphアーキテクチャ解剖：精度・速度・具体性の源泉"
processed_at: "2026-05-31T09:05:03.852573"
---

## 要約

DevRevのKnowledge Graphは、プレビルトのドメインオントロジー上に6つの特化型エンジンをCDCで同期し、AIが最適なクエリパスを自動選択する構成を採る。精度の鍵はOntology Annotationにある。通常のRAGシステムではLLMがテーブルスキーマからビジネスロジックを推測するため、「支払い顧客」の定義（forecast_category = 'closed_won' OR acv > 0 等）をハルシネーションしやすい。DevRevではフィールドごとにcommonly_used_filtersをスキーマに埋め込むことで、LLMが推測ではなく定義を参照してSQL条件に変換できる。数値の正確さはLLMの能力ではなくDuckDBのSQL実行結果に依存し、LLMは結果を「読み上げる」だけという設計が誤答を原理的に排除する。速度面では、MCPやFederatedアプローチがクエリのたびに外部APIを呼び出すのに対し、CDCで事前統合されたPre-replicatedアプローチを採る。DevRevの公開ベンチマークでは同一クエリに対してClaude（MCP経由）の約3.2Mトークン・9分に対し、DevRev Computerは157Kトークン・1.5分と、95%少ないトークンで5.5倍高速を達成している。SQLエンジンにはDuckDBを採用し、Apache ParquetカラムナーフォーマットとApache Arrowのzero-copy転送により数十億レコードでもsub-second応答を実現する。6エンジン（Search/SQL/Graph/TimeSeries/DataWarehouse/Workflow）の使い分けは転置インデックスとカラムナーストレージの物理的な不整合によるもので、クエリルーターが自動ルーティングする。CDCはMongoDB Change StreamをソースにKafka＋Protobufでファンアウトし、v1のモノリシックKafka Connect設計の問題を受けてv2では各サービスが自身のTransformerを所有する共有ライブラリ方式に全面改修されている。権限制御はクエリ前フィルタとして全パス（OpenSearch/DuckDB/Graph/Vector）に注入され、フィールドレベルRBACにより個人情報保護法対応の粒度も実現する。監査エージェント開発への示唆として、ビジネスロジックをスキーマに埋め込むSemantic Model設計は、監査手続きの判断基準をLLMに正確に伝える手法として直接応用可能。また権限のクエリ前フィルタリングはGRC用途での情報漏洩防止設計の参考になる。

## アイデア

- ビジネスロジックをcommonly_used_filtersとしてスキーマに埋め込むことでLLMの推測をゼロにするOntology Annotation設計は、監査手続きの条件定義にそのまま転用できる
- Pre-replicatedアプローチとFederatedアプローチの比較で、MCP経由でも「スキーマ探索コスト」は消えないという構造的な速度差の説明が明快
- CDC v1→v2の全面改修事例（Kafka Connectモノリス→サービスごとのTransformer所有）は、自前でKG基盤を構築する際の現実的な設計コストを示している

## 前提知識

- **CDC（Change Data Capture）** (TODO: 読むべき)
- **DuckDB / カラムナーDB** (TODO: 読むべき)
- **Text-to-SQL** → /deep_3173 LeGo-Code: モジュール式カリキュラム学習は複雑なコード生成を向上させるか？Text-to-SQLからの知見
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **RBAC** → /deep_5264 Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS

## 関連記事

- /deep_4747 源内（デジタル庁ガバメントAI）OSS版を技術解剖 — AWS/Azure/GCP 3クラウド対応の行政RAG基盤
- /deep_5264 Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_5769 長期LLMペルソナ一貫性のための異種時系列メモリガバナンスフレームワーク（ARPM）
- /deep_6224 金融サービスにおけるエージェントAIのデータ準備：品質・セキュリティ・アクセシビリティの三要件

## 原文リンク

[DevRev Knowledge Graphアーキテクチャ解剖：精度・速度・具体性の源泉](https://zenn.dev/knowledge_graph/articles/devrev-kg-architecture-deep-dive)
