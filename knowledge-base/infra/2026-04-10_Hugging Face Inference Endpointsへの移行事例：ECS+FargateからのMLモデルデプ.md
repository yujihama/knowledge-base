---
title: "Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新"
url: "https://huggingface.co/blog/mantis-case-study"
date: 2026-04-10
tags: [HuggingFace, InferenceEndpoints, ECS, Fargate, RoBERTa, FastAPI, Docker, MLOps, モデルデプロイ, transformers]
category: "infra"
memo: "[HF Blog] Why we’re switching to Hugging Face Inference Endpoints, and maybe you should too"
related: [1214, 1446, 1612, 1529, 418]
processed_at: "2026-04-10T12:39:00.819254"
---

## 要約

Mantis社（NLPソリューション提供）が、AWS ECS+Fargateで運用していたMLモデルの推論エンドポイントをHugging Face Inference Endpointsへ移行した事例。移行前のフローはGPUインスタンスでの学習→HF Hubへのアップロード→FastAPI製APIの実装→Dockerコンテナ化→ECRへのプッシュ→ECSクラスターへのデプロイという6ステップだったが、移行後は学習→HF Hubアップロード→Inference Endpointsでのデプロイという3ステップに短縮された。

レイテンシ比較（RoBERTaベースのテキスト分類モデル、Intel Ice Lake CPU、eu-east-1リージョン、同一リージョンのt3-mediumから1000リクエスト）では、ECSのlargeインスタンス（4vCPU/8GB）で約200msだったところ、Inference EndpointsのlargeでP50が80ms±30ms、最大でも108msと2倍以上の高速化を達成。xlargeでは43ms±31msまで短縮された。

コスト面では同サイズのインスタンスでInference Endpointsがlarge換算で月約$175（ECSは$115）と24〜50%高い。ただしECS側のコストにはECR費用やデータ転送コストが含まれておらず実際の差は縮小する。同社はMLOpsチームを持たないため、デプロイ管理の工数削減（月$60のコスト差）を優先して採算が合うと判断。

デプロイ手段はGUI・RESTful API・同社OSS「hugie」CLI（`hugie endpoint create config.json`の1コマンド）に対応。ただしTerraformプロバイダーが未整備な点を課題として挙げ、GitHub Actionsからhugieを呼び出す方式を採用している。また、Endpoint Handlerクラスを使えば1エンドポイントに複数モデルを同居させることも可能で、GPU/CPU双方で使えるコスト削減策として言及されている。sklearnモデルも対象となる点も特徴の一つ。

## アイデア

- ECSでの自前コンテナ運用より公式HFコンテナの方がレイテンシが2倍以上速い：最適化済みのランタイム実装の差が大きく、モデルサービングはカスタム実装より専用マネージドサービスを使う方が性能面でも有利になりうる
- Endpoint Handlerクラスで1エンドポイントに複数モデルを同居：GPUメモリ上限の範囲でモデルを束ねることでコストを抑制でき、小規模なマルチモデル推論サービスのアーキテクチャとして応用可能
- MLOpsチームなしでのマネージドサービス採用判断：コスト差（月$60）ではなく工数・認知負荷の削減を主軸に意思決定しており、スモールチームでのML運用における優先順位の考え方として参考になる
## 関連記事

- /deep_1214 LoRAを用いたRoBERTa・Llama 2・Mistral 7Bの災害ツイート分類性能比較
- /deep_1446 Hugging FaceとAWSが提携：AIの民主化に向けた戦略的パートナーシップ
- /deep_1612 Hugging Face Enterprise Hub（旧 Private Hub）：企業向けMLプラットフォームの概要
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_418 オープンな未来に向けて：Hugging FaceとGoogle Cloudの新たな戦略的パートナーシップ

## 原文リンク

[Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新](https://huggingface.co/blog/mantis-case-study)
