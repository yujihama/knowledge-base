---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-05
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, マルチモーダル, PromptTrack]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-05T09:11:58.285774"
---

## 要約

本記事はThe Gradientに掲載された解説記事で、LLM（大規模言語モデル）が自動運転の課題を解決できるかを検討している。自動運転の従来アーキテクチャは「モジュラー型」（知覚・自己位置推定・計画・制御の4モジュール構成）と、2010年代後半から台頭した「End-to-End学習」（単一ニューラルネットが操舵・加速を直接予測）の2種類に大別される。どちらも完全自動運転を実現するには至っておらず、LLMがその突破口になり得るかを論じている。LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-Decoder構造を持つTransformerアーキテクチャ、そして次単語予測タスクを説明した上で、自動運転への応用を4つの領域に整理する。①知覚（Perception）：GPT-4 Visionのようなモデルが画像からオブジェクトを検出・記述できる。HiLM-D、MTD-GPT、PromptTrack（DETRとLLMを組み合わせ、ID付きトラッキングが可能）などが研究されている。②計画（Planning）：鳥瞰図や知覚結果を入力に、車線変更・停止などの行動を言語で出力する。③データ生成（Generation）：Diffusionモデルと組み合わせて学習用データや代替シナリオを合成する。④Q&A：シナリオに基づいた対話インターフェースの構築。Vision Transformer（ViT）やVideo Vision Transformerを用いて画像・LiDARなどのセンサーデータをトークン化し、既存のTransformerブロックに入力することで、マルチモーダル対応が可能になる。記事全体としては入門的な解説記事であり、独自の実験結果や定量評価は含まれない。監査エージェント開発への直接的示唆は薄いが、マルチモーダルトークン化・Vision Transformer・End-to-End学習の概念は、文書画像を入力とする監査エージェントの知覚モジュール設計に応用できる視点を提供する。

## アイデア

- LiDARやRADARのポイントクラウドもトークン化できるという発想は、構造化・非構造化データを統一的にTransformerに入力する汎用フレームワークとして、監査ログや財務データの処理にも転用可能
- モジュラー型とEnd-to-Endのハイブリッドとして、LLMが各モジュールの出力を言語化・統合するオーケストレーター役を担うアーキテクチャは、LangGraphのような多段エージェント構成と概念的に近い
- PromptTrackのようにオブジェクトに一意IDを割り当てるトラッキング手法は、監査においてエンティティ（取引・仕訳・勘定科目）の同一性追跡に応用できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
