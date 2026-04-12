---
title: "NVIDIA DGX CloudのH100 GPUでモデルを簡単にトレーニングする方法"
url: "https://huggingface.co/blog/train-dgx-cloud"
date: 2026-04-09
tags: [HuggingFace, NVIDIA, DGX Cloud, H100, AutoTrain, ファインチューニング, Mistral, Llama, クラウドGPU]
category: "infra"
memo: "[HF Blog] Easily Train Models with H100 GPUs on NVIDIA DGX Cloud"
related: [1529, 1216, 994, 835, 1213]
processed_at: "2026-04-09T12:21:02.930660"
---

## 要約

Hugging FaceとNVIDIAが共同で「Train on DGX Cloud」サービスをEnterprise Hubユーザー向けに2024年3月に提供開始した（2025年4月10日にサービス終了）。本サービスはHugging Face AutoTrainとSpacesを基盤としたノーコードのトレーニングジョブ作成環境を提供し、NVIDIA H100 Tensor Core GPU（80GB VRAM）またはL40S GPU（48GB VRAM）を分単位の従量課金で利用可能にするもの。対応モデルアーキテクチャはLlama、Falcon、Mistral、Mixtral、T5、Gemma、Stable Diffusion、Stable Diffusion XLで、GPUインスタンスは1x・2x・4x・8xから選択できる。料金はH100が$8.25/GPU時間、L40Sが$2.75/GPU時間。例えばMistral 7Bを1,500サンプルでL40S 1枚にてファインチューニングした場合、約10分・約$0.45で完了する。利用フローはモデルページの「Train」メニューからDGX Cloudを選択し、Enterprise組織内にAutoTrain用のSpaceを自動作成、データセット（CSV/JSON）をアップロードしてパラメータ（エポック数等）をJSON形式で編集後、「Start Training」をクリックするだけ。トレーニング完了後はファインチューニング済みモデルがHub上のプライベートリポジトリに自動保存される。なお本コラボレーションの範囲はトレーニングに留まらず、StarCoder2 15B（600言語以上のコードLLM）の学習支援、optimum-nvidiaライブラリ（Llama 2で1,200トークン/秒を達成）、NVIDIA TensorRT-LLM連携、NIM microservicesへの主要オープンモデル提供にも及ぶ。

## アイデア

- ノーコードUI（AutoTrain）とエンタープライズクラウドGPUを組み合わせることで、インフラ構築不要でLLMファインチューニングの障壁を大幅に下げる設計思想
- 1x〜8x H100インスタンスを分単位従量課金で提供することで、大規模GPUクラスタを所有せずともスケーラブルなトレーニングを実現するビジネスモデル
- トレーニング結果をHub上のプライベートリポジトリに自動保存する設計により、モデルのバージョン管理とチーム共有をシームレスに統合している点
## 関連記事

- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1216 パーソナルコパイロット：自分専用コーディングアシスタントのトレーニング方法
- /deep_994 TGI Multi-LoRA：1回のデプロイで30モデルを同時配信
- /deep_835 Synthetic Data Generator：自然言語でデータセットを構築するノーコードツール
- /deep_1213 Prodigy-HFの紹介：Hugging Faceとの直接統合

## 原文リンク

[NVIDIA DGX CloudのH100 GPUでモデルを簡単にトレーニングする方法](https://huggingface.co/blog/train-dgx-cloud)
