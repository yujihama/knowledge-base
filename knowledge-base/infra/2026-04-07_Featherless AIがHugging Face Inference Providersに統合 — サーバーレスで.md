---
title: "Featherless AIがHugging Face Inference Providersに統合 — サーバーレスで膨大なモデルカタログにアクセス可能に"
url: "https://huggingface.co/blog/inference-providers-featherless"
date: 2026-04-07
tags: [Featherless-AI, Hugging-Face, Inference-Provider, serverless, DeepSeek-R1, huggingface_hub, GPU-orchestration, model-catalog]
category: "infra"
memo: "[HF Blog] Featherless AI on Hugging Face Inference Providers 🔥"
related: [767, 768, 861, 1263, 1487]
processed_at: "2026-04-07T21:00:32.634752"
---

## 要約

Hugging Face Hub上のInference Providersエコシステムに、Featherless AIが新たに追加された。Featherless AIはサーバーレス型のAI推論プロバイダーで、独自のモデルローディング技術とGPUオーケストレーション機構により、DeepSeek・Meta・Google・Qwenなどの最新オープンソースモデルを含む非常に広範なモデルカタログを提供する。

他のプロバイダーが「低コストだが限られたモデル数」か「広いモデル範囲だがユーザー自身がサーバー管理とコスト負担」というトレードオフを抱える中、Featherless AIはサーバーレス価格体系のままで広範なモデルを提供できる点が技術的な差別化要素である。

利用方法は2通りある。①カスタムキーモード：ユーザーが自身のFeatherless AI APIキーを設定し、リクエストはFeatherless AIに直接送られ、課金もFeatherless AIアカウントに対して行われる。②HFルーティングモード：Hugging Faceトークンで認証し、HF経由でルーティングされる。この場合、プロバイダーのAPIレートがそのまま請求され、HFによる上乗せマージンはない（将来的にレベニューシェア協定を検討中）。HF PROユーザーは毎月2ドル分のInferenceクレジットが付与される。

Python SDKからの利用例では、`huggingface_hub`（v0.33.0以上）の`InferenceClient`に`provider="featherless-ai"`を指定するだけでDeepSeek-R1-0528などのモデルを呼び出せる。JavaScriptの`@huggingface/inference`でも同様にproviderパラメータで切り替え可能。HFのモデルページUIからもプロバイダーを選択・優先順位付けできる。

Inference Providers統合の仕組みとして、Hubのモデルページはそのモデルをサポートするサードパーティプロバイダーを一覧表示し、ユーザーの設定した優先順位に基づいてウィジェットやコードスニペットに反映される。

## アイデア

- 独自のGPUオーケストレーション技術により、通常は大規模なGPUクラスタ管理が必要な広範なモデルカタログをサーバーレスで実現している点——モデルを『常時ロード』せず動的にスワップする仕組みが推測される
- HFがプロバイダー間のルーティング層になることで、ユーザーはコード変更なしにプロバイダーを切り替えられる抽象化レイヤーが形成されており、マルチプロバイダー戦略の実装コストが大幅に下がる
- 課金のパススルー方式（HFがマージンを乗せない）は、エコシステム拡大を優先した戦略であり、将来的なレベニューシェアへの転換を示唆している——インフラレイヤーのビジネスモデルとして参考になる
## 関連記事

- /deep_767 Hugging Face Hub に3つの新サーバーレス推論プロバイダー追加：Hyperbolic、Nebius AI Studio、Novita
- /deep_768 Fireworks.aiがHugging Face Hubの推論プロバイダーとして統合
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_1263 物体検出リーダーボード：評価指標とその落とし穴の解説
- /deep_1487 機械学習におけるバイアスについて語ろう！倫理・社会ニュースレター第2号

## 原文リンク

[Featherless AIがHugging Face Inference Providersに統合 — サーバーレスで膨大なモデルカタログにアクセス可能に](https://huggingface.co/blog/inference-providers-featherless)
