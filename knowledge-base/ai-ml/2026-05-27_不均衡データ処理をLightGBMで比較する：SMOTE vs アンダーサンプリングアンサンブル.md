---
title: "不均衡データ処理をLightGBMで比較する：SMOTE vs アンダーサンプリングアンサンブル"
url: "https://zenn.dev/kyoju_teach/articles/d941b78007bb9b"
date: 2026-05-27
tags: [LightGBM, 不均衡データ, SMOTE, アンダーサンプリング, Precision-Recall, クレジットカード不正検知, imbalanced-learn, EasyEnsemble, PR-AUC, scale_pos_weight]
category: "ai-ml"
related: [6565, 6418, 6317, 6493, 6206]
memo: "[Zenn 機械学習] 不均衡データ処理をLightGBMで比較する SMOTE vs アンダーサンプリングアンサンブル"
processed_at: "2026-05-27T21:01:34.907638"
---

## 要約

クレジットカード不正検知など実務で頻出する不均衡データ（Imbalanced Data）に対して、LightGBMを用いた4手法を比較した実験記事。使用データはKaggleのCredit Card Fraud Detectionデータセット（約28万件、不正492件、不正率0.172%）。

比較した手法は以下の4つ：(1) Baseline（何も処理しない素のLightGBM）、(2) scale_pos_weight（クラス重み調整：負例数÷正例数を設定）、(3) SMOTE（imbalanced-learnのPipelineでtrainデータのみに適用しリーク防止）、(4) アンダーサンプリングアンサンブル（多数クラスを少数クラス数まで削減してseedを変えながら10モデル学習し確率を平均）。

threshold=0.5固定での結果：Baseline（Precision 0.77、Recall 0.75、F1 0.76、PR-AUC 0.73）、scale_pos_weight（Precision 0.06、Recall 0.85、F1 0.12）、SMOTE（Precision 0.73、Recall 0.87、F1 0.79、PR-AUC 0.82）、アンダーサンプリングアンサンブル（Precision 0.05、Recall 0.93、PR-AUC 0.83）。

主な知見は3点。第1に、最近のGBDT系モデル（LightGBM）は素の状態でも不均衡データにかなり強く、Baselineでも実用的な性能を示した。第2に、Recall重視の手法（scale_pos_weight・アンダーサンプリングアンサンブル）はPrecisionが大幅に崩壊するトレードオフが顕著に出た。第3に、SMOTEはPrecision・Recallのバランスが最も良好だったが、データ構造やthreshold設定によって結果が変わるため「SMOTEが常に最強」ではない。

実務的な示唆として、何を最適化すべきかを最初に定義することが重要と強調。不正検知であれば見逃し（FN）を減らすためRecall重視、自動BANであれば誤検知（FP）を減らすためPrecision重視など、ユースケースによって最適手法が異なる。またモデル変更よりthresholdチューニング（例：0.5→0.3に下げてRecall向上）の方が効果的なケースも多い。監査AIへの応用として、異常取引検知や監査対象のスクリーニングにおけるPrecision-Recallトレードオフの設計判断に直接参考になる内容。

## アイデア

- アンダーサンプリングアンサンブルがPR-AUC（0.827）でSMOTE（0.820）とほぼ同等なのに、threshold=0.5固定ではPrecisionが0.05と崩壊する——PR-AUCはthreshold非依存の指標なため、threshold調整次第では同等以上の実用性を持つ可能性がある
- SMOTEのCVリーク問題：train/test split前にfit_resampleを適用すると合成サンプルがtestに情報を漏らすため、imbalanced-learnのPipelineで必ずtrain内のみに閉じる設計が必須という実装上の落とし穴
- 監査スクリーニングへの応用として、第1段階でRecall重視（見逃しゼロ優先）のアンダーサンプリングアンサンブルで候補を広く拾い、第2段階でPrecision重視のモデルで絞り込む2段階パイプライン設計が考えられる

## 前提知識

- **LightGBM** → /deep_866 AIに180回の株価予測実験を丸投げしてわかったこと——「AIだけでは正しく評価できない」という話
- **SMOTE** → /deep_5323 インドネシア語Spotifyレビューの感情分析：機械学習とBiLSTMの比較ベンチマーク
- **Precision/Recall/F1** (TODO: 読むべき)
- **PR-AUC** (TODO: 読むべき)
- **クラス不均衡問題** (TODO: 読むべき)

## 関連記事

- /deep_6565 表形式データ拡張：SMOTEENN
- /deep_6418 表形式データ拡張：SMOTE-N（カテゴリ特徴量のみのデータセット向けオーバーサンプリング手法）
- /deep_6317 表形式データ拡張手法：Safe-Level-SMOTE
- /deep_6493 表形式データ拡張手法：K-means SMOTE
- /deep_6206 表形式データ拡張手法：Borderline-SMOTE

## 原文リンク

[不均衡データ処理をLightGBMで比較する：SMOTE vs アンダーサンプリングアンサンブル](https://zenn.dev/kyoju_teach/articles/d941b78007bb9b)
