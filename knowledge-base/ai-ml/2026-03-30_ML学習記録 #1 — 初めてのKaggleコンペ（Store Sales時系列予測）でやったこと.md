---
title: "ML学習記録 #1 — 初めてのKaggleコンペ（Store Sales時系列予測）でやったこと"
url: "https://zenn.dev/knd73/articles/c44efebfbeda03"
date: 2026-03-30
tags: [LightGBM, Polars, Pydantic, 時系列予測, Kaggle, ウォークフォワードCV, 逐次予測, Optuna, MLflow, 特徴量エンジニアリング]
category: "ai-ml"
memo: "[Zenn 機械学習] ML学習記録 #1 — 初めてのKaggleコンペでやったこと"
processed_at: "2026-03-30T12:12:06.460597"
---

## 要約

大学2年生がClaudeをメンターとして活用しながら、Kaggleの時系列予測コンペ「Store Sales - Time Series Forecasting」に初挑戦した記録。最終LBスコアは0.42547（目標0.45以下を達成）。

技術スタックはLightGBM + Polars + Pydantic + MLflow + Optuna。パイプラインはPreprocessor → FeatureBuilder → Pipelineの3層構造で責務を分離し、設定値はすべてPydanticスキーマでJSONから読み込む。CVはウォークフォワード方式を手動実装し、lag最大値（28日）に合わせてgap_days=28を設定。Pydanticのge=28バリデーションでリークを構造的に防止している。

踏んだバグは3つ。①LightGBMのカテゴリカル変数を手動ラベルエンコーディングした結果、train/testで列がずれてスコアが異常に良く見えた（LightGBMネイティブのcategorical_feature指定で解決）。②FeatureBuilder内部でstore_nbr×family×dateソートした結果、submission.csvのid順と予測値の対応がずれた（idカラムでleft joinして解決）。③test期間のlag特徴量がNullになる問題——testにはsalesが存在しないため、15日間のうち後半8日分（8日×1782組合せ=14256行）のlag特徴量がNullになる。1日ずつ予測してsalesに書き戻す「逐次予測」で対応した。

スコア推移はv1のLB=3.271からバグ修正のv3でLB=0.449へ急改善。特徴量追加・Optunaチューニングによる改善（約0.02）より、バグ修正による改善（約2.8）の方が圧倒的に大きかった。最終特徴量はlag/rolling（7/14/28日）、石油価格lag、店舗別取引数lag、祝日フラグ（National/Regional/Local）、カレンダー特徴量、store×family累積統計、2016年エクアドル大地震期間（4/16〜4/30）の除外を含む。

教訓として、①CVスコアが良すぎる場合はリークかバグの疑い、②pytestでlag先頭N行がNullであることを検証するリーク検知パターン、③パイプライン正常化を特徴量エンジニアリングより先に行う方針、が挙げられている。

## アイデア

- Pydanticのge=バリデーションをgap_daysに設定することで、lag特徴量リークを設計レベルで防止する手法——パラメータ制約をコードに埋め込むことでヒューマンエラーを排除できる
- test期間の逐次予測（1日ずつ予測→salesに書き戻し→翌日のlag計算に利用）は誤差伝播の欠点を持つが、Nullよりも現実的な選択であるというトレードオフの整理が明確
- pytestでlag先頭N行がNullであることを毎特徴量で検証するパターン——新規特徴量追加時のリーク検知を自動化する軽量な品質保証手法

## Yujiの取り組みへの示唆

監査エージェント開発におけるPydanticによるconfig管理パターンが直接参考になる。特にge=バリデーションでビジネスルール（gap_days≥max_lag）をスキーマに埋め込む手法は、監査ルールの制約をエージェントのパラメータに組み込む際に応用できる。また、CV設計とpytestによるリーク検証の組み合わせは、LangGraphエージェントのパイプラインテスト設計（各ノードの副作用・データ境界の自動検証）に転用できる考え方である。

## 原文リンク

[ML学習記録 #1 — 初めてのKaggleコンペ（Store Sales時系列予測）でやったこと](https://zenn.dev/knd73/articles/c44efebfbeda03)
