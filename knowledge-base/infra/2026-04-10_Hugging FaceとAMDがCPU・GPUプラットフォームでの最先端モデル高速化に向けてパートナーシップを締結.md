---
title: "Hugging FaceとAMDがCPU・GPUプラットフォームでの最先端モデル高速化に向けてパートナーシップを締結"
url: "https://huggingface.co/blog/huggingface-and-amd"
date: 2026-04-10
tags: [AMD, ROCm, Hugging Face, Instinct MI250, EPYC, Optimum, TransformersライブラリGPU最適化, 量子化]
category: "infra"
memo: "[HF Blog] Hugging Face and AMD partner on accelerating state-of-the-art models for CPU and GPU platforms"
processed_at: "2026-04-10T09:42:08.419725"
---

## 要約

2023年6月、Hugging FaceはAMDをHardware Partner Programに迎え入れ、AMDのCPU・GPUプラットフォーム上でのTransformerモデルの最適化・高速化に向けた協業を開始した。

GPU側では、エンタープライズ向けのInstinct MI200シリーズ（MI250/MI300等）およびMI300シリーズを優先的に対応し、続いてコンシューマ向けのRadeon Navi3xファミリーへと展開する計画。AMDの初期テストによれば、MI250はBERT-Largeのトレーニング速度で競合製品比1.2倍、GPT2-Largeで1.4倍の性能を達成している。

CPU側では、クライアント向けRyzenおよびサーバー向けEPYCで推論最適化を進める。量子化などモデル圧縮技術と組み合わせることで、CPUでもTransformer推論の実用的な選択肢になりうる点が強調されている。さらにAlveo V70 AIアクセラレータ（低消費電力・高性能）も対象プラットフォームに含まれる。

サポート対象アーキテクチャは、NLP系（BERT、DistilBERT、RoBERTa）、ビジョン系（ViT、CLIP、ResNet、ResNeXt）、音声系（Wav2Vec2）、生成AI系（GPT2、GPT-NeoX、T5、OPT、LLaMA、BLOOM、StarCoder）と幅広い。フレームワークはPyTorch、TensorFlow、ONNX Runtimeを対象とする。

実装面では、AMD ROCm SDKをTransformersライブラリを皮切りにHugging Faceのオープンソースライブラリに統合し、最終的にはAMD専用のOptimumライブラリを新設してユーザーがコード変更を最小限にAMDプラットフォームを利用できる環境を整備する方針。

このパートナーシップの背景には、深層学習向けハードウェア選択肢がNVIDIA一強に偏っている市場構造と、価格・供給面での課題がある。AMDとの協業により、コストパフォーマンスの新たな基準を打ち立てることを目指している。

## アイデア

- MI250でBERT-Large 1.2倍・GPT2-Large 1.4倍という具体的なベンチマーク数値が示すように、AMD GPUは既にNVIDIA対抗として実用域に達しており、ベンダーロックイン回避の現実的選択肢になりつつある
- AMD専用Optimumライブラリの設計方針（コード変更最小化）は、ハードウェア抽象化レイヤーのあり方として参考になる——モデルコードをハードウェア非依存に保ちつつ最適化を差し込む設計パターン
- Alveo V70のような専用AIアクセラレータ（低電力・高性能）がHugging Faceエコシステムに組み込まれることで、エッジ・省電力推論の選択肢が広がり、オンプレミス展開シナリオが多様化する
## 関連記事

- /deep_580 Hugging Face Kernel Hub：5分で始める最適化カーネルの活用
- /deep_413 AMD オープンロボティクスハッカソン参加募集
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1310 複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力

## 原文リンク

[Hugging FaceとAMDがCPU・GPUプラットフォームでの最先端モデル高速化に向けてパートナーシップを締結](https://huggingface.co/blog/huggingface-and-amd)
