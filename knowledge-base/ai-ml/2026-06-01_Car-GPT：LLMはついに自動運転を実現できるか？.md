---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-01
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, PromptTrack, GPT-4 Vision, Diffusion]
category: "ai-ml"
related: [4015, 5220, 1266, 1760, 1449]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-01T21:34:54.536096"
---

## 要約

自動運転の歴史的アプローチは「モジュラー方式」（Perception・Localization・Planning・Controlの分離）と「End-to-End学習」（単一ニューラルネットワークによる操舵・加速予測）の2つが主流だったが、どちらも完全な自動運転を実現できていない。本記事は、LLMをこの問題の「予期せぬ解」として検討する。LLMの基本構造はTokenization（テキストを数値列に変換）とTransformer（Encoder-Decoder構造、Multi-head Attention等）による次単語予測であり、入力をテキストから画像・LiDARポイントクラウド・RADARデータ等に置き換えることで自動運転へ転用できる。Vision Transformerがこの橋渡し役を担う。自動運転タスクへのLLM適用として2023年の主要研究領域は4つ。①Perception：GPT-4 VisionやHiLM-D、MTD-GPTが画像から物体・車線等を検出。PromptTrackはDETR物体検出器とLLMを組み合わせ、物体に固有IDを付与するトラッキングも実現。②Planning：LanguageMPC、DriveVLM等がbird-eye viewや知覚出力から「車線変更すべきか」等の行動決定を行う。③Generation：Diffusionモデルを用いたトレーニングデータ生成・代替シナリオ生成により、データ不足問題に対応。④Q&A：チャットインターフェース経由でシナリオに関する質問応答。LLMの強みとして、膨大なテキストコーパスから蒸留された「常識的推論能力」がある。例えば「赤信号＝停止」という知識を明示的にプログラムせずとも推論できる点は、エッジケース対応において従来手法より優位。一方で課題もある。LLMの推論レイテンシは自動運転の要求するリアルタイム応答（ミリ秒オーダー）に対して現時点では遅すぎる。また安全クリティカルな判断における解釈可能性（Explainability）の担保も未解決。著者はLLMを自動運転の「万能解」とは見ておらず、既存モジュラーシステムの補完的コンポーネントとして段階的に統合するアプローチが現実的と結論付けている。監査エージェント開発への示唆としては、複数の専門モジュール（知覚・計画・制御に相当するリスク検出・証拠収集・判断）をLLMで統合するアーキテクチャ設計の参考になる。特にEnd-to-Endとモジュラーのトレードオフ（解釈可能性 vs 性能）は監査AIでも同様の設計課題として存在する。

## アイデア

- LLMの「常識的推論能力」（赤信号で止まる等）をゼロショットで自動運転に転用できる点は、ルールベース設計の限界を超えるアプローチとして興味深い
- PromptTrackのようにDETR等の既存物体検出器とLLMを組み合わせるハイブリッド構成は、監査エージェントでの「専門ツール＋LLM統合」パターンと構造的に同一
- データ生成（Diffusion）をLLMパイプラインに組み込んでエッジケースの訓練データを自動生成する発想は、監査シナリオの自動生成にも応用可能

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer (Encoder-Decoder)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ
- **Diffusionモデル** → /deep_3423 LLMs+：今AIで重要な10のこと

## 関連記事

- /deep_4015 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
