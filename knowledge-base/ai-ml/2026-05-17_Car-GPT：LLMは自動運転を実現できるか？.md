---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-17
tags: [LLM, 自動運転, End-to-End学習, Vision Transformer, Perception, Planning, マルチモーダル, GPT-4 Vision, PromptTrack]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-17T21:23:48.226624"
---

## 要約

本記事はThe Gradientに掲載された解説記事で、大規模言語モデル（LLM）が自動運転の4つの主要モジュール（Perception・Localization・Planning・Control）をどのように代替・補完できるかを概観する。

自動運転のアーキテクチャは2010年代の「モジュール型」（各機能を独立したモジュールで実装）から、単一ニューラルネットワークでステアリングと加速を予測する「End-to-End学習」へと移行しつつある。しかしいずれもブラックボックス問題や汎化性能の限界を抱えており、LLMが「予期せぬ解答」になり得るかが問われている。

LLMの基礎として、テキストを数値トークンに変換する「トークン化」、Encoder-Decoder構造を持つ「Transformer」、そして「次単語予測」による出力生成の3点が解説される。自動運転への応用では、入力をカメラ画像・LiDAR/RADARの点群データ・アルゴリズム出力（車線・物体等）としてトークン化し、既存のTransformerアーキテクチャをほぼそのまま利用する形が提案される。

2023年時点で活発な研究領域は以下の4つ：
1. **Perception**：入力画像から環境・物体を記述。GPT-4 VisionによるObject Detection、HiLM-D・MTD-GPT・PromptTrack（DETRと組み合わせてユニークID付与）などが具体例として挙げられる。
2. **Planning**：画像やBird-Eye Viewから「直進を維持する」「車線変更する」等の行動を記述・推論。LLMの常識的推論能力（commonsense reasoning）が活用できる可能性がある。
3. **データ生成**：Diffusionモデルを組み合わせた学習データ・代替シナリオの生成。
4. **Q&A インターフェース**：シナリオに基づく自然言語でのチャット型問答システム構築。

Vision Transformer（ViT）やVideo Vision Transformerを使って画像を「視覚トークン」として扱う技術がLLMとの統合の鍵であり、マルチモーダル入力（画像＋センサー＋地図情報）を単一モデルで処理するアプローチが研究の主流となっている。

監査エージェント開発への示唆：LLMによるPerception→Planning→Actionの統合パイプラインは、監査エージェントにおける「証拠収集→リスク判断→対応アクション生成」のフローと構造的に類似する。特にPromptTrackのようにオブジェクトにIDを付与して追跡する手法は、監査トレール上のエンティティ（取引・仕訳・承認者）のトラッキングに応用可能なアーキテクチャ上のヒントを与える。

## アイデア

- テキスト用LLMのトークン化・Transformerアーキテクチャをほぼ変更せず、入力データ（LiDAR点群・カメラ画像）をトークンとして扱うだけで自動運転タスクに転用できるという設計の汎用性
- PromptTrackのようにLLMとDETRを組み合わせてオブジェクトに一意IDを付与・追跡する手法は、監査エージェントにおけるエンティティ（取引・承認者）追跡に構造的に応用できる可能性
- LLMの「常識的推論能力」をPlanningモジュールに活用することで、ルールベースでは記述困難なエッジケース（珍しい交通状況）への対応力が向上するという仮説

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
