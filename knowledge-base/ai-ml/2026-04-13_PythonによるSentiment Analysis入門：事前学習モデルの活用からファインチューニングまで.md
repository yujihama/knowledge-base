---
title: "PythonによるSentiment Analysis入門：事前学習モデルの活用からファインチューニングまで"
url: "https://huggingface.co/blog/sentiment-analysis-python"
date: 2026-04-13
tags: [sentiment-analysis, transformers, DistilBERT, RoBERTa, fine-tuning, Hugging Face Hub, pipeline, NLP, AutoNLP, Tweepy]
category: "ai-ml"
related: [1214, 1448, 1529, 1266, 1449]
memo: "[HF Blog] Getting Started with Sentiment Analysis using Python"
processed_at: "2026-04-13T12:37:06.267425"
---

## 要約

本記事はHugging FaceのBlogで2022年2月に公開されたSentiment Analysis（感情分析）の入門ガイドである。感情分析とは、テキストデータを「ポジティブ」「ネガティブ」「ニュートラル」などの感情ラベルに自動分類するNLP技術であり、SNS分析・製品レビュー解析・サポートチケットのリアルタイム分類など多様な用途で活用される。

技術的な内容として主に3点が解説されている。第1に、Hugging Face Hubで公開されている215以上の事前学習済み感情分析モデルをtransformersライブラリのpipelineクラスから5行のコードで利用する方法。`pipeline("sentiment-analysis")`でデフォルトモデルを呼び出し、テキストリストを渡すだけで各文のラベルとスコア（例: POSITIVE / 0.9998）が返される。特定ユースケース向けには`finiteautomata/bertweet-base-sentiment-analysis`（ツイート向けBERTweet）、`twitter-roberta-base-sentiment`（約5800万ツイートで訓練したRoBERTa）、`bert-base-multilingual-uncased-sentiment`（英・蘭・独・仏・西・伊の6言語対応）、`distilbert-base-uncased-emotion`（喜び・怒り・恐怖など6感情分類）等のモデルIDを指定することで差し替え可能。

第2に、独自データでのファインチューニング方法を2アプローチで説明している。コードベースのアプローチでは、IMDB映画レビューデータセット（訓練25,000件・テスト25,000件）を用いてDistilBERT（BERTより40%小型・60%高速・性能95%維持）をfine-tuneする手順を解説。具体的にはGPU環境の準備、datasets/transformers/huggingface_hubのインストール、AutoTokenizerによるトークナイズ、DataCollatorWithPaddingによる動的パディング、TrainerAPIによる訓練・評価（精度93%達成）、Hubへのモデルプッシュまでをカバーしている。コードレスのアプローチとしてAutoNLPも紹介されており、CSVをアップロードするだけでモデル訓練・評価・デプロイが自動化される。

第3に、Tweepyを用いたTwitterからのリアルタイムデータ取得と感情分析パイプラインの統合方法を示している。APIキー認証後、`tweepy.Client.search_recent_tweets`で直近7日間のツイートを取得し、感情分析モデルに投入することで、特定トピックに関する世論動向をリアルタイムで把握できる。

監査エージェント開発への示唆として、本記事のパイプライン構造（データ取得→前処理→推論→ラベリング）は、監査証跡テキストや内部統制ドキュメントの自動分類・リスクスコアリングに直接応用可能である。特にDistilBERTのような軽量モデルをファインチューニングして内部監査固有のラベル体系（リスク高・中・低、異常・正常等）で再訓練するアプローチは、LLMを用いた判定コストを抑えながらスケーラブルな自動化を実現する手段として有効である。

## アイデア

- transformersのpipelineクラスは5行でSOTAモデルを呼び出せる抽象化レイヤーであり、モデルIDを差し替えるだけで多言語・ドメイン特化モデルに切り替えられる設計は、監査AIシステムにおけるモデル交換可能なアーキテクチャの参考になる
- DistilBERT（BERT比40%小型・60%高速）をIMDBデータで再訓練して93%精度を達成している点は、ローカルLLMインフラ（RTX 3090）上で軽量モデルをドメイン特化ファインチューニングする際のベースラインとして活用できる
- AutoNLPによるノーコードファインチューニングはMLOpsの民主化事例であり、非エンジニアのドメイン専門家（監査担当者等）が独自分類モデルを構築・運用できる可能性を示している

## 前提知識

- **BERT / DistilBERT** (TODO: 読むべき)
- **Transformer fine-tuning** (TODO: 読むべき)
- **Hugging Face pipeline** (TODO: 読むべき)
- **トークナイズ・パディング** (TODO: 読むべき)
- **NLP分類タスク** (TODO: 読むべき)

## 関連記事

- /deep_1214 LoRAを用いたRoBERTa・Llama 2・Mistral 7Bの災害ツイート分類性能比較
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[PythonによるSentiment Analysis入門：事前学習モデルの活用からファインチューニングまで](https://huggingface.co/blog/sentiment-analysis-python)
