---
title: "Fireworks.aiがHugging Face Hubの推論プロバイダーとして統合"
url: "https://huggingface.co/blog/fireworks-ai"
date: 2026-04-08
tags: [Fireworks.ai, HuggingFace, サーバーレス推論, InferenceProvider, DeepSeek-R1, huggingface_hub, LLM推論API]
category: "infra"
memo: "[HF Blog] Welcome Fireworks.ai on the Hub 🎆"
processed_at: "2026-04-08T09:46:44.160102"
---

## 要約

Hugging Face Hubは2025年2月14日、Fireworks.aiを公式の推論プロバイダー（Inference Provider）として追加したと発表した。これはHugging Faceが推進する「Inference Providers on the Hub」構想の一環であり、サードパーティの高速推論サービスをHubのエコシステムに直接統合するものである。

Fireworks.aiは高速なサーバーレス推論を提供するサービスで、今回の統合によりHugging Faceのモデルページ上から直接、またはhuggingface_hub等のライブラリ経由でFireworks.aiのバックエンドを利用したAPIコールが可能となった。対応モデルにはDeepSeek-R1、DeepSeek-V3、Mistral-Small-24B-Instruct-2501、Qwen2.5-Coder-32B-Instruct、Llama-3.2-90B-Vision-Instructなど主要な大規模モデルが含まれる。

技術的な利用方法は3種類提供されている。①PythonのhuggingFace_hubライブラリでprovider="fireworks-ai"を指定してInferenceClientを初期化する方法、②JavaScriptの@huggingface/inferenceライブラリでproviderパラメータを指定する方法、③Hugging Faceのルーターエンドポイント（https://router.huggingface.co/fireworks-ai/v1/chat/completions）に対して直接curlでHTTPリクエストを送る方法。いずれもHugging FaceトークンまたはFireworks.aiのAPIキーで認証できる。

課金体系は「直接リクエスト」と「ルート経由リクエスト」の2種類。Fireworks.aiのAPIキーを使う場合はFireworksアカウントに課金され、Hugging Faceトークン経由の場合はHugging Face側に課金されるが、HF側の追加マージンはなくFireworksの標準料金がそのまま適用される。Hugging Face PROプランのユーザーは月額$2相当の推論クレジットを取得でき、複数プロバイダーにまたがって利用可能。

この統合の意義は、開発者がモデルの選定・プロバイダーの切り替えをAPIレイヤーの変更のみで実現できる点にある。Fireworks.aiはGPU最適化・量子化・バッチ処理等の最適化を内部で行い、エンドユーザーには高スループット・低レイテンシのAPIを提供する。Hugging Faceのルーターが抽象化レイヤーとして機能するため、将来的に別プロバイダーへの切り替えもproviderパラメータ1つで対応できる設計となっている。

## アイデア

- provider=パラメータ1つで推論バックエンドを切り替えられる設計は、マルチプロバイダー対応エージェントシステムのポータビリティを大幅に高める
- Hugging FaceルーターがAPIゲートウェイとして機能し、認証・課金・ルーティングを一元管理する構造は、エンタープライズでの複数LLMプロバイダー管理の参考アーキテクチャになる
- DeepSeek-R1のような推論特化モデルをサーバーレスで呼び出せることで、ローカルGPU環境なしでもRLAIF・LLM-as-judgeの実験コストを抑えられる
## 関連記事

- /deep_417 OVHcloudがHugging Face Inference Providersに参加——欧州データセンターからのサーバーレスLLM推論
- /deep_767 Hugging Face Hub に3つの新サーバーレス推論プロバイダー追加：Hyperbolic、Nebius AI Studio、Novita
- /deep_1486 モデルカード：MLモデルのドキュメント化フレームワークとHugging Faceの取り組み
- /deep_402 Hugging Face Hub に Storage Buckets が登場 — S3ライクなミュータブルオブジェクトストレージ
- /deep_583 Featherless AIがHugging Face Inference Providersに統合 — サーバーレスで膨大なモデルカタログにアクセス可能に

## 原文リンク

[Fireworks.aiがHugging Face Hubの推論プロバイダーとして統合](https://huggingface.co/blog/fireworks-ai)
