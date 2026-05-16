---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-24
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, LiDAR, マルチモーダル, DriveGPT4, PromptTrack]
category: "ai-ml"
related: [2663, 1527, 1297, 182, 1817]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-24T12:51:16.443220"
---

## 要約

本記事はThe Gradientに掲載された解説記事で、LLM（大規模言語モデル）が自動運転に応用される可能性を整理したものである。自動運転の従来アーキテクチャは「モジュール型」と「End-to-End学習」の2種類に大別される。モジュール型は知覚（Perception）・自己位置推定（Localization）・経路計画（Planning）・制御（Control）を個別モジュールで実装する設計で、解釈性が高い反面、モジュール間の誤差伝播が問題となる。End-to-Endは単一ニューラルネットワークで操舵・加速を直接予測するが、ブラックボックス問題が残る。そこに第3の選択肢としてLLMを活用するアプローチが登場した。LLMの基本構造はTokenization（テキスト→数値変換）とTransformer（Encoder-Decoder）であり、次トークン予測を繰り返すことで文章を生成する。自動運転への適用では、入力をカメラ画像・LiDAR点群・RADARデータとしてトークン化し（Vision Transformerが担う）、Transformerは同一のまま維持し、出力タスクを自動運転タスク（車線変更、停止判断等）に変更する構成が基本となる。研究が活発な応用領域は4つ：(1) Perception（HiLM-D、MTD-GPT、PromptTrackなどが物体検出・追跡を自然言語で出力）、(2) Planning（DriveGPT4、DriveVLM、LMDriveなどが鳥瞰図または知覚出力を入力に行動を生成）、(3) Generation（ScenarioDiffusion等がLiDAR・HD地図を拡散モデルで合成し学習データ増強）、(4) Q&A（DriveLLMなどがシナリオへの自然言語質問に回答）。LLMを自動運転に使う主な利点は3点：常識的推論（信号機の色が変わっても直進するかどうかの判断等）、Few-Shot学習による新シナリオへの汎化、多センサーデータの統合的処理である。一方で課題も明確で、LLM特有の「ハルシネーション」（事実と異なる応答の生成）がリアルタイム走行制御に組み込まれた場合の安全性リスク、推論速度（GPT-4は数秒オーダー）とリアルタイム性（数十ms以下）の乖離、LiDAR・RADARなど非テキストデータの効率的なトークン化手法の未成熟が挙げられる。現状では研究フェーズであり、完全自動運転の実用化にはこれらの技術的課題を解決する必要がある。監査エージェント開発との関連性としては、複数の異種データソース（構造化・非構造化）を統合し、自然言語で説明可能な意思決定を行うアーキテクチャ設計の参考になる。特にQ&Aアプローチで「なぜそのルートを選んだか」を自然言語で説明できる点は、監査証跡の生成・説明責任の担保と構造的に同一の問題設定である。

## アイデア

- 自動運転のPlanningモジュールをLLMに置き換えると「なぜその判断をしたか」を自然言語で説明できるようになり、説明可能なAI（XAI）として機能する点が監査証跡生成と構造的に同一の問題設定である
- LiDAR点群・カメラ画像・RADARといった異種センサーデータをすべてトークンに変換してTransformerに統合入力する設計は、監査エージェントが財務データ・ログ・契約書を統一的に扱う際のアーキテクチャ参考になる
- ScenarioDiffusionのような拡散モデルによる学習データ自動生成（エッジケースの合成）は、監査シナリオの希少ケース（不正パターン等）のデータ増強に応用可能な発想である

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **LiDAR点群処理** (TODO: 読むべき)
- **Few-Shot学習** → /deep_232 PointRFT：点群Few-shot学習のための強化ファインチューニング

## 関連記事

- /deep_2663 マルチモーダル全天球3D屋外データセットによる場所カテゴリ分類
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_182 AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ
- /deep_1817 AIが中小セラーの商品開発を変える：AlibabaのAccioが示すAIソーシング・エージェントの実態

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
