---
title: "scikit-learnパイプラインで作る、再現性のある機械学習モデル"
url: "https://zenn.dev/ds_ai_lab/articles/20260606-sklearn-pipeline"
date: 2026-06-08
tags: [scikit-learn, Pipeline, ColumnTransformer, データリーク, GridSearchCV, StandardScaler, OneHotEncoder, joblib, 機械学習, 前処理]
category: "ai-ml"
related: [396, 6568, 1577, 349, 1754]
memo: "[Zenn 機械学習] scikit-learnパイプラインで作る、再現性のある機械学習モデル"
processed_at: "2026-06-08T09:10:19.343860"
---

## 要約

scikit-learnのPipelineを使うことで、前処理からモデル訓練・推論までを一つの流れとして管理し、データリーク防止・再現性向上・コードのシンプル化を同時に達成する手法を解説した記事。

まず、Pipelineを使わない典型的な問題として、テストデータに対してStandardScalerのfit_transformを誤って呼び出すデータリークを示す。これによりテストデータの平均・分散が前処理に混入し、評価指標が過剰に良く見える問題が発生する。

Pipelineの基本構造はステップのリストで定義される。fit()呼び出し時、最後のステップ以外はfit_transform()、最後のステップのみfit()が順番に実行される。predict()/score()時は最後以外のステップでtransform()のみが呼ばれるため、テストデータへのfitが構造的に防止される。

実務で頻出する数値・カテゴリ変数の混在データには、ColumnTransformerを組み合わせる。数値列にはSimpleImputer(strategy='median') + StandardScaler、カテゴリ列にはSimpleImputer(strategy='most_frequent') + OneHotEncoder(handle_unknown='ignore')を適用し、それぞれをサブPipelineとして定義した後、ColumnTransformerで統合してからRandomForestClassifier等のモデルと接続する。

ハイパーパラメータのチューニングはGridSearchCVと「ステップ名__パラメータ名」記法（例: model__n_estimators, preprocessor__num__imputer__strategy）で実現できる。CVの各foldでも正しくtrain/testが分離される点がPipelineの大きな利点。

カスタム変換器はBaseEstimatorとTransformerMixinを継承して作成する。fit()でtrainデータの統計量（例: IQRベースの上下限）を記録し、transform()でその統計量を適用することでデータリークを防ぐ。記事ではLogTransformer（対数変換）とOutlierClipper（IQRベースのクリッピング）の実装例を示している。

学習済みPipelineはjoblib.dump/loadでシリアライズ可能で、スケーラーの平均・分散等の前処理パラメータも含めて保存されるため、本番環境でも同一の前処理を再現できる。また、set_config(display='diagram')でJupyterノートブック上でPipelineをHTML図として可視化できる。

監査エージェント開発への示唆として、監査データ（財務数値・テキスト・カテゴリ属性の混在）を扱うモデル構築においても同じパターンが適用可能。Pipelineによって前処理ロジックをモデルとセットで管理することで、監査ワークフローの再現性・説明可能性を担保しやすくなる。

## アイデア

- Pipelineのfit()/predict()の非対称な挙動（最後のステップのみfit()）が構造的にデータリークを防ぐ設計になっている点
- BaseEstimator + TransformerMixinを継承することで、カスタム変換器がGridSearchCVのパラメータ探索やPipelineのシリアライズに完全に統合される点
- ColumnTransformerとサブPipelineを組み合わせることで、異種データ型の複雑な前処理を宣言的・再利用可能な形で記述できる点

## 前提知識

- **scikit-learn** → /deep_173 「平面を作るモデル」から紐解く機械学習と行列
- **StandardScaler** (TODO: 読むべき)
- **交差検証 (Cross-Validation)** (TODO: 読むべき)
- **One-Hot Encoding** (TODO: 読むべき)
- **IQR（四分位範囲）** (TODO: 読むべき)

## 関連記事

- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け
- /deep_6568 【初心者向け】CSVを入れるだけで回帰/分類の分析レポートを自動生成するPythonツール
- /deep_1577 Skops紹介：scikit-learnモデルをHugging Face Hubで安全にホスティング・共有するライブラリ
- /deep_349 Pythonでノイズ除去あり・なしを比較する ― 音声分類の精度はどう変わるか
- /deep_1754 🤗 AIリサーチ・レジデンシープログラムの発表

## 原文リンク

[scikit-learnパイプラインで作る、再現性のある機械学習モデル](https://zenn.dev/ds_ai_lab/articles/20260606-sklearn-pipeline)
