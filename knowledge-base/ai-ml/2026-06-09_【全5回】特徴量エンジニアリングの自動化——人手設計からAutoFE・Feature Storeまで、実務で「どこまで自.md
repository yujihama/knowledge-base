---
title: "【全5回】特徴量エンジニアリングの自動化——人手設計からAutoFE・Feature Storeまで、実務で「どこまで自動化するか」を決める"
url: "https://zenn.dev/salt2/articles/automated-feature-engineering-20260609"
date: 2026-06-09
tags: [AutoFE, 特徴量エンジニアリング, DFS, featuretools, Feature Store, LassoNet, TabNet, 強化学習, MLOps, タブラーデータ]
category: "ai-ml"
related: [327, 5572, 1429, 2419, 1645]
memo: "[Zenn 機械学習] 【全5回】特徴量エンジニアリングの自動化——人手設計からAutoFE・Feature Storeまで、実務で「どこまで自動化するか」を決める"
processed_at: "2026-06-09T09:10:21.785061"
---

## 要約

本シリーズ（全5回）は、テーブル（タブラー）データを対象とした特徴量エンジニアリングの自動化を体系的に解説するZenn Booksである。単にAutoFEツールの使い方を紹介するのではなく、「なぜその手法が生まれたか」という課題背景から積み上げる構成を採用している。

第1回は基礎として、特徴量エンジニアリングの定義と人手設計の原則を整理する。木ベースモデル（XGBoost、LightGBM等）において人手特徴量が今も有効な理由や、小データ環境での効き方を解説し、autofeatを例に人手設計の限界と自動化の動機を示す。

第2回はAutoFE研究の礎であるDeep Feature Synthesis（DFS）を解説する。featuretoolsライブラリを使い、リレーショナルデータをJOIN＋集約で特徴量に変換する「深さ優先」アルゴリズムの仕組みと、その強み・限界を原点から押さえる。

第3回は特徴量選択の3分類——フィルタ法・Wrapper法・埋め込み法——を扱う。大量生成された特徴量から有用なものを絞り込む手法として、Lasso、LassoNet、TabNet、Borutaまでを取り上げ、各手法の課題意識から仕組みを掘り下げる。

第4回はAutoFEの最前線として、強化学習（NFS・DIFER）、GNN（グラフニューラルネットワーク）、Transformer/LLMという3潮流がルールベースのDFSをどう乗り越えてきたかを俯瞰する。「生成」と「選択」がEnd-to-end化していく流れを示す。

第5回は運用基盤としてのFeature Storeを扱う。MetaのLooper、Uberのマーケットプレイス最適化といった産業界の実装事例をもとに、特徴量の管理・再利用・本番環境への一貫提供を設計する方法を解説する。Training–Serving Skewやデータリークへの対処も含む。

監査エージェント開発への示唆：大量のログ・取引データから特徴量を自動生成・選択するパイプラインは、監査エージェントの異常検知モジュールに直接応用できる。特にDFS（featuretools）によるリレーショナルデータの自動集約は、ERP・会計データの構造と親和性が高く、Feature Storeによる特徴量バージョン管理はモデル監査証跡の一部として活用できる。

## アイデア

- DFS（Deep Feature Synthesis）はリレーショナルDBのJOIN構造をそのまま特徴量生成グラフとして扱う発想で、ERP・会計データのような多テーブル構造に直接適用できる点が実務上重要
- 特徴量選択をフィルタ・Wrapper・埋め込みの3分類で整理することで、計算コストと選択精度のトレードオフを明示的に設計できる——Borutaのようなシャドウ変数ベースの手法は偽陽性を統計的に制御できる
- Feature StoreにおけるTraining–Serving Skew問題（学習時と推論時で特徴量の計算ロジックがずれる）は、MLシステムの本番障害の主要因であり、MetaのLooperのような中央管理基盤がその解法として機能する

## 前提知識

- **DFS / featuretools** (TODO: 読むべき)
- **Lasso / 正則化** (TODO: 読むべき)
- **TabNet** (TODO: 読むべき)
- **Feature Store** → /deep_4194 Snowflake Online Feature Serving で作るリアルタイムレコメンデーション - Two-Tower ネットワーク
- **強化学習 (RL)** (TODO: 読むべき)

## 関連記事

- /deep_327 音響プロファイリングによるデータ駆動型塑性変形モデリング
- /deep_5572 非マルコフ強化学習のためのPolicy Gradient手法
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_2419 電力グリッド運用のための実行時安全シールドを備えた階層型強化学習
- /deep_1645 雰囲気でML運用してない？Google流「ML Test Score」でMLパイプラインの信頼性を数値化する

## 原文リンク

[【全5回】特徴量エンジニアリングの自動化——人手設計からAutoFE・Feature Storeまで、実務で「どこまで自動化するか」を決める](https://zenn.dev/salt2/articles/automated-feature-engineering-20260609)
