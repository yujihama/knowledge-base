---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-29
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, DriveGPT4, PromptTrack, Diffusion Model, 説明可能AI]
category: "ai-ml"
related: [3717, 4439, 1346, 3260, 3353]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-29T09:24:30.361798"
---

## 要約

本記事はThe Gradient掲載（2024年3月）の解説記事で、LLM（大規模言語モデル）を自動運転に適用する研究動向を体系的に整理している。

自動運転の従来アプローチは「モジュール型」と「エンドツーエンド学習」の2系統に大別される。モジュール型はPerception・Localization・Planning・Controlの4段階を個別モジュールで実装するが、モジュール間の誤差伝播が問題となる。エンドツーエンド学習は単一ニューラルネットワークで操舵・加速度を直接予測するが、ブラックボックス問題が残る。LLMはこの両方の限界を補う可能性として注目されている。

LLMの基本構造として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造を持つTransformerアーキテクチャ、次単語予測（next-word prediction）の3要素を説明。GPT系は純粋なDecoder型、BERTはEncoder型と整理される。

自動運転へのLLM適用は入力・出力の置き換えで実現できる。入力は画像・LiDARポイントクラウド・RADARデータ等をVision Transformer（ViT）でトークン化、出力は「車線変更せよ」等のドライビングコマンドやシーン記述に変更する。

2023年時点の主要研究領域は以下の4つ：
1. **Perception**：GPT-4 Visionが画像からオブジェクトを検出・記述。HiLM-D、MTD-GPTが動画対応、PromptTrackがDETRとLLMを組み合わせオブジェクトIDの一貫追跡を実現。
2. **Planning**：DriveGPT4やDriveLMが視覚的シーン理解から行動計画を生成。BEV（Bird's Eye View）表現と組み合わせることで交差点等の複雑シナリオに対応。
3. **データ生成（Generation）**：拡散モデル（Diffusion Model）を用いて代替シナリオや学習データを合成。稀少シナリオのデータ拡張に活用。
4. **Q&Aインターフェース**：自然言語でシナリオに関する質問に答えるチャットUI。乗客への説明や遠隔操作支援に応用可能。

LLMの自動運転への強みとして、常識推論（歩行者が傘を持っていれば雨天と判断）、自然言語による説明可能性（XAI）、少数サンプル学習（Few-shot learning）が挙げられる。一方、課題はリアルタイム性（LLMの推論遅延）、センサーデータへの直接対応、安全保証の困難さである。

監査エージェント開発への示唆：LLMをブラックボックスなEnd-to-Endシステムに組み込む際の「説明可能性確保」の手法（自然言語での行動根拠生成）は、監査AIにおける判断ログ・根拠提示の設計に直接応用できる。また、モジュール型→E2E→LLM統合という進化パターンは、監査エージェントのアーキテクチャ選択の参考になる。

## アイデア

- LLMの「常識推論」能力（傘→雨天推定等）をPerceptionモジュールに組み込むことで、従来のルールベース検出では対応困難な暗黙的コンテキスト理解が可能になる点
- 自然言語での行動根拠生成により、エンドツーエンドモデルのブラックボックス問題を部分的に解決できる設計パターンは、説明可能性が求められる他ドメイン（監査・医療等）にも横展開できる
- LiDAR・RADAR等の非テキストセンサーデータをVision Transformerでトークン化してLLMに入力する手法は、テキスト以外のモダリティ統合の汎用的フレームワークとして注目に値する

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク

## 関連記事

- /deep_3717 今AIで重要な10のこと：LLMs+時代の到来
- /deep_4439 Pragmos：プロセスエージェント型モデリングシステム
- /deep_1346 LLM述語からLogic Tensor Networkへ：規制調達における神経記号的オファー検証
- /deep_3260 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_3353 LLMs+：今AIで重要な10のこと（MIT Technology Review）

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
