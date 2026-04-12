---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-04
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, DriveGPT4, GPT-Driver, PromptTrack, マルチモーダル]
category: "ai-ml"
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
related: [1527, 1297, 182, 17, 217]
processed_at: "2026-04-04T21:08:42.749987"
---

## 要約

本記事はThe Gradientが2024年3月に公開した解説記事で、LLM（大規模言語モデル）が自動運転に応用される可能性を体系的にまとめている。自動運転の従来アプローチとして、Perception・Localization・Planning・Controlの4モジュールに分割するモジュラー型と、単一ニューラルネットワークで入力から出力を直接予測するEnd-to-End学習の2つを対比した上で、LLMがどのモジュールに貢献できるかを分析している。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、エンコーダ・デコーダ構造のTransformerアーキテクチャ、次単語予測タスクを解説。自動運転への適用では、入力を画像・LiDARポイントクラウド・RADARデータ等に拡張し、Vision Transformerで処理する構成が中心となる。

LLMが活発に研究されているタスクは以下の4領域。①Perception：GPT-4 Visionやモデル「HiLM-D」「MTD-GPT」が画像から物体・車線を検出。「PromptTrack」はDETRオブジェクト検出器とLLMを組み合わせ、物体にユニークIDを付与するトラッキングも実現。②Planning：「DriveGPT4」は視覚入力とユーザー質問を受け取り、運転行動の説明と次のコントロールシグナルを出力する。「GPT-Driver」はGPT-3.5を使用し、動作プランナーを言語推論問題として定式化。③生成タスク：拡散モデルを用いた訓練データ生成や代替シナリオ生成。④Q&A：シナリオに基づく自然言語対話インターフェース。

技術的な課題としては、LLMの推論速度（高レイテンシ）がリアルタイム制御に不向きである点、Planningからの出力をControlモジュールに接続する際のインターフェース設計、ブラックボックス問題による説明可能性の欠如が挙げられている。記事は「LLMは自動運転の一部を担えるが、完全な置き換えには至っていない」という立場で結論づけている。

## アイデア

- LLMをPlanningモジュールに適用する際、GPT-Driverのように軌道予測を『言語推論問題』として定式化する手法は、構造化されたルールベースの判断をLLMに委譲するアーキテクチャパターンとして汎用性が高い
- Vision TransformerとLLMを組み合わせたPromptTrackの構成は、マルチモーダル入力を統一トークン空間で処理するアーキテクチャの具体例であり、センサーフュージョンへの応用可能性を示す
- 自動運転の4モジュール（Perception/Localization/Planning/Control）をエージェントの認識・判断・実行サイクルと対応づけると、LLMエージェントのアーキテクチャ設計の参考フレームとして読める
## 関連記事

- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_182 AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ
- /deep_17 AI vs. アンチボット：LLMが書き換えるウェブスクレイピングの全ルール
- /deep_217 AGIはマルチモーダルでは実現しない——身体性と世界モデルの欠如が根本的障壁

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
