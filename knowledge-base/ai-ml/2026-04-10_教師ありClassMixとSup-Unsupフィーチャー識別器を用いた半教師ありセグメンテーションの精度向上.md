---
title: "教師ありClassMixとSup-Unsupフィーチャー識別器を用いた半教師ありセグメンテーションの精度向上"
url: "https://tldr.takara.ai/p/2604.07122"
date: 2026-04-10
tags: [semi-supervised-learning, semantic-segmentation, ClassMix, data-augmentation, adversarial-training, mIoU, 医療画像]
category: "ai-ml"
memo: "[HF Daily Papers] Accuracy Improvement of Semi-Supervised Segmentation Using Supervised ClassMix and Sup-Unsup Feature Discriminator"
processed_at: "2026-04-10T12:33:34.073807"
---

## 要約

セマンティックセグメンテーションにおけるピクセルレベルのアノテーション作成コストは非常に高く、少数の labeled データと大量の unlabeled データを組み合わせる半教師あり学習が注目されている。本研究は、既存手法 ClassMix の2つの課題を解決することを目的としている。

【ClassMix の課題】
ClassMix は unlabeled 画像から予測した疑似ラベルを他の画像に貼り付けるデータ拡張手法だが、(1) 疑似ラベルの不正確さによるノイズの混入、(2) labeled 画像と unlabeled 画像の品質ギャップによる特徴マップへの悪影響、という2つの問題を抱えている。

【提案手法1: Supervised ClassMix】
従来の ClassMix が unlabeled 画像の疑似ラベルを使用するのに対し、本手法では labeled 画像の正確なクラスラベルとそれに対応する画像領域を unlabeled 画像および疑似ラベル画像に貼り付ける。これにより、疑似ラベルの誤りが混入するリスクを排除し、データ拡張の品質を向上させる。

【提案手法2: Sup-Unsup Feature Discriminator】
labeled 画像と unlabeled 画像の間に存在する特徴マップの品質ギャップを縮小するため、識別器（Discriminator）を導入する。モデルが unlabeled 画像に対して行う予測を、labeled 画像に対する予測に近づけるよう学習させる。これは adversarial training の考え方を適用したもので、ドメインギャップの緩和に相当する。

【実験結果】
Chase データセット（網膜血管セグメンテーション）および COVID-19 データセット（医療画像セグメンテーション）を用いた実験において、従来の半教師あり学習手法と比較して mIoU（mean Intersection over Union）が平均 2.07% 向上した。

医療画像分野のような高コストアノテーション環境での適用を想定した実用的な改善であり、セグメンテーション精度の定量的な向上を示している。

## アイデア

- 正確な labeled データを使った Supervised ClassMix は、疑似ラベルノイズを原理的に排除する手法であり、品質保証が難しいラベリング環境での堅牢性向上のアプローチとして汎用性がある
- Sup-Unsup Feature Discriminator はドメイン適応の思想を半教師あり学習内部に組み込んだ設計であり、labeled/unlabeled のデータ分布ギャップを明示的にモデル化する点が新しい
- Chase・COVID-19 という異なるドメインの医療データセットで2.07%の mIoU 改善を達成しており、手法の汎化性を示している点が実用上重要

## 関連記事

- /deep_1575 ビジョントランスフォーマー（ViT）をHugging Face Optimum Graphcoreで活用する詳細ガイド
- /deep_153 バスク語方言リソースのカタログ：オンラインコレクションと標準語から方言への変換
- /deep_982 オフロードセマンティックセグメンテーションのためのトークン精錬付きクロススケールデコーダ
- /deep_1485 iTAG: 因果グラフアノテーション付き自然文生成のための逆設計手法
- /deep_1433 Vision-Language Modelによるディープアンローリングでパーソナライズ・高速MRIを実現

## 原文リンク

[教師ありClassMixとSup-Unsupフィーチャー識別器を用いた半教師ありセグメンテーションの精度向上](https://tldr.takara.ai/p/2604.07122)
