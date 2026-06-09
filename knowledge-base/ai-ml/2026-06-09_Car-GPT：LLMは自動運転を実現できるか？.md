---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-09
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, PromptTrack, GPT-4 Vision, Diffusion, BEV]
category: "ai-ml"
related: [4015, 5535, 5220, 1266, 1760]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-09T21:17:15.363648"
---

## 要約

自動運転の歴史は2010年代のモジュール型アプローチ（Perception・Localization・Planning・Controlの4分割）から始まり、その後End-to-End学習（単一ニューラルネットワークで操舵・加速を予測）へと移行した。しかしどちらも自動運転の完全実現には至っていない。本記事はLLMをこの問題の「予期せぬ答え」として位置づけ、自動運転への適用可能性を体系的に整理する。

LLMの基礎として、テキストをトークン（数値）に変換するトークナイゼーション、Encoder-Decoder構造を持つTransformerアーキテクチャ（Multi-head Attention・Layer Normalization等を含む）、および次単語予測タスクを解説。GPT系モデルはDecoder-onlyである点も言及される。

自動運転への適用では、入力をカメラ画像・LiDAR点群・RADAR点群・アルゴリズム出力（車線・物体等）に拡張し、Vision TransformerやVideo Vision Transformerによりトークン化する構成を取る。出力は「シーンの説明」から「車線変更」等の直接制御指令まで多様。

2023年時点で活発な研究領域は4つ：(1) **Perception**：GPT-4 Visionによる物体検出・PromptTrack（DETRとLLMを組み合わせ物体IDを付与）・HiLM-D・MTD-GPTによる検出・予測・追跡。(2) **Planning**：BEV（Bird's Eye View）や知覚出力を入力とし、「直進維持」「譲る」等の行動選択を生成。(3) **Generation**：Diffusionモデルを用いた訓練データ生成・代替シナリオ生成。(4) **Q&A**：シナリオに基づくチャットインターフェース構築。

課題として、リアルタイム推論の遅延（LLMの応答速度が車両制御の要求に追いつかない可能性）、センサーデータのトークン化コスト、ブラックボックス性、および安全性検証の困難さが挙げられる。LLMは「完全な自動運転の解」ではなく、既存モジュールを補強する形での活用が現実的と示唆される。監査AIへの示唆として、自動運転のPlanning層における意思決定の説明可能性要件は、監査エージェントのReasoningトレース設計と構造的に類似しており、LLM-as-judgeによる行動正当化ログの設計に参照できる視点を提供する。

## アイデア

- 自動運転のPlanning層をLLMに置き換える発想は、監査エージェントの意思決定モジュール（何をチェックするか・どう優先順位付けするか）をLLMで代替する設計と同型であり、ReActループへの応用が直接的に考えられる
- PromptTrackのように既存の特化型検出器（DETR等）とLLMを組み合わせるハイブリッド構成は、完全End-to-End化よりも実用性が高く、既存監査ルールエンジンとLLMを並列運用する監査システム設計に示唆を与える
- Diffusionによる訓練データ・代替シナリオ生成は、監査での異常シナリオ合成（レアケースのデータ拡張）に転用可能であり、RLAIF的なフィードバックループ構築の文脈で重要な技術要素となる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークナイゼーション** → /deep_2269 VideoFlexTok：粗から細へのコース・トゥ・ファイン動画トークナイゼーション
- **Diffusionモデル** → /deep_3423 LLMs+：今AIで重要な10のこと

## 関連記事

- /deep_4015 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_5535 GEM: 変形可能Mambaによるリダールワールドモデル生成
- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
