---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-14
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, マルチモーダル, DriveGPT4, PromptTrack, 説明可能AI]
category: "ai-ml"
related: [4441, 3582, 4900, 7556, 4439]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-14T21:12:13.551039"
---

## 要約

本記事は、The Gradientに掲載された2024年3月の解説記事で、LLM（大規模言語モデル）が自動運転の各コンポーネントに応用される研究動向を整理している。

自動運転の従来アーキテクチャは「モジュラー型」で、Perception（物体検知）・Localization（自己位置推定）・Planning（経路計画）・Control（操舵・加速制御）の4モジュールが順次動作する構成だった。2010年代後半からEnd-to-End学習（単一ニューラルネットが入力センサデータから直接操舵・加速を出力）が注目されたが、ブラックボックス問題が残る。LLMはこの文脈での「第三の選択肢」として研究が進んでいる。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造を持つTransformerアーキテクチャ、次単語予測（Next-Word Prediction）を解説。GPT系はDecoder-onlyであり、入力トークン列から出力トークン列を生成する。

自動運転への適用では、入力を画像・LiDAR点群・RADARデータ等に変換（Vision Transformerで対応）し、出力を「車線変更すべき」等の運転行動記述に変更するだけで、Transformerコア自体は流用できる。

研究が活発な適用領域は以下の4つ。①Perception：GPT-4 VisionやHiLM-D、MTD-GPTが画像から物体・車線を記述。PromptTrackはDETR検出器とLLMを組み合わせ、物体にID付き追跡を実現。②Planning：DriveGPT4やDriveLLMが鳥瞰図・画像から「そのまま走行」「譲る」等の行動計画を生成。③データ生成：拡散モデル（Diffusion）を用いてトレーニング用の合成シナリオを生成し、データ不足を補う。④Q&A：LLMにシーンを与えてチャット形式で状況説明・意思決定根拠を返す説明可能AIとして機能。

課題としては、リアルタイム推論速度（自動運転は100ms以下の応答が必要）、センサモダリティの統合（カメラ・LiDAR・RADARの同時処理）、訓練データの安全性担保が挙げられる。監査AI開発への示唆として、LLMが意思決定の根拠をテキストで説明するQ&Aモジュールのアプローチは、監査エージェントの判断説明可能性（Explainability）設計に直接応用できる。複数センサ入力を統合するマルチモーダルTokenizationの手法も、監査における構造化・非構造化データの統合処理設計の参考になる。

## アイデア

- LLMのQ&Aモジュール（シーンを与えて意思決定根拠をテキスト出力）は、監査エージェントの判断説明可能性設計に直接転用できる構造を持つ
- Vision TransformerによるLiDAR/RADAR点群のTokenization手法は、構造化・非構造化の異種データを単一Transformerで処理する汎用パターンとして重要
- 自動運転のEnd-to-Endモデルが抱えるブラックボックス問題に対し、LLMがPlanning段階で自然言語の中間表現を生成することで解釈可能性を付与するアプローチ

## 前提知識

- **Transformer (Encoder-Decoder)** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **拡散モデル (Diffusion)** (TODO: 読むべき)

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_7556 マニュアル動画生成AI「MANAVO」開発ログ①：プロダクト構想と課題の背景
- /deep_4439 Pragmos：プロセスエージェント型モデリングシステム

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
