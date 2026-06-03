---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-03
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, GPT-4 Vision, LanguageMPC, PromptTrack, DriveGPT4, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-03T21:21:14.756216"
---

## 要約

自動運転システムは従来、Perception（知覚）・Localization（位置推定）・Planning（計画）・Control（制御）という4つのモジュールに分割する「モジュール型アプローチ」が主流だった。2010年代にはEnd-to-End学習（単一ニューラルネットワークでステアリングと加速度を直接予測する手法）が台頭したが、ブラックボックス問題が課題として残った。本記事はこの文脈で「LLMが自動運転の突破口になるか」を検討する入門的解説記事である。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、エンコーダー・デコーダーアーキテクチャで構成されるTransformer、そしてNext-Word Predictionの仕組みを説明する。GPTは純粋なデコーダー型であり、Multi-head AttentionやLayer Normalizationを中核とする。

自動運転へのLLM適用においては、入力をViSion Transformerを用いて画像・LiDAR点群・RADARデータをトークン化することで対応可能とする。2023年時点での主要な研究領域は以下の4つ：

1. **Perception（知覚）**：GPT-4 Visionを用いた物体検出・追跡・予測。HiLM-D、MTD-GPT、PromptTrack（DETRとLLMの組み合わせ）等が代表的。PromptTrackは物体にユニークIDを付与する4D知覚的機能を持つ。

2. **Planning（計画）**：自然言語で運転判断（直進・車線変更等）を記述。DriveGPT4はMistral-7Bベースで視覚入力から運転行動を説明。GPT-Driverはルートプランニングにn-shot prompting（例3件でも精度向上）を活用。LanguageMPCはLLMを高レベルプランナーとして利用しモデル予測制御と統合する。

3. **データ生成**：拡散モデルを用いた合成訓練データ・代替シナリオの生成。

4. **Q&A（説明可能性）**：シナリオに基づく対話的質問応答インターフェース。

LLMの自動運転への適用における主な課題は「ハルシネーション（幻覚）」であり、実際には存在しない物体を認識する危険性がある。また、リアルタイム処理性能・エッジデバイスへの展開コスト・長尾分布（稀なコーナーケース）への対応も未解決問題として挙げられる。

監査エージェント開発への示唆として：マルチモーダル入力（画像・構造化データ・テキスト）をトークン統一で扱うアーキテクチャ設計、n-shot promptingによる少数事例からの推論精度向上、LLMを高レベル意思決定エージェントとして位置づけ既存制御ロジックと統合するハイブリッド構成（LanguageMPCに類似）は、監査エージェントのReActループ設計においても参照価値がある。

## アイデア

- LanguageMPCのようにLLMを高レベルプランナーとして機能させ、従来の数値制御アルゴリズム（MPC）と組み合わせるハイブリッド構成は、監査エージェントでLLMによる判断と既存ルールベース検証を統合する設計に直接応用できる
- GPT-Driverのn-shot promptingアプローチ：3例程度のコンテキスト例を与えるだけで経路計画精度が向上するという知見は、少ないラベルデータで高精度な判断が求められる監査シナリオでの推論設計に示唆を与える
- PromptTrackがDETR（物体検出器）とLLMを組み合わせて固有IDを付与する設計は、エンティティ追跡（監査証跡上の同一取引・同一エンティティの連続追跡）を行うエージェント設計のアナロジーとして参考になる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **n-shot prompting** (TODO: 読むべき)
- **モデル予測制御（MPC）** (TODO: 読むべき)

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
