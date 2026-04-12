---
title: "TransformersライブラリにおけるMixture of Experts (MoE)の実装と最適化"
url: "https://huggingface.co/blog/moe-transformers"
date: 2026-03-31
tags: [MoE, Mixture-of-Experts, transformers, DeepSeek, Expert-Parallelism, WeightConverter, GroupedGEMM, sparse-architecture, LLM-inference]
category: "ai-ml"
memo: "[HF Blog] Mixture of Experts (MoEs) in Transformers"
related: [188, 196, 99, 141, 766]
processed_at: "2026-03-31T21:06:04.369172"
---

## 要約

本記事はHugging Faceの`transformers`ライブラリがMixture of Experts (MoE)アーキテクチャをファーストクラスサポートするために行った設計変更を解説する。MoEはTransformerのFFN層を複数の「エキスパート」サブネットワークに置き換え、各トークンに対してルーターが少数のエキスパートのみを選択的に活性化する。gpt-oss-20Bを例にとると、21B総パラメータのうち推論時に使用するのは約3.6B（アクティブパラメータ）で、M3 Ultra Mac（メモリ帯域幅800GB/s）上で実測約115 tok/sを達成している。これは3.6Bモデル相当の速度でありながら21Bモデル相当の品質を持つ。主な技術変更は3点：(1) **Weight Loading Refactor**：チェックポイントでは256個の独立テンソル（例: DeepSeek-V3の各エキスパート）として保存される重みを、GPU上のGrouped GEMM等の最適化カーネルが要求する単一連続テンソルへ変換するため、`WeightConverter`抽象を導入。`MergeModulelist`で複数エキスパートをスタック、`SplitModulelist`で逆変換が可能。Lazy Materializationによりスレッドプールで依存解決後に変換を実行し、メモリピークを低減。v4→v5でロード速度が大幅改善（具体数値は記事に掲載）。(2) **Expert Backend**：FP8対応のDeepSeek-V3など大型MoEモデルの推論を高速化するため、`grouped_gemm`ライブラリや`FusedMoE`カーネル（vLLM由来）を`transformers`に統合。CUDA Graphと組み合わせて推論オーバーヘッドを削減。(3) **Expert Parallelism**：エキスパートを複数GPUに分散配置する専用の並列化手法を実装。テンソル並列・パイプライン並列とは独立した並列軸として、DeepSeekやQwen等の大型MoEを効率的に分散推論可能に。背景として、2025年1月のDeepSeek R1の成功がMoE採用を加速させ、Qwen 3.5、MiniMax M2、GLM-5、Kimi K2.5等が相次いでリリースされた。`transformers`ライブラリへのMoEモデル追加数も2年間で急増しており、DeepSeek R1が明確な変曲点となっている。

## アイデア

- アクティブパラメータ数とメモリ帯域幅からトークン生成速度を逆算できる（800GB/s ÷ (3.6B×2bytes) ≈ 111 tok/s）という単純な見積もり式が実測値と高精度に一致しており、ハードウェア選定や性能見積もりに直接使える実用的な指標
- WeightConverterの設計思想（チェックポイントをランタイムレイアウトへの変換パイプラインとして捉える）は、モデルアーキテクチャの変化に対してロジックを柔軟に適応させる汎用的なパターンであり、他のモデル変換・量子化パイプラインにも応用可能
- Expert Parallelismはテンソル並列・パイプライン並列と独立した第三の並列軸であり、エキスパートの数が多いMoEモデルに特有の並列化戦略として、大規模分散推論の設計において重要な概念
## 関連記事

- /deep_188 DeepSeekの瞬間から1年：中国オープンソースAIエコシステムのアーキテクチャ選択
- /deep_196 MoEアーキテクチャ最適化のための包括的スケーリング則
- /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- /deep_141 Hugging Faceにおけるオープンソースの現状：2026年春
- /deep_766 Gemma 4 へようこそ：デバイス上で動くフロンティア・マルチモーダルモデル

## 原文リンク

[TransformersライブラリにおけるMixture of Experts (MoE)の実装と最適化](https://huggingface.co/blog/moe-transformers)
