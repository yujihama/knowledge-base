---
title: "Hugging FaceとNVIDIA NIMによるサーバーレス推論（DGX Cloud連携）"
url: "https://huggingface.co/blog/inference-dgx-cloud"
date: 2026-04-09
tags: [NVIDIA NIM, Hugging Face, サーバーレス推論, DGX Cloud, H100, TensorRT-LLM, TGI, OpenAI互換API, Meta-Llama, 従量課金]
category: "infra"
memo: "[HF Blog] Serverless Inference with Hugging Face and NVIDIA NIM"
related: [1114, 1308, 1063, 419, 1310]
processed_at: "2026-04-09T09:06:03.203500"
---

## 要約

2024年7月29日、Hugging FaceはNVIDIA DGX Cloudと連携した「NVIDIA NIM API (serverless)」をEnterprise Hubユーザー向けに提供開始した（※2025年4月10日にサービス終了、後継としてInference Providersを推奨）。本サービスは、LLM推論における初期インフラコストと最適化の複雑さという課題に対し、従量課金型のサーバーレスAPIとして解決策を提供するものだった。

技術的構成として、NVIDIA H100 Tensor Core GPUを専用インフラとして使用し、OpenAI互換API（chat.completions.createおよびmodels.list）を標準インターフェースとして採用。既存のopenai Pythonライブラリをbase_urlの変更のみで転用できる設計で、Enterprise Hubのfine-grainedトークンで認証する。

料金体系はH100 GPU使用時間ベースで1時間$8.25（1秒あたり約$0.0023）。モデル別の必要GPU数と推定コストは以下の通り：Meta-Llama-3-8B-Instructは1GPU・約1秒・$0.0023/リクエスト、Meta-Llama-3-70B-Instructは4GPU・約2秒・$0.0184/リクエスト、Meta-Llama-3.1-405B-Instruct-FP8は8GPU・約5秒・$0.0917/リクエスト。対応モデルはMistral、Mixtral、Meta-Llamaシリーズ合計8モデル。

バックエンドではNVIDIA TensorRT-LLMをHugging Face TGI（Text Generation Inference）フレームワークに統合する取り組みも並行して進めており、推論パフォーマンスと最適化の更なる向上を目指していた。ただしコミュニティからはドキュメント不足・メンテナンス状況への懸念も指摘されていた。

## アイデア

- OpenAI互換APIをbase_urlのみ変更して流用できる設計は、既存コードベースへの推論バックエンド差し替えのパターンとして参考になる
- H100 GPU数とモデルサイズのマッピング（8B→1GPU、70B→4GPU、405B→8GPU）は、ローカルLLMインフラ設計時のGPUメモリ見積もりに直接使える数値
- 2025年4月にサービス終了しInference Providersへ移行した経緯は、クラウドLLMサービスの継続性リスクを示す事例として重要
## 関連記事

- /deep_1114 NVIDIA DGX CloudのH100 GPUでモデルを簡単にトレーニングする方法
- /deep_1308 Hugging Face Inference EndpointsでLLMをデプロイする方法
- /deep_1063 AWSアカウントでHugging Face Enterprise Hubを購読する方法
- /deep_419 連続バッチ処理（Continuous Batching）をゼロから理解する
- /deep_1310 複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー

## 原文リンク

[Hugging FaceとNVIDIA NIMによるサーバーレス推論（DGX Cloud連携）](https://huggingface.co/blog/inference-dgx-cloud)
