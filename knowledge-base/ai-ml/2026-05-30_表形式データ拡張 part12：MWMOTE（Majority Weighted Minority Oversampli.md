---
title: "表形式データ拡張 part12：MWMOTE（Majority Weighted Minority Oversampling TEchnique）"
url: "https://zenn.dev/haruto_big6/articles/e93d37c8406882"
date: 2026-05-30
tags: [MWMOTE, SMOTE, オーバーサンプリング, クラス不均衡, k-NN, 表形式データ, imbalanced-learn, agglomerative clustering]
category: "ai-ml"
related: [6565, 6317, 6493, 6206, 6084]
memo: "[Zenn 機械学習] 表形式データ拡張 part12：MWMOTE"
processed_at: "2026-05-30T09:09:41.458506"
---

## 要約

MWMOTEは、クラス不均衡な表形式データに対するオーバーサンプリング手法で、SMOTEの「多数クラス領域への侵害」問題を解決するために設計されている。Borderline-SMOTEやSafe-Level-SMOTEが単純なk-nnで決定境界を推定するのに対し、MWMOTEはk-nnを3回（k1, k2, k3の3パラメータ）組み合わせて境界近傍の少数クラスサンプルを精密に特定する。

アルゴリズムは大きく3段階に分かれる。第1段階（ステップ1〜6）では、まず少数クラスデータ全体のk1-nnを探索しノイズデータを除去してS_minfを構築。次にS_minf内の各サンプルに対しk2個の多数クラス近傍点N_maj(xi)を取得しボーダーライン多数クラス集合S_bmajを構築。さらにS_bmaj内の各多数クラスサンプルに対してk3個の少数クラス近傍点N_min(yi)を取得し、ボーダーライン少数クラス集合S_iminを構築する。この3段階のk-nnにより「決定境界に近い多数クラスデータから見た少数クラス近傍点」を同定する。

第2段階（ステップ7〜9）では各少数クラスサンプルに選択確率S_p(xi)を付与する。重みは近接係数C_f（y_iとx_iの距離に基づく、値域[0, CMAX]）と密度係数D_f（クラスター密度を反映、疎なクラスターほど大きい）の積から情報重みI_wを計算し、それをS_bmaj全体で集計してS_w(xi)、正規化してS_p(xi)とする。決定境界への近さ・少数クラスクラスターの疎密・近傍多数クラスの密度の3要素が重みに反映される。

第3段階（ステップ10〜11）では、少数クラス全体をaverage-linkage agglomerative clusteringでクラスタリングし、S_p(xi)に従いS_iminからサンプルxを選択。同一クラスター内の別サンプルとの内分点を合成データとして生成する（クラスターが単一サンプルの場合は複製）。クラスター内で補間するためSMOTEより多数クラス領域への侵害が抑制される。Pythonではimbalanced-learnのMWMOTE実装が利用可能で、K-means SMOTEと同程度の精度改善が実験で示されている。監査AIへの応用としては、不正取引検知や異常仕訳検出など極度に不均衡なラベルデータに対する前処理手法として有効。

## アイデア

- k-nnを3回段階的に適用して「決定境界に近い多数クラスデータの近傍にある少数クラスデータ」という間接的な定義で境界サンプルを精密に特定するアプローチは、直接的なk-nnより境界推定の精度が高い
- 選択確率の重み付けに近接係数・密度係数・多数クラス密度の3要素を組み込み、単純なオーバーサンプリングではなく「どこにサンプルを増やすべきか」を定量化している設計思想が独自
- クラスター内補間によりSMOTEの多数クラス領域侵害を構造的に防ぐ仕組みは、不正検知など高コスト誤検知が許容されないユースケースで特に有効

## 前提知識

- **SMOTE** → /deep_5323 インドネシア語Spotifyレビューの感情分析：機械学習とBiLSTMの比較ベンチマーク
- **Borderline-SMOTE** → /deep_6206 表形式データ拡張手法：Borderline-SMOTE
- **k-NN** (TODO: 読むべき)
- **agglomerative clustering** (TODO: 読むべき)
- **クラス不均衡** → /deep_2112 UniPROT: 部分最適輸送と劣モジュラ保証による均一プロトタイプ選択

## 関連記事

- /deep_6565 表形式データ拡張：SMOTEENN
- /deep_6317 表形式データ拡張手法：Safe-Level-SMOTE
- /deep_6493 表形式データ拡張手法：K-means SMOTE
- /deep_6206 表形式データ拡張手法：Borderline-SMOTE
- /deep_6084 表形式データ拡張手法：ADASYN（Adaptive Synthetic Sampling）

## 原文リンク

[表形式データ拡張 part12：MWMOTE（Majority Weighted Minority Oversampling TEchnique）](https://zenn.dev/haruto_big6/articles/e93d37c8406882)
