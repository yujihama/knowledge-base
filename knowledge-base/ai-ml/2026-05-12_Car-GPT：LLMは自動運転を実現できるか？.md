---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-12
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, Explainability, GPT-Driver, DriveLM, PromptTrack]
category: "ai-ml"
related: [5220, 1266, 1760, 1449, 2449]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-12T21:35:06.848424"
---

## 要約

本記事は2024年3月にThe Gradientに掲載された解説記事で、LLM（大規模言語モデル）が自動運転技術にどう応用されるかを体系的に整理している。自動運転の従来アプローチは「モジュラー型」（Perception→Localization→Planning→Controlの分離モジュール）と「End-to-End学習」（単一ニューラルネットが操舵・加速を直接予測）の2系統に大別されるが、どちらも完全自律走行を未達成のまま。そこへLLMを組み込む研究が2023年以降活性化した。LLMの基本構造はTokenization（テキスト→数値変換）とTransformer（Encoder-Decoder構造、Multi-head Attention、Next-word Prediction）からなる。自動運転への適用では入力をカメラ画像・LiDAR点群・RADARデータなどに拡張し、Vision TransformerやVideo Vision Transformerでトークン化することで既存Transformerをほぼそのまま流用できる。研究対象として活発なのは①Perception（HiLM-D、MTD-GPT、PromptTrackによる物体検出・追跡・ID付与）、②Planning（GPT-Driverによる言語化されたPlanning、DriveLMによるグラフ構造のQ&A）、③データ生成（Diffusionモデルを用いた合成トレーニングデータ・シナリオ生成）、④Q&A（シーン状況への自然言語回答）の4領域。LLM固有の強みとして「Explainability（説明可能性）」が挙げられており、なぜその操舵判断をしたかを人間が理解できる言語で出力できる点は、従来のブラックボックス型End-to-Endモデルにない特長とされる。一方で課題も明示されており、①レイテンシ（推論速度の遅さ）、②実世界での未検証性、③大量のリソース消費が普及の障壁として指摘されている。記事は入門向けの平易な文体だが、言及される論文・モデル（PromptTrack、GPT-Driver、DriveLM等）は実際の研究成果に基づく。監査エージェント開発への示唆としては、「自律走行×説明可能性」という構造が監査エージェントにおける「判断根拠の言語化」と同型であることに注目できる。LLMがセンサーデータを受け取り自然言語で意思決定を説明するアーキテクチャは、監査証跡の自動生成や判断理由のトレーサビリティ確保に直接応用可能な設計パターンを提供する。

## アイデア

- LLMによる自動運転の最大の付加価値は精度向上ではなく『Explainability（説明可能性）』であり、判断根拠を自然言語で出力できる点が従来のEnd-to-Endモデルと本質的に異なる
- Vision TransformerによるLiDAR・RADAR・カメラデータのトークン化により、自動運転の4モジュール（Perception/Localization/Planning/Control）をLLMのEncoder-Decoder構造に統合できるアーキテクチャが成立している
- DriveLMのようにグラフ構造のQ&Aとして運転シナリオを表現するアプローチは、複雑な意思決定プロセスを構造化されたチェーンとして追跡可能にし、監査エージェントの判断ログ設計に転用できる

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Multi-head Attention** → /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **LiDAR点群** (TODO: 読むべき)

## 関連記事

- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_2449 静的ペルソナを超えて：LLMのための状況依存パーソナリティ制御

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
