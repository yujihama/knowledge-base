---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-19
tags: [自動運転, LLM, Vision Transformer, End-to-End学習, Perception, Planning, PromptTrack, DriveVLM, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-19T21:33:14.942129"
---

## 要約

本記事は、自動運転の課題にLLM（大規模言語モデル）を適用する可能性を解説した入門的な技術解説である。自動運転の従来アプローチとして、Perception・Localization・Planning・Controlという4モジュール構成の「モジュラー型」と、単一ニューラルネットワークで操舵・加速を予測する「End-to-End学習」の2系統が存在する。しかしどちらも完全自律走行を実現できておらず、LLMが第三の解になり得るとの仮説を提示する。LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-Decoder構造を持つTransformerアーキテクチャ、次単語予測（Next-Word Prediction）を説明する。自動運転への応用では、画像・LiDAR点群・RADARデータをVision Transformerでトークン化し、同じTransformerバックボーンで処理できる点を強調する。具体的な研究として、Perceptionでは GPT-4 Visionによる物体記述、HiLM-D・MTD-GPTによる動画対応検出、PromptTrack（DETRとLLMを組み合わせた固有IDの付与）を紹介する。Planningでは、DriveVLM・DriveLLM・DriveLikeHumanなどのモデルが鳥瞰図や過去トラジェクトリを入力として「車線変更」「停止」などの高レベル判断を出力する事例を挙げる。また、自然言語でシナリオを指定してDiffusionモデルで合成トレーニングデータを生成するGeneration活用も示される。Q&A用途では、LLMをチャットインターフェースとして機能させ、走行シナリオの質問に答えるデモも紹介されている。一方で課題も明示されており、LLMの推論速度（リアルタイム要件）、ハルシネーション（幻覚生成）、解釈可能性の欠如、学習・推論コストが自動運転への本格適用を阻む技術的ハードルとして挙げられている。結論として、LLMは自動運転の「すべての解」にはならないが、モジュラーアーキテクチャの特定コンポーネント（特にPlanning・Q&A）を補完・強化する有望な要素技術として位置づけられている。監査エージェント開発への示唆として、複数モジュールを単一LLMに統合するアプローチと、各モジュールを専門化して組み合わせるアーキテクチャ選択のトレードオフは、LangGraphによる監査エージェント設計にも直接応用できる。

## アイデア

- LiDAR・RADAR点群もVision Transformerでトークン化できるため、テキスト・画像・センサーデータを統一バックボーンで処理する汎用アーキテクチャが成立する点
- PromptTrackのようにDETRとLLMを組み合わせて物体に固有IDを付与するアプローチは、監査エージェントにおけるエンティティ追跡（取引ID・証跡管理）に転用できる発想
- DiffusionモデルとLLMを組み合わせてレアケース（悪天候・事故シーン）のトレーニングデータを自然言語指定で生成する手法は、監査シナリオのシンセティックデータ生成にも応用可能

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **Diffusionモデル** → /deep_3423 LLMs+：今AIで重要な10のこと

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
