---
title: "RADS: 強化学習ベースのサンプル選択が低リソース・不均衡な臨床設定でのTransfer Learningを改善する"
url: "https://tldr.takara.ai/p/2604.20256"
date: 2026-04-30
tags: [強化学習, サンプル選択, Transfer Learning, Few-shot Fine-tuning, クラス不均衡, Active Learning, 臨床NLP, 低リソース学習]
category: "ai-ml"
related: [1760, 2419, 2007, 1611, 1605]
memo: "[HF Daily Papers] RADS: Reinforcement Learning-Based Sample Selection Improves Transfer Learning in Low-resource and Imbalanced Clinical Settings"
processed_at: "2026-04-30T12:25:00.145793"
---

## 要約

RADS（Reinforcement Adaptive Domain Sampling）は、医療・臨床テキスト分類のような「極端なデータ不足＋クラス不均衡」環境でのTransfer Learningを改善するためのサンプル選択手法。従来のFew-shot Fine-tuningでは、訓練例として選ぶサンプルの質が最終精度を大きく左右するが、不確実性サンプリング（Uncertainty Sampling）や多様性サンプリング（Diversity Sampling）などのActive Learning手法は、極端なリソース不足やクラス不均衡下では外れ値（outlier）を優先的に選んでしまい、性能が劣化するという問題があった。RADSはこの問題を強化学習（RL）で解決する。具体的には、エージェントがサンプル選択ポリシーを学習し、モデルの転移性（transferability）を高める最も情報量の高いサンプルを反復的に特定する仕組みを持つ。報酬設計はモデルの汎化性能に基づいており、クラス不均衡に対してもロバストな選択が可能になる。実験は複数の実世界臨床データセットで行われ、従来手法と比較してクラス不均衡下でのモデル性能を維持しつつ転移可能性を向上させることを確認した。著者陣はRMIT大学などに所属するLawrence CavedonらのNLP×医療領域の研究者グループ。この手法は医療記録のような希少疾患カテゴリを含むテキスト分類タスクに特に有効であり、Few-shot設定における訓練データ品質の重要性を定量的に示している点が実用上の価値となる。監査エージェント開発への示唆として、内部監査ログや異常取引検知のように「異常クラスが極端に少ない」タスクへのFine-tuningにおいて、RLベースのサンプル選択をデータ収集・ラベリング戦略に組み込むことで、限られたアノテーションコストでより高精度なモデルを実現できる可能性がある。

## アイデア

- 不確実性サンプリングや多様性サンプリングが低リソース環境で外れ値を選びやすいという既知の問題を、RLの報酬設計で直接最適化することで解消している点が構造的に面白い
- サンプル選択自体をRLエージェントの意思決定問題として定式化することで、ヒューリスティックなActive Learning手法の限界を超えるアプローチは、データ収集コストが高い専門ドメイン全般に応用可能
- クラス不均衡と低リソースという2つの制約を同時に扱う設計は、医療・法務・監査など「異常が稀で正解ラベルが高コスト」な実務ドメインに直接転用できる

## 前提知識

- **Transfer Learning** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **Few-shot Fine-tuning** (TODO: 読むべき)
- **Active Learning** → /deep_2760 一様サンプリングを超えて：ロバストなニューラル演算子のための協調的アクティブラーニングと入力ノイズ除去
- **強化学習（Policy Gradient）** (TODO: 読むべき)
- **クラス不均衡対策** (TODO: 読むべき)

## 関連記事

- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_2419 電力グリッド運用のための実行時安全シールドを備えた階層型強化学習
- /deep_2007 連続時間ジャンプ拡散制御のためのActor-Criticフレームワーク：Normalizing Flowsによる実装
- /deep_1611 近接方策最適化（PPO）：方策更新を安定させるクリッピング手法
- /deep_1605 賢明に行動せよ：エージェント型マルチモーダルモデルにおけるメタ認知的ツール使用の育成

## 原文リンク

[RADS: 強化学習ベースのサンプル選択が低リソース・不均衡な臨床設定でのTransfer Learningを改善する](https://tldr.takara.ai/p/2604.20256)
