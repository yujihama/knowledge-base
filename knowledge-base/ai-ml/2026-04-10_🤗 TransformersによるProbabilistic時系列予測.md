---
title: "🤗 TransformersによるProbabilistic時系列予測"
url: "https://huggingface.co/blog/time-series-transformers"
date: 2026-04-10
tags: [Transformer, 時系列予測, 確率的予測, GluonTS, HuggingFace, Ancestral Sampling, MASE]
category: "ai-ml"
memo: "[HF Blog] Probabilistic Time Series Forecasting with 🤗 Transformers"
processed_at: "2026-04-10T21:13:14.377704"
---

## 要約

本記事は、HuggingFace Transformersライブラリに実装されたTime Series Transformerを用いた確率的時系列予測の手法を解説する。従来のARIMAなどのクラシカル手法が各時系列に個別フィットする「ローカル」モデルであるのに対し、ディープラーニングを用いた「グローバル」モデルは複数の時系列から潜在表現を学習できる点が本質的な違いである。さらに点予測ではなく確率分布（ガウス分布、Student-T分布など）を出力する「確率的予測」を行うことで、予測の不確実性を定量化できる。

アーキテクチャにはVaswani et al. (2017)のバニラTransformerをベースとしたEncoder-Decoderモデルを採用。エンコーダにコンテキストウィンドウを、デコーダに予測ウィンドウをそれぞれ入力し、デコーダはcausal maskにより過去ステップのみ参照する（teacher forcingと同等）。推論時はAncestral Samplingにより分布からサンプリングしながら自己回帰的に予測を生成する。欠損値はattention maskで対応でき、インピュテーション不要。

実装面では、GluonTSライブラリを用いて時間関連特徴量（月・週・日など）の生成、ラグ特徴量（月次データなら[1,2,3,4,5,6,7,11,12,13]ステップのラグ）、スケーリング（平均スケーラー）を実施。データセットにはMonash Time Series Forecasting RepositoryのAustraliaツーリズム月次データ（366地域）を使用。

モデル設定はencoder/decoder層数各2、attention heads 2、FFN次元数32と比較的小規模。学習はAdamWオプティマイザ（lr=1e-4、weight decay=1e-8）でAccelerateを用いて実施。評価指標はMASE（Mean Absolute Scaled Error）とsMAPEを使用し、GluonTSの`make_evaluation_predictions`で24ステップ先の予測サンプルを100個生成して算出。Transformerの二次計算量の制約やオーバーフィットのリスクも課題として明示されている。

## アイデア

- 点予測ではなく確率分布を出力することで予測の信頼区間を定量化でき、意思決定支援システムへの組み込みに適している
- GluonTSのラグ特徴量・時間特徴量生成パイプラインは、監査データの時系列分析にそのまま転用可能な汎用前処理フレームワークとして機能する
- Ancestral Samplingによる自己回帰生成は、LLMのトークン生成と構造的に同一であり、言語モデルの知見（KVキャッシュ、バッチ推論最適化等）が時系列予測にも適用できる可能性がある

## Yujiの取り組みへの示唆

監査エージェント開発において、財務指標や取引量などの時系列異常検知に確率的予測モデルを組み込むことで、単純な閾値ベース検知より高精度なアノマリースコアを算出できる。GluonTSのデータパイプライン（ラグ特徴量・スケーリング）はPydanticによるデータバリデーションと組み合わせやすく、LangGraphのワークフロー内にTime Series Transformerノードとして統合する際の参照実装として活用できる。

## 原文リンク

[🤗 TransformersによるProbabilistic時系列予測](https://huggingface.co/blog/time-series-transformers)
