---
title: "Amazon SageMaker向けHugging Face埋め込みコンテナの正式リリース"
url: "https://huggingface.co/blog/sagemaker-huggingface-embedding"
date: 2026-04-09
tags: [SageMaker, TEI, embedding, RAG, Snowflake-Arctic-Embed, HuggingFace, BERT]
category: "infra"
memo: "[HF Blog] Introducing the Hugging Face Embedding Container for Amazon SageMaker"
processed_at: "2026-04-09T09:22:01.271101"
---

## 要約

HuggingFaceとAWSが共同で、Amazon SageMaker上で埋め込みモデルを本番運用するための専用コンテナ「Hugging Face Embedding Container」を正式リリースした。このコンテナはText Embedding Inference（TEI）を基盤としており、Flash Attention・Candle・cuBLASLtによる推論最適化、トークンベースの動的バッチ処理、Safetensors形式の重みローディング、Open TelemetryによるOpenな分散トレーシング、Prometheusメトリクスなどのプロダクション対応機能を備える。モデルグラフのコンパイル不要で起動時間が短く、CPUとGPUで別々のイメージが提供されるため、インスタンスタイプに応じて適切なものを選択する必要がある。対応アーキテクチャはBERT/CamemBERT・RoBERTa・XLM-RoBERTa・NomicBERT・JinaBERTで、BAAI/bge-large-en-v1.5やSnowflake/snowflake-arctic-embed-m-v1.5などの主要モデルをサポートする。デプロイ手順はSageMaker Python SDKを使用し、get_huggingface_llm_image_uriでコンテナURIを取得してHuggingFaceModelクラスに渡すだけで完結する。デモでは、MTEBリーダーボード上位のSnowflake Arctic Embed M v1.5をml.g5.xlargeインスタンス（GPU）またはml.c6i.2xlarge（CPU, $0.204/時）にデプロイし、256トークン入力・10並列スレッドで3,900リクエスト（合計約100万トークン）の負荷試験を実施。欧州からus-east-1へのネットワーク遅延込みでのスループット・平均レイテンシが計測されている。RAGアプリケーションの埋め込みエンドポイントをマネージドかつスケーラブルに構築する用途に直接対応した構成となっている。

## アイデア

- TEIのトークンベース動的バッチ処理により、入力長が異なるリクエストを効率的にまとめて処理でき、RAGパイプラインのスループットを大幅に向上させられる点
- CPU/GPU両対応のコンテナを単一APIで切り替え可能な設計により、コスト最適化（開発時はCPU、本番はGPU）を柔軟に行える点
- Open Telemetry＋Prometheusをネイティブサポートすることで、埋め込みエンドポイントのレイテンシ・スループットを既存の監視スタックに統合しやすい点

## Yujiの取り組みへの示唆

監査エージェントシステムでRAGを活用する場合、監査証跡・規程文書・過去の指摘事項などの埋め込みエンドポイントをSageMaker上でマネージド運用できるため、インフラ管理コストを削減しつつ本番品質の埋め込み基盤を迅速に構築できる。LangGraphで構築した監査エージェントのRetrieverノードから、このSageMakerエンドポイントをAPIコールするだけで接続可能であり、エージェントのアーキテクチャ変更を最小限に抑えられる点も実用的。

## 原文リンク

[Amazon SageMaker向けHugging Face埋め込みコンテナの正式リリース](https://huggingface.co/blog/sagemaker-huggingface-embedding)
