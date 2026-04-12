---
title: "LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する"
url: "https://zenn.dev/0h_n0/articles/72d86ab27620f2"
date: 2026-03-29
tags: [LLM, Transformer, MLA, GQA, MoE, RoPE, QK-Norm, GatedDeltaNet, DeepSeek, アーキテクチャ比較]
category: "ai-ml"
memo: "[Zenn 機械学習] LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する"
related: [216, 1264, 1335, 641, 203]
processed_at: "2026-03-29T22:20:09.191113"
---

## 要約

Sebastian RaschkaのLLM Architecture Galleryをベースに、GPT-2 XL（1.5B）からLing 2.5（1T）まで30以上のオープンウェイトモデルをアテンション機構・位置エンコーディング・正規化手法・MoE設計の4軸で比較分析した記事。アテンション機構はMHA→GQA→MLA→Linear Attentionの順に進化しており、DeepSeek V3のMLAはKVキャッシュを28倍圧縮（213.5GB→7.6GB）。Qwen3.5やKimi LinearはGated DeltaNetとフルアテンションを3:1で交互配置するハイブリッド構成を採用し、コンテキスト長に対してメモリ使用量を定数化する。正規化ではQK-NormがOLMo 3・Qwen3・Gemma 3等で標準化。位置エンコーディングはRoPEが主流だが、NoPEや部分RoPEも登場。MoEはDeepSeekのMTP（Multi-Token Prediction）やAuxiliary-Loss-FreeロードバランスなどDeepSeek V3の設計が多数採用されている。

## 要点

- MLAはKVキャッシュを28倍圧縮するが、追加の行列乗算コストが発生し、100B以上の規模で性能優位が顕著になる
- Gated DeltaNetによるLinear AttentionはO(n)計算でメモリ定数化を実現するが、長距離依存の保持に限界があるためフルアテンションとの3:1ハイブリッド構成が実用的
- QK-Normは2026年時点で事実上の標準技法となっており、1.5倍の学習率でも訓練安定性を確保できる
## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_1264 本番環境でのLLM最適化：低精度・Flash Attention・アーキテクチャ革新
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_641 トレーニング不要なエキスパート言語モデルの動的アップサイクリング
- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ

## 原文リンク

[LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する](https://zenn.dev/0h_n0/articles/72d86ab27620f2)
