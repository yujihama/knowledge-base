---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-20
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, マルチモーダル, PromptTrack]
category: "ai-ml"
related: [1527, 1297, 182, 1817, 17]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-20T12:53:23.638142"
---

## 要約

本記事はThe Gradientに掲載された解説記事で、Large Language Model（LLM）を自動運転に応用する研究動向を体系的に紹介している。自動運転の従来アーキテクチャは「モジュール型」（Perception・Localization・Planning・Controlの4分割）と「End-to-End学習」（単一ニューラルネットが操舵・加速を直接予測）に大別されるが、いずれも自動運転問題を完全には解決していない。そこでLLMをこの領域に適用する研究が2023年を中心に活発化した。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoderまたは純Decoder構造のTransformerブロック（Multi-head Attention・Layer Normalizationなど）、そして次単語予測（Next-word Prediction）という3要素を解説している。自動運転への転用では、入力を画像・LiDAR点群・RADARデータなどに置き換えてトークン化し（Vision Transformer / Video Vision Transformerと同様の手法）、出力タスクを走行指示や環境記述に変更する形をとる。

研究が最も活発な応用領域は4つ。①Perception：GPT-4 Visionによる画像内オブジェクト記述、HiLM-D・MTD-GPTによる映像理解、PromptTrack（DETRとLLMを組み合わせ物体にユニークIDを付与）など。②Planning：入力画像や俯瞰図から「直進継続」「車線変更」などの行動を記述・推論する研究。③Data Generation：Diffusionモデルを用いた学習データやシナリオの自動生成。④Q&A Interface：シーンに基づいてLLMが質問に答えるチャットUI。

記事はLLMが自動運転の「ペニシリン的解答」になり得るという仮説を提示しつつ、現時点では研究段階であり、既存モジュール型・End-to-End手法との比較や実用化には課題が残ることも示唆している。監査エージェント開発の観点では、マルチモーダルトークン化（構造化データ・非構造化データの統一入力）と、単一モデルによるPerception→Planningの統合的推論というアーキテクチャ設計思想が参考になる。複数の異種データソース（財務数値、テキスト、ログ）を統一的にトークン化してエージェントに渡すRAGパイプライン設計に直接応用可能なアイデアである。

## アイデア

- LiDAR点群・RADAR・画像などの異種センサーデータをトークン化して統一的にTransformerに入力する手法は、監査エージェントが財務数値・テキストログ・構造化DBを単一モデルで処理する設計に転用できる
- PromptTrackのようにDETR（既存特化モデル）とLLMを組み合わせるハイブリッド構成は、既存の監査ルールエンジンとLLMを併用するアーキテクチャのアナロジーとして有用
- 自動運転のPlanning層をLLMに置き換える発想（画像→行動記述）は、監査エージェントのReActループにおけるPlanning stepをLLMに委譲する設計根拠を強化する

## 前提知識

- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_182 AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ
- /deep_1817 AIが中小セラーの商品開発を変える：AlibabaのAccioが示すAIソーシング・エージェントの実態
- /deep_17 AI vs. アンチボット：LLMが書き換えるウェブスクレイピングの全ルール

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
