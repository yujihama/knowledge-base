---
title: "HuggingFace ViTモデルをVertex AIにデプロイする"
url: "https://huggingface.co/blog/deploy-vertex-ai"
date: 2026-04-11
tags: [Vertex AI, ViT, TensorFlow, SavedModel, GCP, MLOps, デプロイ, オートスケーリング, google-cloud-aiplatform]
category: "infra"
memo: "[HF Blog] Deploying 🤗 ViT on Vertex AI"
processed_at: "2026-04-11T21:06:31.674564"
---

## 要約

本記事は、HuggingFace TransformersのVision Transformer（ViT B/16）モデルをGoogle Cloud Platform（GCP）のVertex AIプラットフォームにデプロイする手順を解説したチュートリアルである。前回記事（ローカルおよびKubernetesクラスタへのデプロイ）の続編として位置づけられており、同等のスケーラビリティをより少ないコードで実現する点が特徴。

Vertex AIはGCPが提供するフルマネージドMLプラットフォームで、認証・オートスケーリング・モデルバージョン管理・トラフィック分割・レート制限・モデル監視・バッチ/オンライン予測をUnified APIとして提供する。TensorFlow、PyTorch、scikit-learnをサポートしており、本記事ではTensorFlow SavedModel形式を使用。

デプロイ対象のViT B/16モデルは、前処理（224x224リサイズ、[-1,1]正規化、channels_firstレイアウト変換）と後処理（ロジットからラベルへのマッピング）をモデル内に埋め込んだSavedModel形式でシリアライズされており、base64エンコードされた画像文字列を入力として受け付ける。この設計はtraining-serving skewを抑制するための工夫。

デプロイワークフローは4ステップ：①モデルアーティファクトをGCS（Google Cloud Storage）バケットに保存、②google-cloud-aiplatform PythonSDKのModelServiceClientを使いVertex AI Model Registryにアップロード（コンテナイメージとしてus-docker.pkg.dev/vertex-ai/prediction/tf2-gpu.2-8:latestを指定）、③EndpointServiceClientでエンドポイントを作成、④deploy_model()でモデルをエンドポイントにデプロイ（min/max_replica_count=1、マシンタイプn1-standard-8、NVIDIA Tesla T4 GPU×1）。

予測リクエストはPredictionServiceClientを通じて送信し、base64エンコード画像を渡すとconfidence（float）とlabel（string）が返却される。Kubernetes構成と比べてインフラ管理コードが大幅に削減される点と、オートスケーリングがマネージドで提供される点が主なメリット。

## アイデア

- 前処理・後処理をモデル内に埋め込むSavedModel設計により、training-serving skewをアーキテクチャレベルで排除できる点は、推論パイプラインの信頼性向上に有効
- Vertex AI Model Registryによるモデルバージョン管理とトラフィック分割機能を組み合わせることで、カナリアリリースやロールバックを低コストで実現できる
- google-cloud-aiplatform SDKのみでデプロイ全工程を完結させる設計は、KubernetesのYAML管理と比較してインフラコードの複雑性を大幅に低減する

## Yujiの取り組みへの示唆

監査エージェントシステムをプロダクション運用する際、LangGraphベースのエージェントをVertex AI上にデプロイする参考事例として活用できる。特にモデルのバージョン管理・トラフィック分割機能は、監査エージェントのA/Bテストや段階的ロールアウトに直接応用可能。また、前処理をモデルに埋め込む設計パターンは、Pydanticによる入力バリデーションと組み合わせてエージェントのサービング品質を高める際の参考になる。

## 原文リンク

[HuggingFace ViTモデルをVertex AIにデプロイする](https://huggingface.co/blog/deploy-vertex-ai)
