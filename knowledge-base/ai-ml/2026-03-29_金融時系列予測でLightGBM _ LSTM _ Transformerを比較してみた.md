---
title: "金融時系列予測でLightGBM / LSTM / Transformerを比較してみた"
url: "https://zenn.dev/sigma_lab/articles/aitrader-series-model-comp-1-20260304"
date: 2026-03-29
tags: [LightGBM, LSTM, Transformer, アンサンブル学習, 時系列予測, PyTorch, 金融ML, 特徴量エンジニアリング]
category: "ai-ml"
memo: "[Zenn 機械学習] 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた"
processed_at: "2026-03-29T22:22:18.468888"
---

## 要約

金融時系列データの非定常性・低SNR・過学習リスクに対処するため、LightGBM・LSTM・Transformerの3モデルを比較し、アンサンブル学習の有効性を検証。LightGBMはテーブル形式特徴量（RSI、SMAなどテクニカル指標）を扱う決定木ベースモデル、LSTMはゲート機構による長期依存性学習、TransformerはAttentionによるグローバルな関係捉捉に各々強みを持つ。実装はPyTorch（LSTMModel）とLightGBMを組み合わせ、MLPredictorクラスで重み付きアンサンブル（デフォルトLSTM比率0.3）を実現。特徴量エンジニアリングにはRSI_14やSMA_5などのテクニカル指標を使用し、二値分類（翌N日後の上昇/下落）タスクとして定式化している。単一モデルの限界を補完するアンサンブル設計が本稿の主旨。

## 要点

- LightGBM・LSTM・Transformerはそれぞれ局所特徴量・逐次文脈・グローバル依存性を補完的に学習するため、重み付きアンサンブルで予測精度と頑健性を向上できる
- MLPredictorクラスでlstm_weight=0.3の加重平均アンサンブルを実装し、LSTMが利用不可の場合はLightGBMのみにフォールバックする設計で可用性を確保している
- 金融時系列の二値分類タスクでは、RSI・SMA等のテクニカル指標を特徴量エンジニアリングで生成し、StandardScalerで正規化してから各モデルに入力する前処理パイプラインが重要
## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_122 ML学習記録 #1 — 初めてのKaggleコンペ（Store Sales時系列予測）でやったこと
- /deep_488 Claude Code × Google Colab 第3弾：PyTorch LSTMで東京の気温7日間予測（GPU使用）
- /deep_97 AIトレーダー開発ログ #2: Paper Tradingで検証したQuant型アーキテクチャの有効性
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[金融時系列予測でLightGBM / LSTM / Transformerを比較してみた](https://zenn.dev/sigma_lab/articles/aitrader-series-model-comp-1-20260304)
