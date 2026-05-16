---
title: "DeepInfraがHugging Face Inference Providersに統合：サーバーレス推論の選択肢が拡大"
url: "https://huggingface.co/blog/inference-providers-deepinfra"
date: 2026-05-07
tags: [HuggingFace, DeepInfra, Inference Providers, サーバーレス推論, DeepSeek V4, OpenAI互換API, LLMホスティング]
category: "infra"
related: [399, 417, 989, 768, 3639]
memo: "[HF Blog] DeepInfra on Hugging Face Inference Providers 🔥"
processed_at: "2026-05-07T21:28:54.534712"
---

## 要約

2026年4月29日、Hugging Face HubのInference Providersエコシステムに新たにDeepInfraが加わった。DeepInfraは100モデル以上を擁するサーバーレスAI推論プラットフォームで、業界最安水準のトークン単価を特徴とする。今回の統合により、DeepSeek V4、Kimi-K2.6、GLM-5.1などの著名なオープンウェイトLLMが、HubのUIおよびSDK経由で即時利用可能となった。初期対応タスクは会話・テキスト生成に限定されるが、text-to-image、text-to-video、埋め込み等は近日中に追加予定。

技術的な仕組みとして、Inference Providersには2種類の呼び出しモードがある。①「カスタムキー」モード：ユーザーがDeepInfra等のプロバイダーで取得したAPIキーを設定し、リクエストはプロバイダーへ直接ルーティングされ、課金もプロバイダー側で発生する。②「HFルーティング」モード：HFトークンのみで認証し、Hugging FaceがDeepInfraへルーティング、課金はHFアカウントに統合される。マークアップなしでプロバイダー料金のみが適用される。HF PROプランユーザーは月$2分の推論クレジットが付与され、複数プロバイダーに横断利用できる。

SDK統合面では、Pythonの`huggingface_hub`（>=1.11.2）と`@huggingface/inference`（JS）からDeepInfraを直接指定できる。OpenAI互換APIとして`https://router.huggingface.co/v1`をbase_urlに設定し、モデル名に`:deepinfra`サフィックスを付与する（例：`deepseek-ai/DeepSeek-V4-Pro:deepinfra`）。既存のOpenAIクライアントをそのまま流用できるため、移行コストはほぼゼロ。Pi、OpenCode、Hermes Agents、OpenClawなど主要エージェントハーネスとの統合も済んでおり、追加のグルーコードなしでDeepInfraホストモデルをエージェントフローに組み込める。

監査エージェント開発への示唆として、HFルーティング経由でDeepSeek V4等の高性能モデルを単一のHFトークンで呼び出せる点は、複数LLMを並列評価するLLM-as-judgeパイプラインや、コスト比較実験の実装コストを大幅に削減する。また、プロバイダーを抽象化したルーターが`:deepinfra`のようなサフィックスで切り替え可能な設計は、エージェントシステムにおけるフォールバック・ロードバランシング戦略の参考アーキテクチャになり得る。

## アイデア

- `:deepinfra`サフィックスによるモデル指定方式は、同一OpenAIクライアントでプロバイダーを動的切り替えできる設計で、エージェントのフォールバック・コスト最適化ルーターの実装パターンとして応用できる
- HFルーティングモードによりプロバイダーのAPIキー管理が不要になる点は、マルチプロバイダー実験環境の認証管理を単純化し、LLM-as-judgeでの複数モデル並列評価コストを下げる
- PROプランの月$2クレジットがDeepInfra・他プロバイダーに横断利用できる仕組みは、従量課金の細粒度管理をHF側に委譲するマルチベンダー推論の統合課金モデルとして新しい

## 前提知識

- **Inference API** → /deep_1707 機械学習によるカスタマーサービスの強化：HuggingFaceエコシステムを使った感情分析パイプラインの実装
- **OpenAI互換API** → /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- **サーバーレス推論** → /deep_417 OVHcloudがHugging Face Inference Providersに参加——欧州データセンターからのサーバーレスLLM推論
- **HuggingFace Hub** (TODO: 読むべき)
- **DeepSeek V4** → /deep_3556 DeepSeek V4が重要な3つの理由：長コンテキスト・低コスト・Huaweiチップ対応

## 関連記事

- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_417 OVHcloudがHugging Face Inference Providersに参加——欧州データセンターからのサーバーレスLLM推論
- /deep_989 Hugging FaceとNVIDIA NIMによるサーバーレス推論（DGX Cloud連携）
- /deep_768 Fireworks.aiがHugging Face Hubの推論プロバイダーとして統合
- /deep_3639 DeepSeek V4 APIマイグレーションガイド — 2026年7月24日の廃止期限前に知っておくべきこと

## 原文リンク

[DeepInfraがHugging Face Inference Providersに統合：サーバーレス推論の選択肢が拡大](https://huggingface.co/blog/inference-providers-deepinfra)
