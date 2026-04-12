---
title: "Hugging Face Hub に3つの新サーバーレス推論プロバイダー追加：Hyperbolic、Nebius AI Studio、Novita"
url: "https://huggingface.co/blog/inference-providers-nebius-novita-hyperbolic"
date: 2026-04-08
tags: [HuggingFace, ServerlessInference, InferenceProvider, DeepSeek-R1, FLUX.1, huggingface_hub, API]
category: "infra"
memo: "[HF Blog] Introducing Three New Serverless Inference Providers: Hyperbolic, Nebius AI Studio, and Novita 🔥"
processed_at: "2026-04-08T09:46:11.330884"
---

## 要約

Hugging Face Hub が2025年2月18日、サーバーレス推論エコシステムに新たに3社のプロバイダー（Hyperbolic、Nebius AI Studio、Novita）を追加したことを発表した。これにより既存のTogether AI、Sambanova、Replicate、fal、Fireworks.ai と合わせて8社体制となった。

技術的な仕組みとして、各プロバイダーはHugging FaceのPythonクライアント（huggingface_hub）およびJavaScriptクライアント（@huggingface/inference）と統合されており、provider パラメータを切り替えるだけで同一コードから異なるプロバイダーを利用できる。認証モードは2種類あり、「カスタムキーモード」では各プロバイダーのAPIキーを直接使用して課金もプロバイダー側に発生し、「HFルーティングモード」ではHugging Faceトークンのみで利用でき課金はHFアカウントに集約される。重要な点として、HFルーティングでは価格へのマークアップは行われず、プロバイダーコストをそのまま通過させる形となっている。

対応モデルとして、DeepSeek-R1（Hyperbolicで対応）、FLUX.1-dev・FLUX.1-schnell（Nebius AI Studioで対応）など実用的なモデルが新たに利用可能となった。コード例では、HyperbolicでDeepSeek-R1を使ったテキスト生成、Nebius AI StudioでFLUX.1-schnellを使った画像生成（PIL.Imageオブジェクトで返却）が示されており、max_tokens=500等のパラメータはプロバイダー間で共通して使用できる。

料金面では、Hugging Face PROプランユーザーは月2ドル分の推論クレジットが付与され、複数プロバイダーをまたいで利用可能。無料ユーザーにも小枠のクォータが用意されている。UIからはアカウント設定でプロバイダーの優先順位を設定でき、モデルページのウィジェットやコードスニペットにも反映される。将来的にはプロバイダーとのレベニューシェア契約も検討されている。

## アイデア

- provider パラメータ1行変更で推論バックエンドを切り替え可能な抽象化設計は、ベンダーロックイン回避とコスト最適化を同時に実現する実用的なパターン
- HFルーティングモードによりプロバイダー個別のアカウント管理なしに複数プロバイダーを試せるため、プロトタイピング速度が大幅に向上する
- PROプランの月2ドルクレジットをDeepSeek-R1等の高性能モデルに割り当てることで、低コストで高精度な推論実験が可能
## 関連記事

- /deep_768 Fireworks.aiがHugging Face Hubの推論プロバイダーとして統合
- /deep_417 OVHcloudがHugging Face Inference Providersに参加——欧州データセンターからのサーバーレスLLM推論
- /deep_1486 モデルカード：MLモデルのドキュメント化フレームワークとHugging Faceの取り組み
- /deep_402 Hugging Face Hub に Storage Buckets が登場 — S3ライクなミュータブルオブジェクトストレージ
- /deep_583 Featherless AIがHugging Face Inference Providersに統合 — サーバーレスで膨大なモデルカタログにアクセス可能に

## 原文リンク

[Hugging Face Hub に3つの新サーバーレス推論プロバイダー追加：Hyperbolic、Nebius AI Studio、Novita](https://huggingface.co/blog/inference-providers-nebius-novita-hyperbolic)
