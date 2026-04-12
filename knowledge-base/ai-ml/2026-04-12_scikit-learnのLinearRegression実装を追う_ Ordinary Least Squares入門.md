---
title: "scikit-learnのLinearRegression実装を追う: Ordinary Least Squares入門"
url: "https://zenn.dev/seiwan/articles/sklearn_learn_1_1_1"
date: 2026-04-12
tags: [scikit-learn, LinearRegression, OLS, 最小二乗法, numpy, lstsq, 回帰分析, Diabetesデータセット, R², MSE]
category: "ai-ml"
memo: "[Zenn 機械学習] scikit-learnのLinearRegressionを実装まで追う: Ordinary Least Squares入門"
related: [173, 396, 1577, 865, 340]
processed_at: "2026-04-12T09:04:21.597854"
---

## 要約

本記事は、scikit-learnのLinearRegressionクラスを「動かす」だけでなく、GitHubのソースコードレベルで内部実装を追うことを目的とした技術解説記事である。

【数学的背景】線形回帰の予測式はŷ = Xw + bで表され、学習とは残差平方和L(w,b) = Σ(yi - ŷi)²を最小化するwとbを求めることである（OLS: Ordinary Least Squares）。教科書的な解は正規方程式ŵ = (X^T X)^{-1} X^T yだが、実装では数値安定性の観点からlstsq系ルーチン（最小二乗ソルバ）を使用する。

【実装確認の流れ】まず最短例として3点の学習データ([[0,0],[1,1],[2,2]] → [0,1,2])でfitを呼ぶと、coef_=[0.5, 0.5]、intercept_≈0が得られ、ŷ = 0.5x1 + 0.5x2という直線が求まることを確認する。次にDiabetesデータセット（442サンプル、10特徴量）のBMI列のみを使い、末尾20件をテストとしてhold-out評価を行う。結果はcoef_≈938.24、intercept_≈152.92、MSE≈2548、R²≈0.47で、「BMI単一特徴量では進行度の分散の47%しか説明できない」と定量的に解釈できる。

【内部実装の詳細】ソースはsklearn/datasets/_base.pyとsklearn/linear_model/_base.pyを中心に追う。load_diabetesはgzip圧縮CSVを読み込み、scaled=True（デフォルト）のとき標準化後にdata /= n^0.5でスケーリングする。LinearRegressionのfit内部では、(1)fit_interceptがTrueならXの列方向平均を引いてセンタリング、(2)多出力かどうかでscipy.linalg.lstsqまたはnp.linalg.lstsqに分岐してソルバを呼び出し、(3)求まった係数から切片を復元する流れになっている。predictはŷ = X @ coef_ + intercept_の行列積のみで、追加計算は一切ない。

【監査エージェント開発への示唆】scikit-learnの内部実装が示す「正規方程式ではなくlstsqを使う」設計判断は、数値精度と計算安定性のトレードオフを意識したものである。監査エージェントで回帰ベースの異常検知や予測モデルを組み込む場合、ライブラリの内部ソルバ選択の意図を理解した上でfit_intercept・copy_Xなどのパラメータを適切に設定することが重要である。また、MSEとR²を組み合わせた評価フレームワークは、監査エージェントの予測精度報告テンプレートとしてそのまま応用可能である。

## アイデア

- 正規方程式(X^T X)^{-1} X^T yを直接計算せずlstsqルーチンに委ねる設計は、逆行列計算の数値不安定性（特に多重共線性が強い場合）を回避するための実践的判断であり、教科書実装との重要な乖離点
- fit_intercept=Trueのとき、切片をデザイン行列に列追加するのではなく、Xをセンタリングして係数を求めた後に切片を復元する二段階設計は、数値精度と計算効率を両立させる工夫
- R²=0.47という結果から「BMI単一特徴量では不十分」と定量的に示し、残りの9特徴量・非線形モデル・正則化という改善方向を具体的に提示している点が、実務的なモデル評価の思考フローとして参考になる

## 前提知識

- **線形代数（行列積・転置）** (TODO: 読むべき)
- **最小二乗法 (OLS)** (TODO: 読むべき)
- **numpy / scipy** (TODO: 読むべき)
- **scikit-learn API (fit/predict)** (TODO: 読むべき)
- **MSE / R²** (TODO: 読むべき)

## 関連記事

- [「平面を作るモデル」から紐解く機械学習と行列](../ai-ml/2026-04-01_「平面を作るモデル」から紐解く機械学習と行列.md)
- [機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け](../infra/2026-03-29_機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け.md)
- [Skops紹介：scikit-learnモデルをHugging Face Hubで安全にホスティング・共有するライブラリ](../infra/2026-04-11_Skops紹介：scikit-learnモデルをHugging Face Hubで安全にホスティング・共有するライブラリ.md)
- [MLで株価を予測することはできるのか？](../ai-ml/2026-04-08_MLで株価を予測することはできるのか？.md)
- [LLMパフォーマンスに対するプロンプト構成要素の影響を理解するための回帰フレームワーク](../ai-ml/2026-04-06_LLMパフォーマンスに対するプロンプト構成要素の影響を理解するための回帰フレームワーク.md)

## 原文リンク

[scikit-learnのLinearRegression実装を追う: Ordinary Least Squares入門](https://zenn.dev/seiwan/articles/sklearn_learn_1_1_1)
