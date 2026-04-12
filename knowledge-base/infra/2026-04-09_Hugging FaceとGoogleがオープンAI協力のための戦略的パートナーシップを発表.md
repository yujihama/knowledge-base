---
title: "Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表"
url: "https://huggingface.co/blog/gcp-partnership"
date: 2026-04-09
tags: [Hugging Face, Google Cloud, Vertex AI, TPU, GKE, Inference Endpoints, オープンソース, モデルデプロイ]
category: "infra"
memo: "[HF Blog] Hugging Face and Google partner for open AI collaboration"
processed_at: "2026-04-09T21:07:45.751177"
---

## 要約

2024年1月25日、Hugging FaceとGoogle Cloudは、オープンなAI開発の民主化を目的とした戦略的パートナーシップを発表した。協力の柱は4つ：オープンサイエンス、オープンソース、Google Cloudユーザー向け統合、Hugging Face Hubユーザー向け新機能である。

オープンサイエンスの側面では、Transformerや Vision Transformerを生み出したGoogleの研究成果と、現在100万件超のモデル・データセット・AIアプリケーションをホストするHugging Face Hubの影響力を組み合わせ、最新AI研究の普及を加速する。

オープンソースでは、TensorFlowやJAXといったGoogleのOSSツールとHugging FaceのライブラリをさらAPI・フレームワーク横断で統合しやすくする。

Google Cloud統合面では、Google Kubernetes Engine（GKE）およびVertex AI上でHugging Faceモデルのトレーニング・デプロイが容易になる。利用できるハードウェアはTPUインスタンス、NVIDIA H100搭載のA3 VM、Intel Sapphire Rapids搭載のC3 VMと多様。

Hub ユーザー向けには、Inference EndpointsによるGoogle Cloud上のプロダクションデプロイ、Hugging Face SpacesへのTPUアクセラレーション、Enterprise HubサブスクリプションのGoogle Cloudアカウント経由の課金管理が提供される予定。

なお、2025年11月13日には同パートナーシップのさらなる深化が発表されており、企業が独自のAIをオープンモデルで構築するための基盤強化が進んでいる。Google Cloud CEOのThomas Kurian氏はVertex AIと安全なインフラへのアクセス提供を、Hugging Face CEOのClement Delangue氏はTPUを含む最適化インフラとの組み合わせによる開発者支援を強調した。

## アイデア

- Vertex AI + Hugging Face Hubの統合により、100万件超のオープンモデルをエンタープライズグレードのMLOpsパイプラインに直接組み込める経路が確立された
- TPUをHugging Face Spaces上で利用可能にする設計は、高コストなGPUなしに大規模推論を試験できる民主化モデルとして注目に値する
- Enterprise HubサブスクリプションをGoogle Cloud課金に統合することで、企業のガバナンス・コスト管理とオープンモデル利用を両立させるアーキテクチャパターンを示している
## 関連記事

- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け
- /deep_418 オープンな未来に向けて：Hugging FaceとGoogle Cloudの新たな戦略的パートナーシップ
- /deep_1396 Snorkel AI × Hugging Face：エンタープライズ向けファウンデーションモデル活用基盤の構築
- /deep_709 Inference Endpoints の新しいアナリティクスダッシュボード
- /deep_1578 Hugging FaceのTensorFlow哲学：KerasネイティブなTransformersの設計方針

## 原文リンク

[Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表](https://huggingface.co/blog/gcp-partnership)
