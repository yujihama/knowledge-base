---
title: "QuantoとDiffusersによるメモリ効率的なDiffusion Transformerの推論"
url: "https://huggingface.co/blog/quanto-diffusers"
date: 2026-04-09
tags: [Quanto, Diffusers, 量子化, INT8, FP8, INT4, Stable Diffusion 3, PixArt-Sigma, メモリ最適化, 推論効率化]
category: "infra"
memo: "[HF Blog] Memory-efficient Diffusion Transformers with Quanto and Diffusers"
processed_at: "2026-04-09T09:05:37.006975"
---

## 要約

本記事は、HuggingFaceのQuantoライブラリとDiffusersを組み合わせてTransformerベースの拡散モデルのメモリ使用量を削減する手法を解説する。対象モデルはPixArt-Sigma（0.611B）、Stable Diffusion 3（2.028B）、Aura Flow（6.843B）の3種で、H100 GPU上でFP16/BF16ベースラインとの比較ベンチマークを実施している。

Quantoによる量子化はoptimum.quantoのquantize()とfreeze()を呼び出すだけで適用でき、weights引数にqfloat8/qint8/qint4を指定する。FP8量子化ではPixArt-Sigmaのメモリが12.086GB→11.547GBに減少（約4.5%削減）とわずかだが、テキストエンコーダも同時に量子化すると5.363GBまで劇的に低下（約56%削減）し、レイテンシは1.540s→1.601sとほぼ変わらない。

Stable Diffusion 3は3つのテキストエンコーダを持ち、第2エンコーダ（CLIPTextModelWithProjection系）の量子化は品質劣化を招くため非推奨。第1と第3エンコーダ（T5EncoderModel）を量子化した場合、メモリ8.204GB・レイテンシ2.789sとなり、量子化なし16.403GB・2.118sと比べて半分以下のメモリで推論可能。

INT8はFP8よりレイテンシが良好で、fuse_qkv_projections()でQKVプロジェクションを水平融合するとさらに高速化される（バッチサイズ4で5.129s→4.989s）。INT4はbfloat16+H100限定で、メモリを3.058GBまで削減できるが、レイテンシは7.6秒超と大幅に増加する。INT4ではハードウェアネイティブサポートがなく、重みを4bitで転送しても計算はbfloat16で行うため。最終投影層をINT4から除外することで品質劣化を緩和する。

モデルの保存・ロードはsave_pretrained()/from_pretrained()で通常通り可能で、QuantoConfig経由で量子化設定を永続化できる。CPUオフロード（enable_model_cpu_offload()）との組み合わせでさらなるメモリ削減も実現可能。bfloat16はH100や4090等の対応アーキテクチャでFP16より高速（INT8時1.538s→1.454s）。

## アイデア

- テキストエンコーダの量子化がDiffusion Backboneより劇的なメモリ削減効果をもたらす点（12GB→5.3GB）は、マルチモデルパイプラインでのボトルネックがエンコーダ側にあることを示唆する
- SD3の第2テキストエンコーダのみ量子化不可という非対称な制約は、モデルアーキテクチャの数値安定性がエンコーダごとに異なることを示しており、量子化可能コンポーネントの事前評価が重要
- INT4はメモリを3GBまで削減できるが計算はbfloat16で行うため速度向上がない、という「転送効率型量子化」の概念はLLM量子化（GPTQ等）と同様のトレードオフ設計

## Yujiの取り組みへの示唆

監査エージェントシステムでローカルLLM（RTX 3090予定）を活用する際、Quantoの量子化手法はVRAM 24GBの制約内で大規模モデルを動かすための直接的な実装パターンとして参照できる。特にテキストエンコーダとメインモデルを個別に量子化する設計思想は、LangGraphのマルチエージェント構成でコンポーネントごとにメモリ最適化を適用する際に応用可能。save_pretrained()/from_pretrained()の互換性維持により、Diffusersベースのパイプラインを既存コードを大きく変更せず量子化できる点も実用的。

## 原文リンク

[QuantoとDiffusersによるメモリ効率的なDiffusion Transformerの推論](https://huggingface.co/blog/quanto-diffusers)
