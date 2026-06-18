---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-18
tags: [LLM, 自動運転, Vision Transformer, Perception, End-to-End学習, マルチモーダル, Planning, PromptTrack, GPT-4 Vision]
category: "ai-ml"
related: [4441, 3582, 4900, 7556, 1527]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-18T21:10:59.641383"
---

## 要約

自動運転の歴史的アプローチとして、Perception・Localization・Planning・Controlの4モジュールに分割する「モジュラー型」と、単一ニューラルネットワークで入出力を直結する「End-to-End学習」が主流だった。本記事はこれらに加えてLLM（大規模言語モデル）が第三の解法になりうるかを検討する。

LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-Decoder構造のTransformerアーキテクチャ（Multi-head Attention, Layer Normalization等）、次単語予測タスクによる出力生成を解説する。自動運転への適用では、入力をカメラ画像・LiDAR点群・RADAR点群などに置き換え、Vision TransformerやVideo Vision Transformerで tokenize することで、同一のTransformerモデルをそのまま流用できる。

自動運転における主要な LLM 適用領域は4つ。①Perception（知覚）：GPT-4 Visionが画像から物体・車線を検出。HiLM-D・MTD-GPTは動画対応。PromptTrackはDETR物体検出器とLLMを組み合わせ、各物体にID（例：前方車両ID#3）を割り当て、4D Perceptionを実現。②Planning（計画）：画像やBEV（鳥瞰図）を入力に「車線変更すべきか」などの行動判断を出力。③Generation（生成）：Diffusionモデルを活用した訓練データ・代替シナリオの自動生成。④Question & Answering：シナリオに基づいてLLMにチャット形式で質問可能なインターフェース。

技術的特徴として、マルチモーダル入力（画像・センサー・アルゴリズム出力を統合）・Few-shot Learning・Pretrain/Fine-tuningパラダイムが自動運転に適用可能である点が強調されている。一方、End-to-End学習と同様のブラックボックス問題、リアルタイム推論コスト、センサーフュージョンの複雑さなどが課題として残る。

監査エージェント開発への示唆：LLMを用いた「状況説明→行動判断」のパイプラインは、監査シナリオにおける証憑読解→リスク判定フローと構造的に類似する。特にPromptTrackのように外部検出器の出力をLLMに渡してIDベースで追跡する設計は、ReActエージェントで複数の監査ツール出力を統合する際の参考アーキテクチャになりうる。

## アイデア

- PromptTrackがDETRとLLMを組み合わせて物体IDを付与する設計は、外部ツールの出力をLLMに渡すReActエージェントパターンと同型であり、監査エージェントでの証憑追跡に転用できる
- 自動運転の4モジュール（Perception→Localization→Planning→Control）をLLMで統合するEnd-to-End的アプローチは、監査ワークフロー（情報収集→リスク評価→判断→報告）のエージェント設計にそのまま対応する
- Diffusionモデルによる訓練データ・代替シナリオの自動生成は、監査エージェントの評価用合成データ（異常取引シナリオ等）生成にも応用可能

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ
- **Diffusionモデル** → /deep_3423 LLMs+：今AIで重要な10のこと

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_7556 マニュアル動画生成AI「MANAVO」開発ログ①：プロダクト構想と課題の背景
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
