---
title: "TransformerでAttention Residualsを観察する"
url: "https://zenn.dev/ka_kan/articles/5307a3031fede6"
date: 2026-03-29
tags: [Transformer, Attention Residuals, 残差接続, LLM, MoonshotAI, PyTorch, アーキテクチャ改善]
category: "ai-ml"
memo: "[Zenn 機械学習] TransformerでAttention Residualsを観察する"
processed_at: "2026-03-29T22:21:56.781752"
---

## 要約

MoonshotAIが提案したAttention Residuals（arxiv:2603.15031）を自作Transformerに実装し、Wikipediaコーパスで検証した実験レポート。標準残差接続では前層の出力を固定的に加算するのに対し、Attention Residualsはブロック境界ごとにそれまでの全ブロック出力を学習可能な線形射影＋softmaxで重み付き合成する方式。8層・512次元・54Mパラメタのモデルで15,000step学習した結果、2層ごとにゲートを配置したAttnRes-2が検証Loss 3.257を記録し、Baseline（3.563）に対して0.3以上の改善を達成。4層ごとのAttnRes-4（3.337）よりも細かいゲート粒度のほうが有効だった。ゲートは加算ではなく置換（h=gate(block_outputs)）として機能する点が実装上の特徴。最適なブロック数はモデル規模・深さに依存する可能性があり、大規模モデルへの適用は今後の検証課題。

## 要点

- Attention Residualsは固定加算ではなく学習可能な重み付き合成で残差を構成し、54Mモデルでも検証Lossを0.3以上改善できる
- ゲート粒度は細かいほど（2層ごと）有効で、粗い設定（4層ごと）より汎化性能が高かった
- 実装はblock_outputsを蓄積しsoftmax集約後にhを置換する方式で、標準残差との差分が明確に測定可能

## 監査エージェントへの示唆

監査エージェントで使用するLLMのファインチューニングや軽量モデル構築時に、残差接続の改善手法として参照できる。特にLangGraphベースのマルチステップ推論では中間層の情報活用が精度に影響するため、Attention Residuals的なアプローチがエージェントの判断品質向上に寄与する可能性がある。

## 原文リンク

[TransformerでAttention Residualsを観察する](https://zenn.dev/ka_kan/articles/5307a3031fede6)
