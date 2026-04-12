---
title: "LCM LoRAによるSDXLの4ステップ高速推論"
url: "https://huggingface.co/blog/lcm_lora"
date: 2026-04-09
tags: [LCM, LoRA, SDXL, Stable Diffusion, 蒸留, 高速推論, diffusers, 画像生成]
category: "ai-ml"
memo: "[HF Blog] SDXL in 4 steps with Latent Consistency LoRAs"
related: [1268, 1181, 1302, 1444, 1220]
processed_at: "2026-04-09T21:20:22.756974"
---

## 要約

Latent Consistency Models（LCM）は、Stable DiffusionやSDXLの画像生成に必要なステップ数を25〜50ステップから4〜8ステップに削減する蒸留手法。従来の蒸留はモデルごとに個別に実施する必要があり、大量のGPUリソースと時間を要していた。本手法の核心は、フルモデルの蒸留ではなく少数のLoRAアダプタ層（LoRA: Low-Rank Adaptation）のみを学習させる点にある。これにより、学習済みのLCM LoRAをHugging Face Hub上の任意のファインチューン済みSDXL/SD1.5モデルに適用できるようになる。推論コードは3ステップで実装可能：(1) DiffusionPipelineで標準SDXLを読み込み、(2) `pipe.load_lora_weights('latent-consistency/lcm-lora-sdxl')`でLoRAを適用、(3) schedulerをLCMSchedulerに変更。重要なパラメータとして、guidance_scaleを1（実質無効化）に設定する必要がある。ネガティブプロンプトを使用したい場合は1〜2の範囲で設定可能だが、それ以上の値は機能しない。速度面では、M1 MacでのSDXL（base）は約60秒/枚だったものが、LCM LoRA適用後は約6秒（4ステップ）と10倍高速化。RTX 4090では1秒未満、RTX 3090では約1秒（従来の7秒比）を実現。品質面では1ステップはほぼ使い物にならないが、4〜6ステップで十分な品質に達し、8ステップでは過飽和・アニメ調になる傾向がある。通常のSDXLは20ステップ未満では使用困難なことを考えると、実用性において大きな差がある。また、LCM LoRAをDreambooth等でファインチューンされたモデル（collage-diffusion等SD1.5ベース）に適用する場合は、対応するSD1.5用のLCM LoRA（`latent-consistency/lcm-lora-sdv1-5`）を使用する。さらにLCM LoRAと通常のスタイルLoRAを同時に適用する技術（`set_adapters`と`add_lora_weights`を組み合わせた重み付けマージ）も可能で、例えばPixelArtスタイルLoRAと組み合わせることでピクセルアートを4ステップで生成できる。本ブログ記事はdiffusersライブラリのLCMScheduler統合も含む実装詳細を提供しており、2023年11月時点での公式リリース内容。

## アイデア

- フルモデル蒸留をLoRA層のみの学習に置き換えることで、蒸留コストを大幅削減しつつ任意のファインチューン済みモデルへの転用を可能にした設計思想は、LLMの軽量化・高速化にも応用できる発想
- guidance_scaleを1に設定してCFGを実質無効化することで推論速度を最大化する手法は、品質とスピードのトレードオフを明示的にコントロールするパラメータ設計の好例
- 複数LoRAの重み付けマージ（LCM LoRA + スタイルLoRA）により、高速性と表現力を同時に確保できる合成アーキテクチャは、モジュール式アダプタの組み合わせ可能性を示す
## 関連記事

- /deep_1268 T2I-AdapterによるSDXLの効率的な制御可能生成
- /deep_1181 SegMoE: Segmindによる拡散モデルのMixture of Experts フレームワーク
- /deep_1302 🤗 Diffusers 1周年記念：1年間の主要機能まとめ
- /deep_1444 Swift Diffusers - Mac向け高速Stable Diffusion ネイティブアプリ
- /deep_1220 SDXLの推論高速化・メモリ削減のための実践的最適化手法

## 原文リンク

[LCM LoRAによるSDXLの4ステップ高速推論](https://huggingface.co/blog/lcm_lora)
