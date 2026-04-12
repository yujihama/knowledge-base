---
title: "オープンな未来に向けて：Hugging FaceとGoogle Cloudの新たな戦略的パートナーシップ"
url: "https://huggingface.co/blog/google-cloud"
date: 2026-04-04
tags: [HuggingFace, GoogleCloud, VertexAI, GKE, TPU, CDN, InferenceEndpoints, ModelGarden, オープンモデル, CloudRun]
category: "infra"
memo: "[HF Blog] Building for an Open Future - our new partnership with Google Cloud"
processed_at: "2026-04-04T12:02:11.172184"
---

## 要約

2025年11月13日、Hugging FaceはGoogle Cloudとの深化した戦略的パートナーシップを発表した。過去3年間でHugging FaceのGoogle Cloudユーザーによる利用は10倍に成長し、現在では月間数十ペタバイトのモデルダウンロードと数十億リクエストを処理している。

主要な技術的取り組みとして、まずHugging Face XetストレージとGoogle Cloud高度ストレージ・ネットワーク技術を組み合わせた「CDN Gateway」の構築が挙げられる。これによりVertex AI・GKE・Cloud Run・Compute Engine上でのモデルダウンロード時間が短縮され、モデルサプライチェーンの堅牢性が向上する。

Vertex AI Model Gardenでは人気オープンモデルをワンクリックでデプロイ可能で、GKE AI/MLでは同様のモデルライブラリとHugging Face管理の事前設定済み環境が提供される。Cloud Run GPUsを用いたサーバーレスなオープンモデル推論も可能となる。

Hugging Face側の顧客向けには、Inference EndpointsにGoogle Cloudのインスタンスが追加され、価格引き下げが予定されている。Hugging Face上の1000万人のAIビルダーがVertex Model GardenやGKEへ数ステップでデプロイできるよう統合が進む。

TPUサポートも強化され、第7世代TPUをGPUと同等の容易さでHugging Faceモデルに利用できるよう、Hugging Faceのライブラリにネイティブサポートが追加される予定。

セキュリティ面では、VirusTotal・Google Threat Intelligence・Mandiantを活用し、Hugging Face Hub上の数百万のオープンモデル・データセット・Spacesのセキュリティ強化が図られる。

GoogleはTransformerアーキテクチャの原著論文への貢献やGemmaモデルシリーズなど1,000以上のモデルをコミュニティに提供しており、Hugging Faceは200万以上のオープンモデルへのアクセスを提供している。両社の強みを組み合わせることで、企業が自社AIを構築・カスタマイズし、自社のセキュアなインフラ内でホストできる未来を目指す。

## アイデア

- CDN Gatewayによるモデルサプライチェーン強化：モデルをクラウドエッジにキャッシュすることでtime-to-first-tokenを削減する設計は、大規模推論インフラの低レイテンシ化パターンとして参考になる
- TPUへのネイティブライブラリサポート：GPU依存から脱却しTPUを汎用的に使えるようにする取り組みは、特定ハードウェアへのロックイン回避という観点で重要な設計方針
- VirusTotal/Mandiant連携によるモデルセキュリティスキャン：オープンモデルのサプライチェーンリスク（悪意あるモデルウェイト等）への対策として、セキュリティツールをAIプラットフォームに統合するアプローチは新しいリスク管理の形
## 関連記事

- /deep_1579 TF ServingとKubernetesを用いたHugging Face ViTモデルのデプロイ
- /deep_1535 JAX / Flax で Stable Diffusion を高速推論する方法
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新
- /deep_1612 Hugging Face Enterprise Hub（旧 Private Hub）：企業向けMLプラットフォームの概要

## 原文リンク

[オープンな未来に向けて：Hugging FaceとGoogle Cloudの新たな戦略的パートナーシップ](https://huggingface.co/blog/google-cloud)
