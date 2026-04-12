---
title: "BLOOMトレーニングを支えた技術：Megatron-DeepSpeedによる176Bパラメータモデルの学習基盤"
url: "https://huggingface.co/blog/bloom-megatron-deepspeed"
date: 2026-04-11
tags: [BLOOM, Megatron-DeepSpeed, 3D並列処理, テンソル並列, パイプライン並列, ZeRO, A100, 分散学習, LLM訓練基盤, bf16]
category: "infra"
memo: "[HF Blog] The Technology Behind BLOOM Training"
processed_at: "2026-04-11T21:30:54.424195"
---

## 要約

BLOOMは1,760億パラメータの多言語大規模言語モデルであり、2022年3月〜7月の約3.5ヶ月（約100万GPU時間）をかけてフランス国立計算センター（IDRIS）のスーパーコンピュータ「Jean Zay」上で訓練された。ハードウェア構成は384基のNVIDIA A100 80GB GPU（48ノード）、各ノードにNVLink 4接続の8GPU、AMD EPYC 7543 CPUと512GBのCPUメモリ、ノード間接続にはOmni-Path Architecture（OPA）を採用。データセットは59言語・3,500億トークン（1.5TBの重複排除済みテキスト）で、語彙サイズは250,680トークン。

ソフトウェアスタックの核心はMegatron-DeepSpeedであり、NVIDIAのMegatron-LMとMicrosoftのDeepSpeedを組み合わせた3次元並列処理（3D Parallelism）を実装している。具体的には：①データ並列（DP）＝同一モデルを複数GPUに複製してデータのスライスを分散処理、②テンソル並列（TP）＝各テンソルをシャード分割して複数GPUに水平分散（Megatron-LM提供）、③パイプライン並列（PP）＝モデルをレイヤー単位で垂直分割してGPU間でパイプライン処理（DeepSpeed提供）。これに加えてZeRO（Zero Redundancy Optimizer）によるテンソルシャーディングでGPUメモリを効率化し、オプティマイザ状態・勾配・パラメータをGPU間で分散保持する。

モデルアーキテクチャはGPT-3ベースにALiBiポジショナルエンベッディング、埋め込み層LayerNorm、GeLUアクティベーション関数などの改良を加えたもの。チェックポイントはfp32オプティマイザ状態＋bf16/fp32重みで2.3TB、bf16重みのみで329GB。HuggingFace BigScienceチームを中心に、Microsoft DeepSpeedチーム、NVIDIA Megatron-LMチーム、IDRISチーム、PyTorchチームが連携して実現した大規模協調プロジェクトである。

## アイデア

- 3D並列処理（DP+TP+PP）の組み合わせにより、単一フレームワークでは不可能なスケールのモデル訓練を実現している点：各並列化手法は補完的であり、ZeROによるメモリ最適化との統合がカギ
- BF16精度とfp32オプティマイザ状態の混合精度訓練：数値安定性とメモリ効率を両立するためのエンジニアリング判断が、大規模LLM訓練の実用的ベストプラクティスとして参照できる
- ALiBiポジショナルエンベッディングの採用：従来の正弦波位置エンコーディングに代わり、外挿性能に優れたALiBiを選択したアーキテクチャ判断は、長文コンテキスト処理が重要なドメインへの応用を示唆する
## 関連記事

- /deep_1275 PyTorch FSDPを使ったLlama 2 70Bのファインチューニング
- /deep_1306 Intel CPU上でのStable Diffusionモデルのファインチューニング
- /deep_1489 高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較
- /deep_1536 最適化の記録: BLOOM推論サーバーの高速化
- /deep_429 大規模AIシステムにおける戦略的レバーとしてのスループット最適化：データローダーとメモリプロファイリング革新からの証拠

## 原文リンク

[BLOOMトレーニングを支えた技術：Megatron-DeepSpeedによる176Bパラメータモデルの学習基盤](https://huggingface.co/blog/bloom-megatron-deepspeed)
