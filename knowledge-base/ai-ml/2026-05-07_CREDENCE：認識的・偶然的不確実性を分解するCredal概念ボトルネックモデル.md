---
title: "CREDENCE：認識的・偶然的不確実性を分解するCredal概念ボトルネックモデル"
url: "https://tldr.takara.ai/p/2604.24170"
date: 2026-05-07
tags: [Concept Bottleneck Models, 不確実性定量化, Credal Sets, epistemic uncertainty, aleatoric uncertainty, 解釈可能AI, アンサンブル学習]
category: "ai-ml"
related: [1429, 3654, 113, 1701, 2698]
memo: "[HF Daily Papers] Credal Concept Bottleneck Models for Epistemic-Aleatoric Uncertainty Decomposition"
processed_at: "2026-05-07T12:21:03.392288"
---

## 要約

Concept Bottleneck Models（CBM）は、人間が解釈可能な「概念」を経由して予測を行うニューラルネットワーク手法だが、従来のCBMは各概念の確率を点推定で出力するため、2種類の不確実性を混同してしまう問題があった。1つ目は「認識的不確実性（epistemic uncertainty）」で、モデルの学習不足や訓練データの不足から生じる「削減可能」な不確実性。2つ目は「偶然的不確実性（aleatoric uncertainty）」で、入力データそのものの曖昧さ（アノテーター間の意見不一致など）に起因する「削減不可能」な不確実性。この2種類を区別できなければ、不確実性を実際の意思決定に活かすことが難しい。

本論文はCREDENCE（Credal Ensemble Concept Estimation）というフレームワークを提案する。CREDENCEでは各概念をcredal予測（確率区間）として表現する。これはベイズ集合論的確率論（Credal Sets理論）に基づき、単一の確率値ではなく「下限～上限」の区間で概念の確率を表す。認識的不確実性は、互いに多様に学習された複数の「概念ヘッド（concept heads）」間の予測の不一致度から導出する。偶然的不確実性は、アノテーターの意見不一致データが利用可能な場合にそれに合致するよう学習された専用の「曖昧性出力」から推定する。

この分解により、具体的な意思決定ルールが得られる：①両不確実性が低いケースは自動判定、②認識的不確実性が高いケースはデータ追加収集を優先、③偶然的不確実性が高いケースは人間レビューへルーティング、④両方が高い場合は判定を棄権（abstain）する。複数のタスクでの実験により、認識的不確実性は予測エラーと正の相関を持ち、偶然的不確実性はアノテーター不一致率を精度よく追跡することを確認した。実装はGitHub（Tankiit/Credal_Sets）で公開済み。監査AIへの応用として、高リスク判断の自動化と人間へのエスカレーション基準の設計に直接活用できる枠組みを提供する。

## アイデア

- 確率区間（credal prediction）という表現により、単一確率値では捉えられない「モデルが何を知らないか」と「データ自体が曖昧か」を構造的に分離できる点は、監査判断の自動化・エスカレーション設計に直接応用可能
- 複数の多様な概念ヘッドの不一致を認識的不確実性の代理指標として使う手法は、LLM-as-judgeにおける複数モデルアンサンブルによる信頼度推定と類似しており、エージェントシステムの判断品質評価に転用できる
- 偶然的不確実性をアノテーター不一致データで直接監督学習する設計は、ヒューマンフィードバック（RLHF/RLAIF）において「ラベルノイズ」と「真の曖昧さ」を区別するための新たな視点を与える

## 前提知識

- **Concept Bottleneck Models（CBM）** (TODO: 読むべき)
- **Credal Sets理論** (TODO: 読むべき)
- **epistemic/aleatoric uncertainty** (TODO: 読むべき)
- **アンサンブル学習** → /deep_97 AIトレーダー開発ログ #2: Paper Tradingで検証したQuant型アーキテクチャの有効性
- **不確実性定量化（UQ）** (TODO: 読むべき)

## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_3654 電気自動車充電需要の時空間モデリング：スコットランド大規模データセットとINLAによるベイズ推論
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_1701 近傍点を用いた高スケーラブルなガウス過程回帰の理論と実践
- /deep_2698 説明可能な金融不正検知のためのShapley値ガイド型適応アンサンブル学習と米国規制コンプライアンス検証

## 原文リンク

[CREDENCE：認識的・偶然的不確実性を分解するCredal概念ボトルネックモデル](https://tldr.takara.ai/p/2604.24170)
