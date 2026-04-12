---
title: "LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する"
url: "https://zenn.dev/0h_n0/articles/72d86ab27620f2"
date: 2026-03-29
tags: [LLM, Transformer, MLA, GQA, MoE, RoPE, QK-Norm, GatedDeltaNet, DeepSeek, アーキテクチャ比較]
category: "ai-ml"
memo: "[Zenn 機械学習] LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する"
processed_at: "2026-03-29T22:20:09.191113"
---

## 要約

Sebastian RaschkaのLLM Architecture Galleryをベースに、GPT-2 XL（1.5B）からLing 2.5（1T）まで30以上のオープンウェイトモデルをアテンション機構・位置エンコーディング・正規化手法・MoE設計の4軸で比較分析した記事。アテンション機構はMHA→GQA→MLA→Linear Attentionの順に進化しており、DeepSeek V3のMLAはKVキャッシュを28倍圧縮（213.5GB→7.6GB）。Qwen3.5やKimi LinearはGated DeltaNetとフルアテンションを3:1で交互配置するハイブリッド構成を採用し、コンテキスト長に対してメモリ使用量を定数化する。正規化ではQK-NormがOLMo 3・Qwen3・Gemma 3等で標準化。位置エンコーディングはRoPEが主流だが、NoPEや部分RoPEも登場。MoEはDeepSeekのMTP（Multi-Token Prediction）やAuxiliary-Loss-FreeロードバランスなどDeepSeek V3の設計が多数採用されている。

## 要点

- MLAはKVキャッシュを28倍圧縮するが、追加の行列乗算コストが発生し、100B以上の規模で性能優位が顕著になる
- Gated DeltaNetによるLinear AttentionはO(n)計算でメモリ定数化を実現するが、長距離依存の保持に限界があるためフルアテンションとの3:1ハイブリッド構成が実用的
- QK-Normは2026年時点で事実上の標準技法となっており、1.5倍の学習率でも訓練安定性を確保できる

## 監査エージェントへの示唆

監査エージェントにLLMを組み込む際のモデル選定基準として、KVキャッシュ効率（MLA採用モデルは長文書処理に有利）とコンテキスト長の扱い方（Linear Attentionの固定メモリ制約）を定量的に比較できる。特にローカルLLMインフラ構築時に、RTX 3090（24GB VRAM）でのデプロイ可否をアーキテクチャ別のメモリ消費から判断する際に有用。

## 原文リンク

[LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する](https://zenn.dev/0h_n0/articles/72d86ab27620f2)
