---
title: "OptunaとLLMを組み合わせたハイパーパラメータ最適化の比較実験"
url: "https://zenn.dev/ka_kan/articles/b2675626c64180"
date: 2026-03-29
tags: [Optuna, LLM, ハイパーパラメータ最適化, TPE, RandomForest, OpenRouter, 不正検知]
category: "ai-ml"
memo: "[Zenn LLM] OptunaとLLMを組み合わせるとどうなるかを観察する"
processed_at: "2026-03-29T22:08:35.022992"
---

## 要約

LLMをOptunaのオーケストレーターとして活用し、サイクルごとに探索範囲の更新と収束判断を行わせる実験。クレジットカード不正検知（OpenML #1597）のRandomForestClassifierをF1で最適化し、Optuna単体とClaude Sonnet 4・Gemini 2.5 Flash・GPT-4o mini・Llama 4 Scoutの4モデルを比較。結果はOptuna単体がF1=0.8962で最高、LLM条件ではClaude Sonnet 4が0.8852で最良だったが全モデルでOptuna単体を下回った。根本原因はOptunaのTPEアルゴリズムがtrial蓄積から内部的に探索分布を更新する設計であり、LLMによる外部からの探索範囲上書きと競合した点にある。LLMの強みを活かすには数値パラメータの範囲絞り込みではなく、ドメイン知識を要する特徴量選択への介入やベースをランダムサーチにする設計が適切との考察を示した。

## 要点

- OptunaのTPEはtrial蓄積で内部的に探索分布を更新するため、LLMによる探索範囲の外部上書きと設計上競合し、Optuna単体より性能が低下した
- LLM条件ではGPT-4o miniが65trialと最多で収束せず、Llama 4 Scoutが13trialで最速収束するなどモデル間で挙動が大きく異なった
- LLMをOptunaと組み合わせる場合、数値パラメータの範囲絞り込みより特徴量選択等のドメイン知識依存タスクに役割を限定する設計が適切

## 監査エージェントへの示唆

監査エージェントでLLMをオーケストレーターとして使う際、既存の最適化アルゴリズム（TPE等）と役割が競合しないよう設計分離が必要。LLMはドメイン知識を要する判断（監査手続の選択・リスク評価の優先順位付け）に集中させ、数値的な探索はアルゴリズムに委ねる役割分担が有効。

## 原文リンク

[OptunaとLLMを組み合わせたハイパーパラメータ最適化の比較実験](https://zenn.dev/ka_kan/articles/b2675626c64180)
