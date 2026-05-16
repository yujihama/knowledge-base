---
title: "Amazon SageMakerとHugging Faceのパートナーシップ：NLPモデルのトレーニングと推論を簡略化"
url: "https://huggingface.co/blog/the-partnership-amazon-sagemaker-and-hugging-face"
date: 2026-04-14
tags: [SageMaker, HuggingFace, DLC, Transformers, 分散トレーニング, PyTorch, TensorFlow, NLP, AWS, 推論デプロイ]
category: "infra"
related: [1446, 26, 1529, 1760, 1709]
memo: "[HF Blog] The Partnership: Amazon SageMaker and Hugging Face"
processed_at: "2026-04-14T12:50:29.826861"
---

## 要約

2021年3月、Hugging FaceとAmazonはNLPモデルの本番活用を加速するための戦略的パートナーシップを発表した。主な成果物は、Amazon SageMaker向けHugging Face Deep Learning Containers（DLCs）と、SageMaker Python SDKへのHugging Face専用拡張機能の追加である。

Hugging Face DLCsはTensorFlowおよびPyTorchの両方に対応し、シングルGPU・シングルノードマルチGPU・マルチノードクラスター構成をサポートする。SageMakerのDistributed Data Parallel LibraryおよびDistributed Model Parallel Libraryと完全統合されており、Amazon EC2の最新世代インスタンスを活用して大規模モデルの分散トレーニングが可能になった。

同年7月8日には推論・デプロイ機能も拡張され、Hugging Face Model Hubに公開されている10,000以上のTransformersモデルをSageMakerエンドポイントとして1コマンドでデプロイできるようになった。S3に保存したカスタムモデルからのデプロイも同様にサポートされる。

トレーニングのワークフローとしては、HuggingFace Estimatorオブジェクトを使用してhyperparametersを指定し、SageMaker TrainingJobを起動する形式をとる。training scriptはargparseでハイパーパラメータを受け取り、transformers/datasetsライブラリを用いてTrainerを構成・実行する標準的なPythonスクリプトとして記述できる。データはAmazon S3経由で受け渡し、モデルはトレーニング終了後に自動的にS3へ保存される。

SageMakerのAutomatic Model Tuning機能と組み合わせることでハイパーパラメータ最適化も自動化でき、SageMaker Studio IDEでの実験管理・比較も可能。実験セットアップにかかる時間を「数日から数分」に短縮することを目標としている。

監査エージェント開発への示唆：SageMakerのTrainingJobはIAMロールベースのアクセス制御と完全統合されており、監査ログやモデル学習の証跡管理が容易。分散トレーニング基盤を活用してLangGraphベースの監査エージェント評価用モデルをスケーラブルにfine-tuningする際のインフラ選択肢として有力。

## アイデア

- HuggingFace EstimatorというSageMaker SDK拡張により、transformers/datasetsライブラリを使った既存のトレーニングスクリプトをほぼ変更なしにクラウドスケールで実行できる設計思想
- SageMakerのDistributed Model Parallel Libraryと統合することで、単一GPUに収まらない大規模Transformerモデル（BART/T5等）のSummarizationタスクを複数ノードに分割してトレーニングできる点
- Model Hubの10,000以上のモデルを直接SageMakerエンドポイントとしてデプロイできる仕組みにより、fine-tuningなしのゼロショット推論APIを最小コードで本番環境に展開できる点

## 前提知識

- **Amazon SageMaker** → /deep_1016 Amazon SageMaker向けHugging Face埋め込みコンテナの正式リリース
- **Hugging Face Transformers** → /deep_1573 Hugging Face TransformersとHabana GaudiでBERTをスクラッチから事前学習する
- **Deep Learning Container** (TODO: 読むべき)
- **分散トレーニング** (TODO: 読むべき)
- **IAMロール** (TODO: 読むべき)

## 関連記事

- /deep_1446 Hugging FaceとAWSが提携：AIの民主化に向けた戦略的パートナーシップ
- /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1709 機械学習エキスパート・インタビュー：Lewis Tunstall（Hugging Face MLエンジニア）

## 原文リンク

[Amazon SageMakerとHugging Faceのパートナーシップ：NLPモデルのトレーニングと推論を簡略化](https://huggingface.co/blog/the-partnership-amazon-sagemaker-and-hugging-face)
