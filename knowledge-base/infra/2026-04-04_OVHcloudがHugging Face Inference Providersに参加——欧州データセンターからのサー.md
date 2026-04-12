---
title: "OVHcloudがHugging Face Inference Providersに参加——欧州データセンターからのサーバーレスLLM推論"
url: "https://huggingface.co/blog/OVHcloud/inference-providers-ovhcloud"
date: 2026-04-04
tags: [OVHcloud, HuggingFace, InferenceProvider, サーバーレス推論, 欧州データ主権, gpt-oss, DeepSeek-R1, ファンクションコーリング, 構造化出力]
category: "infra"
memo: "[HF Blog] OVHcloud on Hugging Face Inference Providers 🔥"
processed_at: "2026-04-04T09:08:39.631363"
---

## 要約

OVHcloudが2025年11月24日にHugging Face Hub公式のInference Providerとして追加された。これにより、HuggingFaceのモデルページから直接OVHcloudのAI Endpointsを通じてgpt-oss-120b、Qwen3、DeepSeek R1、Llamaなどのオープンウェイトモデルを呼び出せるようになった。

OVHcloud AI Endpointsはフルマネージドのサーバーレスサービスで、ファーストトークンまでのレイテンシが200ms以下という仕様を持つ。料金は€0.04/100万トークンから。インフラは欧州のデータセンターに配置されており、GDPRや業界規制に基づくデータ主権の要件を満たす構成となっている。

技術的な統合方法は2通りある。(1) Python SDKの場合、`huggingface_hub>=1.1.5`の`InferenceClient`を使い、モデル名を`openai/gpt-oss-120b:ovhcloud`のように`モデル名:プロバイダー名`形式で指定する。(2) JavaScriptの場合は`@huggingface/inference`の`InferenceClient`で同様の指定が可能。

認証・課金の仕組みは2モード構造で、(a) OVHcloudのAPIキーを直接使う「ダイレクトモード」ではOVHcloudアカウントに課金、(b) HFトークンで認証する「ルーティングモード」ではHugging Faceアカウントに課金される（追加マークアップなし）。HF PROユーザーは月$2相当の推論クレジットが付与される。

対応機能はテキスト生成・埋め込みモデルのほか、構造化出力（Structured Outputs）、ファンクションコーリング、テキスト・画像のマルチモーダル処理が含まれる。これらはエージェント系ワークフローでのツール呼び出しや出力パース処理に直接使える機能群である。

## アイデア

- モデル名に`:ovhcloud`サフィックスを付けるだけでプロバイダーを切り替えられる設計は、マルチプロバイダー冗長化や価格比較をコード変更最小で実現できる抽象化として参考になる
- 欧州データセンター完結・データ主権保証という構成は、金融・監査領域の規制要件（GDPR、SOX等）を満たすLLMインフラの選択肢として実用的な位置づけ
- ファーストトークン200ms以下という仕様と構造化出力+ファンクションコーリングの組み合わせは、ReActループの各ステップで外部ツール呼び出しを伴うエージェントのレイテンシ設計に直接影響する

## Yujiの取り組みへの示唆

LangGraphベースの監査エージェント開発において、構造化出力とファンクションコーリングを200ms以下のレイテンシで提供できる欧州拠点のサーバーレス推論基盤は、ReActループの応答速度とPydanticによるスキーマバリデーションの組み合わせを本番環境で検証する際の候補インフラになり得る。また、HFトークン1本でプロバイダーを切り替えられる`InferenceClient`のインターフェースは、LLM-as-judgeの評価実験でモデルやプロバイダーをA/Bテストする際のコスト管理と切り替え実装を簡素化できる。

## 原文リンク

[OVHcloudがHugging Face Inference Providersに参加——欧州データセンターからのサーバーレスLLM推論](https://huggingface.co/blog/OVHcloud/inference-providers-ovhcloud)
