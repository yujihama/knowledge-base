---
title: "LLM評価はギャンブルだった — promptstatsで始める統計的評価"
url: "https://zenn.dev/beckento/articles/b5e33b92cdd084"
date: 2026-03-29
tags: [LLM評価, 統計的検定, promptstats, Bootstrap信頼区間, Wilcoxon検定, 混合効果モデル, プロンプトエンジニアリング, LLM-as-a-Judge]
category: "ai-ml"
memo: "[Zenn 機械学習] LLM評価はギャンブルだった — promptstatsで始める統計的評価"
processed_at: "2026-03-29T22:22:38.647512"
---

## 要約

フロンティアモデルの性能が拮抗する現在、平均スコアの比較だけではLLM評価が事実上のコイントスになることを示した記事。真の能力差0.02のモデルを単一評価した場合、劣るモデルが勝つ確率は約40%に達し、30プロンプト平均でも約9%の誤判定率が残る。これに対しPythonライブラリ「promptstats」を用いてBootstrapリサンプリングによる95%信頼区間の可視化、Wilcoxon符号順位検定・Friedman検定によるペアワイズ有意差判定、線形混合効果モデル（LMM）でのプロンプト×モデル交互作用分析を行う手法を解説。信頼区間の重なりによって「今のデータ量で結論を出せるか否か」を定量的に判断できる。LLM-as-a-Judgeの評価者間信頼性（Cohen's κ等）や検定力分析は自前実装が必要な点も明示。

## 要点

- 性能が拮抗するフロンティアモデルの比較では、単一評価の誤判定率は約40%でありほぼコイントスに等しい
- promptstatsはBootstrap CI・ペアワイズ検定・noise plot・LMMを提供し、「統計的に有意な差か否か」を定量判定できる
- LLM-as-a-Judgeの評価者間信頼性（Cohen's κ）や検定力分析はpromptstatsの対象外であり別途実装が必要

## 監査エージェントへの示唆

監査エージェントのプロンプト比較やモデル選定において、平均スコアだけでなく信頼区間と有意差検定を用いることで、誤判定リスクを定量化できる。安全性テストの失敗率評価には二項検定・exact binomial CIの自前実装が必要であり、監査品質の担保に直結する。

## 原文リンク

[LLM評価はギャンブルだった — promptstatsで始める統計的評価](https://zenn.dev/beckento/articles/b5e33b92cdd084)
