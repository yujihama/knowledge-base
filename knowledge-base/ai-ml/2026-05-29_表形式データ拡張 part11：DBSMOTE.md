---
title: "表形式データ拡張 part11：DBSMOTE"
url: "https://zenn.dev/haruto_big6/articles/bb14f396ad363e"
date: 2026-05-29
tags: [DBSMOTE, SMOTE, DBSCAN, クラス不均衡, オーバーサンプリング, 表形式データ, smote-variants, KMeans-SMOTE, データ拡張]
category: "ai-ml"
related: [6317, 6761, 6493, 6206, 6565]
memo: "[Zenn 機械学習] 表形式データ拡張 part11：DBSMOTE"
processed_at: "2026-05-29T09:08:36.487648"
---

## 要約

本記事はクラス不均衡問題に対処するオーバーサンプリング手法「DBSMOTE（Density-Based SMOTE）」を解説する。従来のSMOTEは多数クラスの分布を無視して合成データを生成するため、少数クラスと多数クラスの決定境界が侵食される問題がある。DBSMOTEはDBSCAN（Density-Based Spatial Clustering of Applications with Noise）を用いて少数クラスをクラスタリングし、ノイズと判定されたデータを除外した上でクラスター内のみに合成データを生成することでこの問題を回避する。

アルゴリズムの流れは4段階。①少数クラスデータをDBSCANでクラスタリング（パラメータ：到達可能距離εとコア点閾値minPts）。②各クラスター内でdirectly density-reachable graph（DDRG）を構築。DDRGはコア点とそのε圏内の点をエッジで結んだグラフ。③クラスター重心に最も近い点を擬似中心点とし、ダイクストラ法で各データ点から擬似中心点への最短経路を探索。④各データ点に対して最短経路上のランダムなエッジを選択し、その2点間で合成データを生成。生成データはコア点周辺に集中するため、決定境界から離れた安全な領域にのみデータが追加される。

Pythonによる実験では、クラスター重心が[0,0]、[3,3]、[-3,3]の3クラスタ合計3000サンプル（多数クラス2970、少数クラス計30）のデータに対して決定木分類器でF1スコアを比較。結果はOriginal: 0.5455、SMOTE: 0.3200、KMeans-SMOTE: 0.6667、DBSMOTE: 0.6667となり、クラスターベース手法が通常SMOTEを上回った。実装はsmote-variantsライブラリを使用。

DBSMOTEの利点はノイズ除外とコア点周辺への集中生成による境界侵食の抑制。欠点はεとminPtsへの感度が高くチューニングが難しい点、および生成データの多様性が低い点。KMeans-SMOTEとの比較では、DBSMOTEの方が生成範囲が狭い（DBSCANがノイズ判定したデータを除外するため）。監査AIのユースケースとして、不正取引検知など正常/異常の極端なクラス不均衡が生じる表形式データに対してDBSMOTEを適用することで、偽陽性・偽陰性のトレードオフを考慮した安全な学習データ拡張が可能になる。

## アイデア

- DBSCANのノイズ除外機能をデータ拡張に活用することで、外れ値由来の不安定な合成データを自動排除できる点が巧妙
- ダイクストラ法による最短経路探索を生成点選択に使うことで、クラスター中心付近（=コア点密集域）にデータを誘導する設計思想が興味深い
- εとminPtsのハイパーパラメータ感度の高さは実運用上の課題であり、自動チューニング（Bayesian Optimization等）との組み合わせが実用化のカギになりうる

## 前提知識

- **SMOTE** → /deep_5323 インドネシア語Spotifyレビューの感情分析：機械学習とBiLSTMの比較ベンチマーク
- **DBSCAN** (TODO: 読むべき)
- **クラス不均衡** → /deep_2112 UniPROT: 部分最適輸送と劣モジュラ保証による均一プロトタイプ選択
- **ダイクストラ法** → /deep_136 AIに地図を読ませる：MapTraceによるルートトレース学習
- **KMeans-SMOTE** (TODO: 読むべき)

## 関連記事

- /deep_6317 表形式データ拡張手法：Safe-Level-SMOTE
- /deep_6761 表形式データ拡張手法 part10：ROSE（Random Over Sampling Examples）
- /deep_6493 表形式データ拡張手法：K-means SMOTE
- /deep_6206 表形式データ拡張手法：Borderline-SMOTE
- /deep_6565 表形式データ拡張：SMOTEENN

## 原文リンク

[表形式データ拡張 part11：DBSMOTE](https://zenn.dev/haruto_big6/articles/bb14f396ad363e)
