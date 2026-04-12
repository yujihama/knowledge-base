---
title: "Le MuMo JEPA：学習可能な融合トークンによるマルチモーダル自己教師あり表現学習"
url: "https://tldr.takara.ai/p/2603.24327"
date: 2026-04-05
tags: [self-supervised-learning, multi-modal, JEPA, LiDAR, transformer, representation-learning, SIGReg, fusion-tokens]
category: "ai-ml"
memo: "[HF Daily Papers] Le MuMo JEPA: Multi-Modal Self-Supervised Representation Learning with Learnable Fusion Tokens"
related: [499, 364, 504, 225, 1494]
processed_at: "2026-04-05T12:03:44.604506"
---

## 要約

Le MuMo JEPAは、RGB画像と他のモダリティ（LiDAR深度、熱画像など）から統合表現を自己教師あり学習するフレームワーク。既存のLeJEPAをマルチモーダル設定に拡張したもので、共有トランスフォーマー内にモダリティ固有のパッチステムと、それらの間でレイテントボトルネックとして機能する「融合トークン」を組み合わせた構造を持つ。

核心的な技術は「プルーニング融合戦略」にある。最初のクロスモーダルアテンション層の後にモダリティ固有トークンを除去し、クロスモーダル情報を共有の融合トークングリッドに圧縮する。その後、Sketched Isotropic Gaussian Regularization（SIGReg）を結合マルチモーダルCLS埋め込みに適用することで表現の正則化を行う。

実験は主に自動運転データセットで実施。Waymoデータセットでは、スクラッチからのマルチモーダルベースライン群の中でパフォーマンスと効率のトレードオフが最良で、CenterNet物体検出と密度深度推定を改善しつつ、セグメンテーションでも競争力を維持。nuScenesにおけるスクラッチ学習でも最強モデルとなり、Teledyne FLIR ADASベンチマーク（RGB-熱画像）でもWaymoで事前学習後のファインチューニングにより最良の結果を達成。計算量・メモリ・推定学習時間いずれも大幅に削減しながら最高の精度効率バランスを実現している。

アノテーションなしで複数センサーからの補完的情報を活用できる点が核心的な価値であり、センサーフュージョンが必要なロボティクスや自動運転領域での基盤モデル構築に実用的な示唆を持つ。

## アイデア

- 融合トークンをレイテントボトルネックとして使うことで、モダリティ固有情報を捨てずに効率的なクロスモーダル統合を実現する設計思想
- プルーニング（モダリティトークンの途中破棄）により計算コストを削減しながら表現品質を維持できることの実証
- SIGRegによるCLS埋め込みの正則化がマルチモーダル設定での過適合防止に機能している点
## 関連記事

- /deep_499 自己教師あり表現学習のためのガウス結合埋め込み（GJE/GMJE）
- /deep_364 患者適応型トランスフォーマーネットワークを用いたてんかん発作予測
- /deep_504 患者適応型トランスフォーマーネットワークを用いたてんかん発作予測
- /deep_225 LeWorldModel入門: 15Mパラメータで実現するJEPAベースWorld Model
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Le MuMo JEPA：学習可能な融合トークンによるマルチモーダル自己教師あり表現学習](https://tldr.takara.ai/p/2603.24327)
