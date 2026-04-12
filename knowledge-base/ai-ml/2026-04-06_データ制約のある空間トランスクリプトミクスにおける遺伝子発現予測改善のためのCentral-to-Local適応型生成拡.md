---
title: "データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク"
url: "https://arxiv.org/abs/2603.26827"
date: 2026-04-06
tags: [diffusion model, spatial transcriptomics, data augmentation, transfer learning, gene expression prediction, histopathology, few-shot adaptation]
category: "ai-ml"
memo: "[arXiv cs.AI+cs.LG] Central-to-Local Adaptive Generative Diffusion Framework for Improving Gene Expression Prediction in Data-Limited Spatial Transcriptomics"
related: [1476, 1689]
processed_at: "2026-04-06T12:05:05.385544"
---

## 要約

空間トランスクリプトミクス（ST）は、組織内の空間的な遺伝子発現プロファイルを取得する技術だが、高コスト・低スループット・データ共有の制約により訓練データが極めて乏しい。本論文はこの問題に対し、C2L-ST（Central-to-Local adaptive generative diffusion framework for ST）を提案する。

アーキテクチャの核心は2段階の適応学習にある。第1段階では、大規模な病理組織学データセット上でグローバルな「セントラルモデル」を事前学習し、転移可能な形態学的表現を獲得する。第2段階では、少数の画像-遺伝子ペアスポットのみを用いて、軽量な遺伝子条件付きモジュレーション（gene-conditioned modulation）により機関固有の「ローカルモデル」に適応させる。この戦略により、データが乏しい条件下でも分子的一貫性を持つ病理組織パッチの合成が可能になる。

拡散モデルを生成基盤として使用し、合成された画像は高い視覚的・構造的忠実度を示し、細胞組成を再現し、複数の臓器において実データとの埋め込み空間上の重複が確認されている。生成した合成画像-遺伝子ペアを下流の遺伝子発現予測モデルの訓練に組み込むと、予測精度と空間的一貫性が向上し、実データのごく一部のスポット数のみで実データと同等の性能を達成した。

論文では31ページ・12図にわたって実験が報告されており、現在査読中（under review）の状態。提案手法は、ドメイン適応型・汎化可能なデータ拡張フレームワークとして、空間生物学と組織学・トランスクリプトミクス統合の両分野への応用が想定されている。

## アイデア

- 「セントラルモデルで大規模データから表現を学習し、ローカルモデルで少数ペアに適応」というCentral-to-Local構造は、データ希少領域への拡散モデル適用の汎用パターンとして興味深い
- 遺伝子条件付けモジュレーションにより生成画像の分子的一貫性を担保する設計は、生成モデルにドメイン固有の制約を埋め込む手法として参考になる
- 合成データを下流タスクの訓練に組み込みパフォーマンスを向上させるアプローチは、医療・専門ドメインにおけるデータ拡張戦略として応用範囲が広い

## 関連記事

- /deep_1476 高忠実度画像圧縮のためのノイズ制約拡散（NC-Diffusion）フレームワーク
- /deep_1689 Car-GPT: LLMは自動運転を実現できるか？

## 原文リンク

[データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク](https://arxiv.org/abs/2603.26827)
