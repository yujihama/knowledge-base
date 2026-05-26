---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-26
tags: [LLM, 自動運転, Vision Transformer, Planning, Perception, エンドツーエンド学習, DriveVLM, Explainability]
category: "ai-ml"
related: [716, 5220, 1266, 1760, 1449]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-26T21:35:48.799842"
---

## 要約

自動運転技術は2010年代から「モジュール型」アプローチ（Perception・Localization・Planning・Controlの4モジュール構成）が主流だったが、近年はエンドツーエンド学習（単一ニューラルネットワークでステアリング・加速度を直接予測）への移行が進んでいる。本記事はLLMがこの問題の「予期せぬ解」になりうるかを検討する。

LLMの基本構造として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoderアーキテクチャを持つTransformer、次単語予測（Next-Word Prediction）の3要素を説明。自動運転への適用では、入力をカメラ画像・LiDARポイントクラウド・RADARデータ等に拡張し（Vision Transformerを活用）、出力を運転タスク（車線変更等）に置き換える形で応用可能とする。

研究が活発な4分野として、①Perception（HiLM-D・MTD-GPT・PromptTrackによる物体検出・予測・追跡）、②Planning（DriveVLM・DriveMLM・GPT-Driver等がBEVや言語命令から軌道生成）、③生成（diffusionによる訓練データ・代替シナリオ生成）、④Q&A（シナリオへの質問応答チャットインターフェース）を挙げる。

Planning分野では、LLMが「なぜその行動をとったか」を自然言語で説明できる点（Explainability）が従来のブラックボックス型エンドツーエンド手法に対する明確な優位性として強調される。DriveVLMはVision-Language Modelを用いてシーン理解と軌道計画を統合し、DriveMLMはマルチモーダル入力から判断根拠を出力する。

一方で課題も明確に指摘される。①レイテンシ：LLMの推論速度（数秒オーダー）は自動運転の要求するリアルタイム性（ミリ秒オーダー）と乖離が大きい。②ハルシネーション：LLMが事実と異なる情報を生成するリスクは安全クリティカルなシステムでは致命的。③センサーデータ処理：LiDAR等の3Dポイントクラウドを効率的にトークン化する手法が未成熟。

総括として、LLMは現時点でPerceptionとPlanningのサブタスクに有望な成果を示しており、特に説明可能性と自然言語による指示理解において既存手法を補完できる。ただし完全自律運転のエンドツーエンド置換にはレイテンシとハルシネーション問題の解決が不可欠であり、近未来的には「モジュール型＋LLMハイブリッド」構成が現実的な方向性と示唆される。監査エージェント開発への示唆として、LLMがブラックボックス的判断に対して自然言語での説明根拠を付与する仕組みは、監査証跡の自動生成・判断理由の説明可能性確保に直接応用できる設計パターンである。

## アイデア

- LLMのNext-Word Predictionをステアリング・加速度の「次行動予測」に読み替えることで、自然言語処理と運転制御を同一アーキテクチャで扱える点が構造的に興味深い
- DriveVLMのように判断根拠を自然言語で出力する設計は、自動運転に限らず監査エージェント等の安全クリティカルシステムで説明可能性を担保するアーキテクチャパターンとして汎用性が高い
- レイテンシ問題の解決策として、LLMをリアルタイム制御層ではなく「高レベル意思決定・シーン解釈層」に限定し、低レイテンシの従来モジュールと組み合わせるハイブリッド構成が現実解として浮上している

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **Multimodal LLM** → /deep_369 視覚的In-Contextデモンストレーション選択の学習
- **BEV（Bird's Eye View）** (TODO: 読むべき)
- **ハルシネーション** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
