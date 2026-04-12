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

## Yujiの取り組みへの示唆

監査エージェント開発において、LangGraphのノード内でHugging Face InferenceClientを使う場合、provider切り替えによるモデル比較実験がコード変更最小で実施できる。特にDeepSeek-R1はReasoning能力が高くLLM-as-judgeや監査判断ロジックの検証に活用できるため、Hyperbolic経由での低コスト試用は価値が高い。ローカルLLMインフラ構築中のつなぎとして、RTX 3090環境が整うまでの本番グレード推論基盤としても機能する。

## 原文リンク

[Hugging Face Hub に3つの新サーバーレス推論プロバイダー追加：Hyperbolic、Nebius AI Studio、Novita](https://huggingface.co/blog/inference-providers-nebius-novita-hyperbolic)
