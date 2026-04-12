---
title: "Hugging Face TransformersとHabana GaudiでBERTをスクラッチから事前学習する"
url: "https://huggingface.co/blog/pretraining-bert"
date: 2026-04-11
tags: [BERT, MLM, Habana Gaudi, Optimum Habana, 事前学習, BertTokenizerFast, HuggingFace, AWS DL1]
category: "ai-ml"
memo: "[HF Blog] Pre-Train BERT with Hugging Face Transformers and Habana Gaudi"
related: [1492, 1016, 1572, 1529, 1494]
processed_at: "2026-04-11T21:06:03.818630"
---

## 要約

本チュートリアルは、AWS上のHabana Gaudi搭載DL1インスタンスを使い、BERT-baseモデルをスクラッチから事前学習する手順を解説したものである。使用ライブラリはHugging Face Transformers、Optimum Habana、Datasetsの3つ。学習タスクはBERT本来の事前学習手法の一つであるMasked Language Modeling（MLM）で、入力テキストの一部をマスクしてモデルに予測させることで双方向の文脈理解を獲得させる。

事前学習のパイプラインは大きく4ステップに分かれる。①データセット準備：Wikipedia（20220301.en）とBookCorpusをHugging Face Hubからロードし、concatenate_datasetsで結合して大規模コーパスを構築する。②トークナイザー訓練：既存のbert-base-uncasedをベースにBertTokenizerFastを使い、語彙サイズ32,000でカスタムトークナイザーをtrain_new_from_iterator()で訓練しHubに公開する。③データ前処理：訓練済みトークナイザーで全テキストをトークン化し、512トークン単位のチャンクに分割・結合してマルチプロセス（num_proc=CPU数）で並列処理、DataCollatorForLanguageModelingでMLM用マスク処理（mask確率15%）を動的に適用する。④事前学習：BertConfigで隠れ層768次元・12ヘッド・12レイヤーの標準BERT-baseアーキテクチャを定義し、BertForMaskedLMをスクラッチで初期化。GaudiTrainingArguments＋GaudiTrainerをOptimum Habanaから利用することでHabana Gaudi HPU向けに最適化されたトレーニングループを実行する。バッチサイズ、学習率スケジューラ、warmup等はTrainingArgumentsで制御する。

Habana Gaudiを採用する理由はコストパフォーマンスにある。NVIDIAのGPUと比較してHabana GaudiはAWS DL1インスタンス上でMLワークロードに対し高いスループット対コスト比を提供するとされており、大規模事前学習コストの削減を狙える。ステップ1〜3はCPU集約的なためc6i.12xlargeのような汎用インスタンスで実施し、ステップ4のGPU/HPU集約的な学習フェーズのみDL1インスタンスに切り替える設計が推奨されている。

## アイデア

- トークナイザーをドメイン固有コーパスでゼロから訓練することで、監査・法令テキスト特有の語彙（内部統制、重要性、リスク評価等）をボキャブラリに取り込んだ専門特化BERTを構築できる
- MLMによる双方向事前学習はラベルなしテキストから文脈表現を獲得するため、大量の監査報告書・内部統制文書を用いたドメイン適応事前学習（Domain-Adaptive Pretraining）に直接応用可能
- HuggingFace HubへのArtifact（トークナイザー・データセット・モデル）の段階的プッシュにより、チーム内での再現性確保と実験管理が容易になるパターンはMLOpsパイプライン設計の参考になる
## 関連記事

- /deep_1492 タンパク質への深層学習：プロテイン言語モデルの仕組みと応用
- /deep_1016 Amazon SageMaker向けHugging Face埋め込みコンテナの正式リリース
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Hugging Face TransformersとHabana GaudiでBERTをスクラッチから事前学習する](https://huggingface.co/blog/pretraining-bert)
