---
title: "エントロピー正則化強化学習におけるWasserstein方策勾配の大域収束"
url: "https://tldr.takara.ai/p/2605.26078"
date: 2026-05-27
tags: [Wasserstein Policy Gradient, エントロピー正則化RL, 最適輸送, Bellman収縮, Langevin拡散, Polyak-Łojasiewicz条件, 対数Sobolev不等式]
category: "ai-ml"
related: [1178, 6161, 4936, 5486, 3754]
memo: "[HF Daily Papers] Global Convergence of Wasserstein Policy Gradient for Entropy-Regularized Reinforcement Learning"
processed_at: "2026-05-27T09:11:33.361789"
---

## 要約

本論文は、連続制御問題向けの方策最適化手法であるWasserstein Policy Gradient（WPG）に対して、エントロピー正則化強化学習（RL）目的関数のもとでの大域収束理論を構築した研究である。

WPGは最適輸送（Optimal Transport）の幾何学、具体的にはWasserstein距離を用いて行動分布を最適化する手法で、各状態条件付き方策をsoft Q関数の行動勾配方向に輸送しつつ、Langevin型拡散を組み合わせて更新する。連続行動空間での表現力に優れる一方、大域収束の理論的保証が不明確であった。

従来のLangevin拡散の解析が直接適用できない理由は2点ある。第一に、RL目的関数がBellman再帰を通じて方策に依存しており、静的な凸汎関数ではない。第二に、Langevin項のドリフトはsoft Q関数によって決まるが、方策の更新に伴うその正則性の管理が困難である。

著者らはこれらの課題をBellman構造を活用することで克服した。具体的には3つの鍵となる論拠を組み合わせている。①soft Bellman残差がGibbs方策に対する状態ごとのKL表現を持つこと、②Bellman縮小写像がこの残差を大域最適性ギャップに結びつけること、③Bellman resolvent恒等式が価値改善を相対Fisher情報に接続すること。

これら3要素と、更新するGibbs族に対する一様対数Sobolev不等式（LSI）を組み合わせることで、分布的なPolyak–Łojasiewicz（PL）条件を導出した。PL条件は凸性を仮定せずに線形収束速度を保証する条件であり、強化学習では通常期待できない凸性の代替として機能する。さらに離散化誤差を制御するための正則性と一様有界性も確立し、離散化バイアスまでの幾何級数的収縮（geometric contraction）を得た。

概念的な貢献として、エントロピー正則化RLが通常の意味では凸でないにもかかわらず、Bellman再帰が有利なPL型幾何構造を誘導し、WPGの大域収束を支えることを明示した。これはPPOやGRPO等のRL方策最適化に数学的基盤を与える方向性として重要であり、監査エージェント開発における複数ステップ意思決定の信頼性理論にも示唆を持つ。

## アイデア

- Bellman再帰構造をPL条件の代替として活用することで、非凸なRL目的関数に対して大域収束を証明できるという数学的フレームワークは、PPO・GRPO等の実用的アルゴリズムの理論的裏付けにも応用可能
- Wasserstein距離ベースの方策更新は、連続行動空間において分布の形状変化を輸送コストで評価できるため、離散トークン空間を前提とするKLベース手法では捉えられない最適化の幾何を活用できる
- soft Q関数の正則性をBellman resolvent恒等式とFisher情報で制御する手法は、値関数近似を使うactor-criticアーキテクチャの収束解析に向けた理論的足場として応用可能

## 前提知識

- **Bellman方程式** (TODO: 読むべき)
- **エントロピー正則化RL** (TODO: 読むべき)
- **Wasserstein距離** → /deep_630 ガウス混合モデル間のフローマッチングにおける明示的サロゲートとWasserstein誤差境界
- **Langevin MCMC** (TODO: 読むべき)
- **Polyak-Łojasiewicz条件** (TODO: 読むべき)

## 関連記事

- /deep_1178 確率測度のワッサースタイン空間におけるランダム座標降下法
- /deep_6161 球面調和関数を用いた最適輸送：気候モデル比較への応用
- /deep_4936 機械学習研究における数学の変化する役割：形状・対称性・構造
- /deep_5486 機械学習研究における数学の変化する役割：形状・対称性・構造
- /deep_3754 形状・対称性・構造：機械学習研究における数学の役割の変容

## 原文リンク

[エントロピー正則化強化学習におけるWasserstein方策勾配の大域収束](https://tldr.takara.ai/p/2605.26078)
