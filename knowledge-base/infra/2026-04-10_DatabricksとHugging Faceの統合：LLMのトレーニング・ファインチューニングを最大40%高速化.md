---
title: "DatabricksとHugging Faceの統合：LLMのトレーニング・ファインチューニングを最大40%高速化"
url: "https://huggingface.co/blog/databricks-case-study"
date: 2026-04-10
tags: [Hugging Face, Apache Spark, Databricks, fine-tuning, Dataset, Dolly, MLflow, PyTorch, 分散学習]
category: "infra"
memo: "[HF Blog] Databricks ❤️ Hugging Face: up to 40% faster training and tuning of Large Language Models"
related: [819, 1575, 1275, 1532, 614]
processed_at: "2026-04-10T12:08:06.027263"
---

## 要約

2023年4月、DatabricksはHugging Faceのコードベースへの初の公式コントリビューションとして、Apache Spark DataframeをHugging Face Datasetに直接変換する`Dataset.from_spark()`関数を実装した。背景として、DatabricksはオープンソースLLM「Dolly」および商用利用可能なファインチューニング用データセット「databricks-dolly-15k」をHugging Face上で公開しており、その過程で大規模データの効率的な前処理が課題となっていた。

従来の方法では、SparkのDataframeをHugging Face Datasetとして利用するために、一度ParquetファイルとしてDisk（DBFS）に書き出し、再度読み込む必要があった。この方式では、16GBのデータセット処理に約22分を要し、Diskへの書き込み・読み込みのI/Oコストに加えて、Dataset読み込み時のデータ再マテリアライズによるリソース消費が問題だった。

新実装の`Dataset.from_spark(df)`を使用することで、同じ16GBのデータセットを12分（約45%短縮）で処理できるようになった。技術的には、SparkのデータをParquetを経由せず直接Hugging Face Datasetにマッピングし、HuggingFace Datasetsのメモリマッピングおよびスマートキャッシュ機構と組み合わせることで、I/Oオーバーヘッドを削減している。

DatabricksはさらにSparkを通じたStreaming対応を追加予定としており、データロードのさらなる高速化を図る。関連する動きとして、MLflowがTransformers・OpenAI・LangChainのサポートを追加、DatabricksがSpark上でのPyTorch分散トレーニングを簡易化する「PyTorch distributor for Spark」をリリースしており、大規模LLM開発のためのエコシステム整備を進めている。本統合は、Sparkのコスト効率・スケーラビリティとHugging Faceのパイプライン統合機能を組み合わせ、企業が自社データでAIモデルをドメイン特化ファインチューニングする際のデータ基盤として機能する。

## アイデア

- SparkとHugging Faceの直接統合により、大規模データ前処理からモデルファインチューニングパイプラインまでをシームレスに接続できる設計パターンが確立された
- Parquet経由の中間ファイルを排除することで処理時間を40%以上削減できた点は、データパイプラインにおけるI/Oボトルネック最小化の具体的事例として参考になる
- Databricksが自社LLM（Dolly）開発の知見をOSSコントリビューションとして還元する戦略は、エンタープライズAI企業のコミュニティ戦略モデルとして注目に値する
## 関連記事

- /deep_819 外科手術動画データセットの拡充手法：VLMの細粒度時空間理解のための SurgSTU-Pipeline
- /deep_1575 ビジョントランスフォーマー（ViT）をHugging Face Optimum Graphcoreで活用する詳細ガイド
- /deep_1275 PyTorch FSDPを使ったLlama 2 70Bのファインチューニング
- /deep_1532 PyTorch DDPからAccelerateとTrainerへ：分散学習を段階的にマスターする
- /deep_614 MLflowって何ができるの？機械学習ライフサイクルの全体像とツールの役割をサクッと解説

## 原文リンク

[DatabricksとHugging Faceの統合：LLMのトレーニング・ファインチューニングを最大40%高速化](https://huggingface.co/blog/databricks-case-study)
