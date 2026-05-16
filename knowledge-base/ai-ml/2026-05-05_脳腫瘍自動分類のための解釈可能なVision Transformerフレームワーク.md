---
title: "脳腫瘍自動分類のための解釈可能なVision Transformerフレームワーク"
url: "https://tldr.takara.ai/p/2604.21311"
date: 2026-05-05
tags: [Vision Transformer, ViT-B/16, 脳腫瘍分類, MRI, CLAHE, Attention Rollout, MixUp, CutMix, EMA, TTA, 医療画像, XAI]
category: "ai-ml"
related: [1575, 1433, 1760, 456, 747]
memo: "[HF Daily Papers] an interpretable vision transformer framework for automated brain tumor classification"
processed_at: "2026-05-05T12:11:54.194129"
---

## 要約

本論文は、MRI画像から脳腫瘍を自動的に4クラス（神経膠腫・髄膜腫・下垂体腫瘍・健常脳）に分類する深層学習フレームワークを提案する。バックボーンにはImageNet-21kで事前学習済みのViT-B/16（Vision Transformer）を採用し、7,023枚のMRIスキャンデータセットで評価している。

前処理としてCLAHE（Contrast Limited Adaptive Histogram Equalization）を適用し、標準的な正規化では見えにくい腫瘍境界のローカルコントラストを強調する。ファインチューニングは2段階で実施：まずバックボーンを凍結した状態で分類ヘッドをウォームアップし、次に識別的学習率（層ごとに異なるLRを設定）で全体をファインチューニングする。

データ拡張にはMixUpとCutMixをバッチ単位で適用し、過学習を抑制しつつ汎化性能を向上させる。推論安定性の向上にはEMA（Exponential Moving Average）による重み平滑化と、TTA（Test-Time Augmentation）を組み合わせる。

解釈可能性の面では、Attention Rolloutによるヒートマップ可視化を実装し、各予測においてモデルが注目した脳領域を臨床医が確認できる形で提示する。これにより「なぜその診断か」の根拠を画像として示すことができる。

結果として、テスト精度99.29%、マクロF1スコア99.25%を達成し、健常クラスと髄膜腫クラスでは再現率100%を記録。CNN系ベースラインをすべて上回った。CLAHEによる前処理・2段階ファインチューニング・EMA+TTAの組み合わせが、医療画像分類における高精度と解釈可能性の両立を実現した好例として位置づけられる。監査エージェント開発への示唆としては、AIの判断根拠を可視化するAttention Rollout的なアプローチ（説明可能性モジュール）は、監査AIが「なぜこの取引をリスクと判断したか」を内部監査人に提示する設計に直接応用できる。

## アイデア

- Attention Rolloutによるヒートマップ可視化は、医療診断に留まらず監査AIの判断根拠説明（なぜこの取引がリスクか）に転用できる説明可能性パターンとして有用
- 2段階ファインチューニング（ヘッド固定→識別的LRで全体）は少量ドメインデータへの転移学習の定石として、監査ドメイン特化モデル構築時にも参考になる
- CLAHEのような前処理によるドメイン特化的なコントラスト強調が最終精度に大きく寄与している点は、画像以外のドメイン（財務数値の異常強調など）への類推が可能

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Transfer Learning** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **Attention Rollout** (TODO: 読むべき)
- **MixUp / CutMix** (TODO: 読むべき)
- **EMA (Exponential Moving Average)** (TODO: 読むべき)

## 関連記事

- /deep_1575 ビジョントランスフォーマー（ViT）をHugging Face Optimum Graphcoreで活用する詳細ガイド
- /deep_1433 Vision-Language Modelによるディープアンローリングでパーソナライズ・高速MRIを実現
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_456 視覚的 vs テキスト形式：教育推薦システムにおける説明形式と個人特性が説明の知覚に与える影響
- /deep_747 異種媒体における波の反射・透過予測：フーリエ演算子ベースのTransformerモデリング

## 原文リンク

[脳腫瘍自動分類のための解釈可能なVision Transformerフレームワーク](https://tldr.takara.ai/p/2604.21311)
