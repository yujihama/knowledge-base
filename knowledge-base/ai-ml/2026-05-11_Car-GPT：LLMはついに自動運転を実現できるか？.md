---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-11
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, DriveVLM, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-11T09:55:16.347888"
---

## 要約

自動運転の開発アプローチは2010年代の「モジュール型」（Perception→Localization→Planning→Control の分離）から、単一ニューラルネットワークで操舵・加速を直接予測する「End-to-End学習」へと移行しつつあるが、どちらも完全な自動運転を実現していない。本記事はその第三の解として LLM（大規模言語モデル）の活用可能性を探る。LLMの基礎としてTokenization（テキスト→数値変換）、Transformer（Encoder-Decoder構造、Multi-head Attention）、Next-word Prediction を解説した上で、自動運転への応用として4つの研究領域を整理している。①Perception（HiLM-D、MTD-GPT、PromptTrack等でオブジェクト検出・追跡をLLMで実施）、②Planning（DriveVLM、GPT-Driver等がBird-Eye-View画像から車線変更・停止等の行動を自然言語で推論）、③Generation（DriveDreamer等のDiffusionモデルで希少シナリオの訓練データを合成）、④Q&A（DriveLMのようなチャットインターフェースで状況説明を対話的に取得）。Vision Transformer（ViT）が画像をパッチ単位でトークン化することで、LiDAR点群・RADAR・カメラ映像などマルチモーダル入力を統一的に扱える点が鍵となる。課題としては、LLMの推論レイテンシが実車でのリアルタイム制御要件（数十ms以下）に対して依然として高すぎること、説明可能性の向上と同時にブラックボックス性が残ること、センサー融合・キャリブレーション精度への依存が挙げられる。記事はWaymo・Tesla等の既存プレイヤーがEnd-to-End学習に注力している背景を示しつつ、LLMが「ペニシリンのような偶発的ブレークスルー」になり得るかを問いかける入門的解説記事である。監査エージェント開発への示唆としては、ReActパターンと同様に「観察→推論→行動」をLLMに統合するアーキテクチャが自動運転でも試みられており、マルチモーダル入力を単一モデルで処理する設計思想は監査エージェントにおける非構造化エビデンス（PDF・スキャン帳票）のトークン化戦略に応用できる。

## アイデア

- 画像・LiDAR・RADARをViTでパッチトークン化することで、テキスト向けTransformerをほぼそのまま自動運転のマルチモーダル入力に転用できる点は、監査エージェントの非構造化ドキュメント処理にも応用可能な設計パターン
- GPT-Driver等がPlanning結果を自然言語で出力することで、従来のブラックボックスなEnd-to-End学習に説明可能性を付与しようとしている点は、LLM-as-judgeによる意思決定根拠の文書化と同じ発想
- DriveDreamerのようなDiffusionベースのシナリオ生成で希少・危険ケースの訓練データを合成するアプローチは、監査における低頻度不正パターンの合成データ拡張にそのまま転用できる

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Transformer / Attention** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Diffusionモデル** → /deep_3423 LLMs+：今AIで重要な10のこと
- **Bird-Eye-View表現** (TODO: 読むべき)

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
