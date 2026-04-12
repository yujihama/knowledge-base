---
title: "NVIDIA DGX CloudのH100 GPUでモデルを簡単にトレーニングする方法"
url: "https://huggingface.co/blog/train-dgx-cloud"
date: 2026-04-09
tags: [HuggingFace, NVIDIA, DGX Cloud, H100, AutoTrain, ファインチューニング, Mistral, Llama, クラウドGPU]
category: "infra"
memo: "[HF Blog] Easily Train Models with H100 GPUs on NVIDIA DGX Cloud"
processed_at: "2026-04-09T12:21:02.930660"
---

## 要約

Hugging FaceとNVIDIAが共同で「Train on DGX Cloud」サービスをEnterprise Hubユーザー向けに2024年3月に提供開始した（2025年4月10日にサービス終了）。本サービスはHugging Face AutoTrainとSpacesを基盤としたノーコードのトレーニングジョブ作成環境を提供し、NVIDIA H100 Tensor Core GPU（80GB VRAM）またはL40S GPU（48GB VRAM）を分単位の従量課金で利用可能にするもの。対応モデルアーキテクチャはLlama、Falcon、Mistral、Mixtral、T5、Gemma、Stable Diffusion、Stable Diffusion XLで、GPUインスタンスは1x・2x・4x・8xから選択できる。料金はH100が$8.25/GPU時間、L40Sが$2.75/GPU時間。例えばMistral 7Bを1,500サンプルでL40S 1枚にてファインチューニングした場合、約10分・約$0.45で完了する。利用フローはモデルページの「Train」メニューからDGX Cloudを選択し、Enterprise組織内にAutoTrain用のSpaceを自動作成、データセット（CSV/JSON）をアップロードしてパラメータ（エポック数等）をJSON形式で編集後、「Start Training」をクリックするだけ。トレーニング完了後はファインチューニング済みモデルがHub上のプライベートリポジトリに自動保存される。なお本コラボレーションの範囲はトレーニングに留まらず、StarCoder2 15B（600言語以上のコードLLM）の学習支援、optimum-nvidiaライブラリ（Llama 2で1,200トークン/秒を達成）、NVIDIA TensorRT-LLM連携、NIM microservicesへの主要オープンモデル提供にも及ぶ。

## アイデア

- ノーコードUI（AutoTrain）とエンタープライズクラウドGPUを組み合わせることで、インフラ構築不要でLLMファインチューニングの障壁を大幅に下げる設計思想
- 1x〜8x H100インスタンスを分単位従量課金で提供することで、大規模GPUクラスタを所有せずともスケーラブルなトレーニングを実現するビジネスモデル
- トレーニング結果をHub上のプライベートリポジトリに自動保存する設計により、モデルのバージョン管理とチーム共有をシームレスに統合している点

## Yujiの取り組みへの示唆

監査エージェント開発においてLangGraphやPydanticベースのモデルをドメイン特化データでファインチューニングする際、本サービスのようなノーコード環境はプロトタイピングのスピードを高める参考事例となる。ただし本サービス自体は2025年4月に終了しており、現在はHugging Face Inference Endpoints等の代替手段を検討する必要がある。ローカルLLMインフラ（RTX 3090）構築中であるYujiにとっては、クラウドGPUとローカルGPUのコスト・レイテンシ比較の観点からH100の$8.25/時間という単価は参照ベンチマークとして有用。

## 原文リンク

[NVIDIA DGX CloudのH100 GPUでモデルを簡単にトレーニングする方法](https://huggingface.co/blog/train-dgx-cloud)
