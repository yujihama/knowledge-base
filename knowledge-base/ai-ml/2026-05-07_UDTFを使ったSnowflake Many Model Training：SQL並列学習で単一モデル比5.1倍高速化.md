---
title: "UDTFを使ったSnowflake Many Model Training：SQL並列学習で単一モデル比5.1倍高速化"
url: "https://zenn.dev/snowflakejp/articles/77025aadb71ce1"
date: 2026-05-07
tags: [Snowflake, UDTF, Many Model Training, scikit-learn, RandomForest, 並列学習, PARTITION BY, Snowpark]
category: "ai-ml"
related: [1149, 396, 173, 1648, 4047]
memo: "[Zenn 機械学習] UDTF を使った Snowflake  Many Model Training"
processed_at: "2026-05-07T21:19:47.404191"
---

## 要約

SnowflakeのUDTF（User-Defined Table Function）を活用し、グループ（店舗・商品カテゴリ等）ごとに個別モデルを並列訓練するMany Model Training（MMT）の実装方法を解説した記事。公式APIがContainer Runtimeを必要とするのに対し、UDTFはSQL上の`PARTITION BY`句を指定するだけでSnowflakeが各パーティションを自動並列処理する点が最大の特徴。

実装の核心はPythonハンドラークラスの2メソッド構成にある。`process()`はパーティション内の各行データを受け取りリストに蓄積し、`end_partition()`はパーティション（＝1グループ）のデータが揃った時点で呼び出され、scikit-learnのRandomForestRegressorによるモデル訓練とMAE・RMSEの計算を実行してメトリクスをyieldする。SQLクエリ側では`TABLE(train_model_udtf(...) OVER (PARTITION BY sd.STORE_ID))`と記述するだけで50店舗の並列学習が実現する。

検証データは50店舗×365行＝18,250行の売上シミュレーションデータ（気温・祝日・プロモーション・曜日・月を特徴量）。学習時間の比較では、全データを1モデルで学習するSnowflake ML APIのRandomForestRegressorが30.3秒かかったのに対し、UDTF MMTは5.9秒で完了し、5.1倍の速度差を記録した。ただし環境・データ依存の結果であることも明記されている。

UDTFのパッケージ指定（`PACKAGES = ('scikit-learn', 'numpy', 'pandas')`）により、Snowflakeのウェアハウスリソース上でscikit-learnが直接動作する。モデルの再訓練はSnowflake Tasksで定期スケジュール実行が可能。ユースケースはリテール（店舗別売上予測）・製造（工場別品質予測）・エネルギー（地域別需要予測）など。監査エージェント開発への示唆として、拠点・部門・リスクカテゴリごとに個別の異常検知モデルを並列訓練する構成への応用が考えられ、Snowflakeデータウェアハウス上でSQLのみでMLパイプラインを完結させる設計パターンとして参考になる。

## アイデア

- UDTF の`end_partition()`フックがバッチ学習の境界を自然に表現しており、SQLの`PARTITION BY`とMLの「グループ別モデル」の概念を一対一対応させた設計が巧み
- Container Runtimeが不要なUDTFアプローチにより、データをSQLウェアハウスから移動させずにin-database MLが完結し、データ転送コストとレイテンシを排除できる
- 50モデル並列で5.1倍高速化という結果は、グループ数が増えるほどスケールアウト効果が大きくなることを示唆しており、数百・数千グループのMMTでの優位性がさらに拡大する可能性がある

## 前提知識

- **UDTF** (TODO: 読むべき)
- **Snowpark** (TODO: 読むべき)
- **RandomForestRegressor** (TODO: 読むべき)
- **PARTITION BY** (TODO: 読むべき)
- **Many Model Training** (TODO: 読むべき)

## 関連記事

- /deep_1149 製造業エンジニアがベアリング異常検知をゼロから実装した話
- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け
- /deep_173 「平面を作るモデル」から紐解く機械学習と行列
- /deep_1648 scikit-learnのLinearRegression実装を追う: Ordinary Least Squares入門
- /deep_4047 Snowflake Online Feature Serving で作るリアルタイムレコメンデーション - Two-Tower ネットワーク

## 原文リンク

[UDTFを使ったSnowflake Many Model Training：SQL並列学習で単一モデル比5.1倍高速化](https://zenn.dev/snowflakejp/articles/77025aadb71ce1)
