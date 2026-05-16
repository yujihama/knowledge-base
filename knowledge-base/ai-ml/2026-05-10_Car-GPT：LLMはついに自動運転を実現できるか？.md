---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-10
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, DriveVLM, LanguageMPC, Explainability]
category: "ai-ml"
related: [1266, 1760, 1449, 2449, 1969]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-10T21:45:21.315492"
---

## 要約

本記事は、Large Language Model（LLM）を自動運転車に適用する可能性を体系的に解説した入門的レビュー記事である。自動運転の従来アプローチとして、Perception・Localization・Planning・Controlの4モジュールからなる「モジュラー型」と、単一ニューラルネットワークで操舵・加速を直接予測する「End-to-End学習」の2系統を整理したうえで、LLMがその代替または補完となり得るかを論じる。LLMの基本構造として、テキストをトークン列に変換するTokenization、Encoder-Decoder構造のTransformerアーキテクチャ（Multi-Head Attention, Layer Normalization等）、そして次単語予測（Next-Word Prediction）の仕組みを概説する。自動運転へのLLM適用では、入力をカメラ画像・LiDARポイントクラウド・RADARデータ等にTokenize（Vision Transformerを利用）し、出力をレーン変更などの運転タスクに置き換えるという設計が基本方針となる。具体的な研究事例として、Perception領域ではGPT-4 Visionによる物体検出・記述、HiLM-D・MTD-GPT（画像/動画ベースの検出・予測・追跡）、PromptTrack（DETRと LLMを組み合わせた固有ID付与による4Dトラッキング）を紹介。Planning領域では、DriveVLM・DriveLM（ドライブシーンへのQ&A）、SurrealDriver（LLMによるドライバー行動のシミュレーション）、LanguageMPC（LLMをMPC制御のハイレベルプランナーとして使用）などを挙げる。Generation領域では、Diffusionモデルとの組み合わせによるトレーニングデータ・代替シナリオ生成を紹介。また、LLMにより「なぜその判断をしたか」を自然言語で説明できる点（Explainability）が、モジュラー型・E2Eアーキテクチャ双方のブラックボックス問題に対する解決策になり得ると指摘する。ただし実用上の課題として、推論レイテンシ（リアルタイム性）、センサーデータ処理の計算コスト、安全性の保証など未解決の問題も残ると締めくくる。監査エージェント開発への示唆としては、LLMをPlanningの「ハイレベルな判断層」として使い、下位の実行モジュール（MPC等）と組み合わせるLanguageMPCのアーキテクチャは、LangGraphベースの監査エージェントにおける「LLMによる戦略決定＋ツール実行」という階層設計と構造的に類似しており参考になる。

## アイデア

- LanguageMPCのアーキテクチャ（LLMをハイレベルプランナー、MPCを低レベル制御器として分離）は、監査エージェントのLLM-as-orchestrator設計に直接応用できる分離原則を体現している
- PromptTrackのように既存の特化型モデル（DETR等）とLLMを組み合わせるハイブリッド設計は、LLMの弱点（リアルタイム性・計算コスト）を補いながら自然言語推論能力を活かす現実的な統合戦略を示している
- 自動運転における「なぜその判断か」のExplainability問題は、監査AIの説明可能性要件と同根であり、LLMによる自然言語出力がブラックボックスE2Eモデルの監査適合性を高める手段として機能し得る

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Model Predictive Control (MPC)** (TODO: 読むべき)
- **Diffusionモデル** → /deep_3423 LLMs+：今AIで重要な10のこと

## 関連記事

- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_2449 静的ペルソナを超えて：LLMのための状況依存パーソナリティ制御
- /deep_1969 階層的SVGトークン化：スケーラブルなベクターグラフィックスモデリングのためのコンパクトな視覚プログラム学習

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
