---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-22
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, Diffusion Model, GPT-4V, DriveGPT4, PromptTrack]
category: "ai-ml"
related: [3717, 3260, 3353, 3453, 3559]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-22T09:27:51.590029"
---

## 要約

本記事はThe Gradientに掲載された解説記事で、Large Language Model（LLM）を自動運転に応用する研究動向を2024年時点でまとめたものである。

自動運転の従来アーキテクチャは「モジュラー型」であり、Perception・Localization・Planning・Controlの4モジュールを順次処理する設計だった。2010年代後半からはEnd-to-End学習が台頭し、単一ニューラルネットワークがステアリングや加速を直接出力するアプローチが研究されているが、ブラックボックス問題が課題として残る。

LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-Decoderアーキテクチャを持つTransformer、そしてNext-Word Predictionによる出力生成の3要素が説明される。Vision Transformer（ViT）やVideo Vision Transformerにより、画像・LiDAR点群・RADARデータもトークン化可能であり、Transformerアーキテクチャ自体は入力種別に依存しない。

LLMが自動運転で貢献できるタスクとして以下が挙げられる：
- **Perception**：GPT-4 Visionが入力画像から物体・車線を記述。HiLM-D・MTD-GPTが検出・予測・追跡を実行。PromptTrackはDETRとLLMを組み合わせ物体にユニークIDを付与。
- **Planning**：DriveVLMやDriveGPT4がBird-Eye-View画像を入力に「直進」「車線変更」等の行動を出力。GPT-Driverはテキスト形式でシーン記述を行いウェイポイントを生成。
- **Data Generation**：拡散モデル（Diffusion Model）を活用し、エッジケースを含むシナリオ画像・動画を合成してトレーニングデータを補完。ChatSimやDriveDreamerが代表例。
- **Q&A Interface**：DriveLM・NuScenesQAなどがドライビングシーン上でQA形式の推論を実現。

主要な課題として、LLMの推論レイテンシ（例：GPT-4は数百ms〜秒単位）がリアルタイム制御の要件（数十ms以下）を満たさないこと、大規模モデルの車載計算リソースへの搭載困難性、センサーとLLMの統合パイプライン設計の複雑さが指摘される。

監査エージェント開発への示唆：LLMをPerceptionとPlanningの分離モジュールとして活用し、自然言語でのシーン解釈と行動根拠の説明可能性を確保するアーキテクチャは、監査エージェントにおける「証拠→判断→根拠説明」の構造と類似している。DriveGPT4のように多段階推論を自然言語で透過的に行う手法は、監査判断の説明可能性（Explainability）要件に直接応用可能である。

## アイデア

- LiDAR点群・RADAR・カメラ画像をすべてトークン化してTransformerに統一入力できるという設計思想は、マルチモーダルエージェントのセンサー統合アーキテクチャに転用可能
- DriveGPT4のように自然言語でステップバイステップの推論を行いウェイポイントを生成するアプローチは、LLM-as-judgeにおける根拠付き判断の出力フォーマット設計に示唆を与える
- エッジケースデータ不足をDiffusion Modelで合成補完する手法は、監査データの希少ケース（不正パターン等）に対するデータ拡張戦略として応用できる

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **Bird-Eye-View** (TODO: 読むべき)

## 関連記事

- /deep_3717 今AIで重要な10のこと：LLMs+時代の到来
- /deep_3260 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_3353 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_3453 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_3559 LLMs+：今AIで重要な10のこと（MIT Technology Review）

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
