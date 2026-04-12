---
title: "FTimeXer: 外生変数を組み込んだ周波数認識型時系列Transformerによるカーボンフットプリント予測"
url: "https://arxiv.org/abs/2604.02347"
date: 2026-04-09
tags: [時系列予測, Transformer, FFT, カーボンフットプリント, 外生変数, ロバスト学習, 周波数解析, マスキング正則化]
category: "ai-ml"
memo: "[arXiv cs.AI+cs.LG] FTimeXer: Frequency-aware Time-series Transformer with Exogenous variables for Robust Carbon Footprint Forecasting"
related: [1494, 113, 1185, 798, 869]
processed_at: "2026-04-09T12:16:41.560092"
---

## 要約

電力グリッドのカーボン強度（carbon intensity）予測は、製品カーボンフットプリント（PCF）会計や脱炭素化意思決定において不可欠だが、グリッドのカーボン強度は非定常性が高く、既存手法は周期的・振動的パターンの活用や、欠損・位置ずれといった不規則な外生変数への対応が弱いという課題があった。本論文ではこれらに対応するため、FTimeXer（Frequency-aware Time-series Transformer with Exogenous variables）を提案する。

アーキテクチャの核心は2点。第一に、FFT（高速フーリエ変換）を用いた周波数ブランチとゲーテッド時間-周波数融合機構により、マルチスケールの周期性を効果的に捉える。時間ドメインと周波数ドメインの両表現をゲート機構で動的に統合することで、単純なAttentionだけでは捉えにくい振動パターンを抽出する。第二に、確率的外生マスキング（stochastic exogenous masking）と一貫性正則化（consistency regularization）を組み合わせたロバストな学習スキームを採用する。これにより、外生変数が欠損・ずれた場合でも偽相関（spurious correlations）を抑制し、予測の安定性を高める。

3つの実世界データセット上で実験を行い、強力なベースラインに対して一貫した改善を達成。ETAI 2026（第5回エレクトロニクス技術・AI国際会議）に採択済み。電力グリッドのカーボン因子予測精度向上により、PCF会計の信頼性および脱炭素化に関する意思決定支援の質を改善できることを示した。技術的には、TimeXerなど既存の時系列Transformerに周波数認識と外生変数ロバスト性を付加した拡張として位置づけられる。

## アイデア

- FFTブランチとAttentionベースの時間ブランチをゲート融合する設計は、周期性が強いがノイズも多い時系列（監査ログ、財務指標等）への適用に転用可能
- 確率的外生マスキング＋一貫性正則化の組み合わせは、現実のデータパイプラインで頻発する欠損・遅延データへの汎用的なロバスト化手法として参考になる
- カーボン強度という非定常かつ外部要因依存の時系列を対象にすることで、環境規制対応（ESG報告・Scope3排出量計算）の自動化に直結するユースケースを開拓している
## 関連記事

- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_1185 HuggingFaceで始めるPatch Time Series Transformer（PatchTST）
- /deep_798 DySCo: 長期時系列予測のための動的意味圧縮フレームワーク
- /deep_869 DySCo: 効果的な長期時系列予測のための動的意味圧縮

## 原文リンク

[FTimeXer: 外生変数を組み込んだ周波数認識型時系列Transformerによるカーボンフットプリント予測](https://arxiv.org/abs/2604.02347)
