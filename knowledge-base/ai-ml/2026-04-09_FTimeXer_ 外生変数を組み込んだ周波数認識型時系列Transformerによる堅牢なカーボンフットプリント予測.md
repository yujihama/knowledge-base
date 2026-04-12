---
title: "FTimeXer: 外生変数を組み込んだ周波数認識型時系列Transformerによる堅牢なカーボンフットプリント予測"
url: "https://arxiv.org/abs/2604.02347"
date: 2026-04-09
tags: [Transformer, 時系列予測, FFT, カーボンフットプリント, 外生変数, 周波数領域, non-stationarity, consistency regularization]
category: "ai-ml"
memo: "[arXiv cs.AI+cs.LG] FTimeXer: Frequency-aware Time-series Transformer with Exogenous variables for Robust Carbon Footprint Forecasting"
related: [1494, 113, 1185, 798, 869]
processed_at: "2026-04-09T12:47:05.349377"
---

## 要約

電力グリッドのカーボン強度（carbon intensity）を正確に予測することは、製品カーボンフットプリント（PCF）会計や脱炭素化意思決定において重要だが、グリッドのカーボン強度は高い非定常性を示し、周期・振動パターンの活用が難しく、欠損データや時間的ずれを含む外生変数への対応も既存手法では不十分だった。本論文はこれらの課題に対応するため、FTimeXer（Frequency-aware Time-series Transformer with Exogenous variables）を提案する。

FTimeXerの主要な技術的構成は2点ある。第一に、高速フーリエ変換（FFT）駆動の周波数ブランチとゲーテッド時間-周波数フュージョン機構を組み合わせることで、マルチスケールの周期性を効果的に捉える。FFTにより時系列を周波数領域に変換し、複数のスケールで周期的パターンを抽出したうえで、ゲーティング機構により時間ドメインと周波数ドメインの情報を適応的に統合する。第二に、確率的外生マスキング（stochastic exogenous masking）と一貫性正則化（consistency regularization）を組み合わせたロバストな学習スキームを採用する。外生変数の一部をランダムにマスクしながら学習することで、特定の外生変数への過度な依存（spurious correlations）を抑制し、欠損・ずれのある外生入力に対しても安定した予測を実現する。

3つの実世界データセットを用いた実験で、強力なベースラインに対して一貫した改善を示した。本手法はETAI 2026（第5回電子技術・人工知能国際会議）に採択されている。カーボン強度予測の精度向上により、サプライチェーン全体でのPCF会計の信頼性向上や、再生可能エネルギー調達タイミングの最適化などへの応用が期待される。

## アイデア

- 確率的マスキング＋一貫性正則化の組み合わせによるロバスト学習スキームは、欠損・不整合データが常態化する実務データへの対応策として汎用性が高い
- FFT駆動の周波数ブランチとゲーテッド時間-周波数フュージョンによるマルチスケール周期性の抽出は、外部指標（経済指標・規制サイクル等）が混在する複雑な時系列モデリングに応用可能
- 外生変数の不規則入力（欠損・ずれ）への明示的な対処をモデルアーキテクチャレベルで組み込む設計思想は、実環境データを扱う予測システム全般に参考になる
## 関連記事

- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_1185 HuggingFaceで始めるPatch Time Series Transformer（PatchTST）
- /deep_798 DySCo: 長期時系列予測のための動的意味圧縮フレームワーク
- /deep_869 DySCo: 効果的な長期時系列予測のための動的意味圧縮

## 原文リンク

[FTimeXer: 外生変数を組み込んだ周波数認識型時系列Transformerによる堅牢なカーボンフットプリント予測](https://arxiv.org/abs/2604.02347)
