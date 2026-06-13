---
title: "表形式データ拡張手法 part23：SMOTE-LOF"
url: "https://zenn.dev/haruto_big6/articles/51c82a7061240d"
date: 2026-06-13
tags: [SMOTE, LOF, クラス不均衡, データ拡張, 外れ値検出, 表形式データ, オーバーサンプリング]
category: "ai-ml"
related: [6317, 6493, 6206, 8154, 6761]
memo: "[Zenn 機械学習] 表形式データ拡張手法 part23：SMOTE-LOF"
processed_at: "2026-06-13T09:09:23.109410"
---

## 要約

表形式データにおけるクラス不均衡問題を解決する手法として、SMOTE-LOF（SMOTE + Local Outlier Factor）を解説した記事。

SMOTEは少数クラスデータをk近傍点間の補間で合成するが、多数クラスデータの分布を考慮しないため、生成データが多数クラス領域内に混入するリスクがある。これに対処するアプローチは2種類あり、①事前に少数クラスからノイズを除去する（Borderline-SMOTEなど）、②生成後にノイズを除去する（SMOTEENN、SMOTE-LOFなど）。SMOTE-LOFは後者の後処理アプローチを採用する。

LOF（Local Outlier Factor）の仕組みは以下の通り。まず点xとoの間のreachability distanceをreach_dist_k(x, o) = Max(k_dist(o), dist(x, o))で定義する。k_dist(o)はoのk番目近傍までの距離で、これによりo周辺のデータ分布を考慮した距離指標となる。次に、xのk近傍点全体に対するreach_distの平均の逆数として局所到達可能密度lrd(x)を算出する（lrd(x) = k / Σreach_dist(x, o)）。lrd(x)が大きいほどx周辺の密度が高いことを意味する。最終的なLOFスコアは、xのk近傍点oにおけるlrd(o)/lrd(x)の比率の平均として定義され（lof(x) = Σ(lrd(o)/lrd(x)) / k）、lof(x)が1より大きいほどxは外れ値である可能性が高い。密疎混在クラスターでも相対比較により閾値問題を回避できる点が特徴。

SMOTE-LOFのアルゴリズムは4ステップ。①SMOTEで少数クラスを拡張、②少数クラスデータ全体（元データ＋拡張データ）を標準化、③LOFスコアを計算、④スコアが閾値を超える拡張データのみを除去（元データは削除しない）。SMOTEENNとの違いは、ノイズ判別にLOFを使用する点と、除去対象が拡張データのみに限定される点。閾値はデータ依存であり、実運用ではLOFスコアの分布可視化が必要。

出典: Maulidevi & Surendro, "SMOTE-LOF for noise identification in imbalanced data classification", Journal of King Saud University-Computer and Information Sciences, 34(6), 2022.

## アイデア

- LOFはグローバル閾値でなく近傍との相対密度比で外れ値判定するため、疎密混在データセットでもロバストに機能する点が設計として巧み
- 生成データのみを削除対象とし元データを保護する設計は、少数クラスのサンプル数をこれ以上減らさないという制約を明示的に守る実用的配慮
- 監査データ（不正取引の検出など）はクラス不均衡が顕著なケースが多く、SMOTE-LOFのような後処理フィルタリングは誤検知削減に直接応用可能

## 前提知識

- **SMOTE** → /deep_5323 インドネシア語Spotifyレビューの感情分析：機械学習とBiLSTMの比較ベンチマーク
- **k近傍法** → /deep_4093 モデルフリーな投資家選好推定：相対エントロピーIRLアプローチ
- **LOF** (TODO: 読むべき)
- **クラス不均衡** → /deep_2112 UniPROT: 部分最適輸送と劣モジュラ保証による均一プロトタイプ選択
- **SMOTEENN** → /deep_6565 表形式データ拡張：SMOTEENN

## 関連記事

- /deep_6317 表形式データ拡張手法：Safe-Level-SMOTE
- /deep_6493 表形式データ拡張手法：K-means SMOTE
- /deep_6206 表形式データ拡張手法：Borderline-SMOTE
- /deep_8154 表形式データ拡張手法 part22：Radial-Based Oversampling（RBO）
- /deep_6761 表形式データ拡張手法 part10：ROSE（Random Over Sampling Examples）

## 原文リンク

[表形式データ拡張手法 part23：SMOTE-LOF](https://zenn.dev/haruto_big6/articles/51c82a7061240d)
