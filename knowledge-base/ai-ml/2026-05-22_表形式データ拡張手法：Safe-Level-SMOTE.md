---
title: "表形式データ拡張手法：Safe-Level-SMOTE"
url: "https://zenn.dev/haruto_big6/articles/1408870c3ea882"
date: 2026-05-22
tags: [Safe-Level-SMOTE, SMOTE, オーバーサンプリング, クラス不均衡, 表形式データ, データ拡張, smote-variants, imbalanced-learn]
category: "ai-ml"
related: [6206, 6084, 5323, 1526, 5404]
memo: "[Zenn 機械学習] 表形式データ拡張手法：Safe-Level-SMOTE"
processed_at: "2026-05-22T12:01:38.941075"
---

## 要約

Safe-Level-SMOTEは、クラス不均衡問題に対処するオーバーサンプリング手法であり、SMOTEの改良版の一つ。SMOTEが多数クラスの分布を無視して少数クラスサンプル間にランダムにデータを生成するため、多数クラス領域に侵入するデータを生成してしまうという欠点を解消するために提案された（Bunkhumpornpat et al., PAKDD 2009）。

アルゴリズムの核心は「安全度（safe level）」の概念。少数クラスサンプルpのk近傍を探索し、そのうち少数クラスに属するサンプル数をsl_pと定義する。次に、pの少数クラス近傍点nに対しても同様にsl_nを計算し、安全度比率sl_ratio = sl_p / sl_nを算出する。この比率に基づき、新規サンプル生成式 s = p + (n - p) * rand における乱数randの範囲を5パターンで調整する：(i) sl_p = sl_n = 0ならサンプル生成しない、(ii) sl_n = 0かつsl_p ≠ 0ならrand = 0（pを複製）、(iii) sl_ratio = 1ならrand ∈ [0, 1]（SMOTE同様）、(iv) sl_ratio > 1ならrand ∈ [0, 1/sl_ratio]（pに近い側）、(v) sl_ratio < 1ならrand ∈ [1 - sl_ratio, 1]（nに近い側）。これにより、少数クラスが密集している「安全な場所」を優先的にデータ生成先として選ぶ「守り」の拡張戦略を実現する。

ADASYNやBorderline-SMOTEが多数・少数クラスの決定境界付近に積極的にデータを生成する「攻め」の手法であるのに対し、Safe-Level-SMOTEはその逆の思想を持つ。この保守的な設計により多数クラスへの悪影響を抑えられるが、少数クラスの決定境界を拡張する効果は劣る。また、全サンプルがノイズ状態（sl_p = sl_n = 0）の場合はデータ生成が一切行われないため、フォールバック戦略が必要となる欠点もある。

Python実装ではimbalanced-learnにSafe-Level-SMOTEが含まれないため、smote-variantsライブラリを使用する（pip install smote-variants）。実験結果として、SMOTEが少数クラス全域に均等にデータを生成するのに対し、Safe-Level-SMOTEは多数クラスから若干距離のある安全領域に集中してデータを生成することが散布図で確認できる。なお、smote-variantsの実装では各特徴量ごとに個別の乱数を使用するため、厳密な2点間の内分点ではなく長方形領域内にサンプルが生成される点が原論文の記述と若干異なる。どの拡張手法が最適かはデータ特性や誤陽性コストなど実運用上の条件に依存するため、実データによる検証が不可欠。

## アイデア

- 安全度比率（sl_ratio）によって乱数の生成範囲を5パターンに動的調整するアイデアは、「どちらの点に近い合成サンプルを作るか」を安全性指標で制御する精緻な設計であり、単純な内分点生成を超えた確率的バイアス制御の好例
- 全サンプルがノイズ状態の場合にデータ生成がゼロになるという「生成拒否」設計は、品質保証を優先するフォールバック設計の問題として監査AIの異常検知モデル学習にも応用できる観点（低品質データからの学習をどう防ぐか）
- 特徴量ごとに個別の乱数を使うsmote-variantsの実装が、意図せず「2点を対角とする長方形内にサンプルを生成する」という効果をもたらしデータ多様性を増す点は、論文実装の曖昧さがむしろポジティブな影響をもたらした事例として興味深い

## 前提知識

- **SMOTE** → /deep_5323 インドネシア語Spotifyレビューの感情分析：機械学習とBiLSTMの比較ベンチマーク
- **k近傍法（kNN）** (TODO: 読むべき)
- **クラス不均衡問題** (TODO: 読むべき)
- **Borderline-SMOTE** → /deep_6206 表形式データ拡張手法：Borderline-SMOTE
- **ADASYN** → /deep_6084 表形式データ拡張手法：ADASYN（Adaptive Synthetic Sampling）

## 関連記事

- /deep_6206 表形式データ拡張手法：Borderline-SMOTE
- /deep_6084 表形式データ拡張手法：ADASYN（Adaptive Synthetic Sampling）
- /deep_5323 インドネシア語Spotifyレビューの感情分析：機械学習とBiLSTMの比較ベンチマーク
- /deep_1526 銀行取引における不正検知システム
- /deep_5404 量子純粋状態アンサンブル生成のための確率的シュレーディンガー拡散モデル

## 原文リンク

[表形式データ拡張手法：Safe-Level-SMOTE](https://zenn.dev/haruto_big6/articles/1408870c3ea882)
