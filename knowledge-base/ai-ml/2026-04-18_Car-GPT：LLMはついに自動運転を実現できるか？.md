---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-18
tags: [LLM, 自動運転, Vision Transformer, Perception, Planning, End-to-End学習, DriveGPT4, NeRF, マルチモーダル]
category: "ai-ml"
related: [1343, 1527, 1297, 182, 1817]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-18T12:33:02.208704"
---

## 要約

本記事は、自動運転へのLLM応用可能性を解説した入門的サーベイ記事である。自動運転の従来アーキテクチャは「モジュール型」と「End-to-End学習」の2系統に大別される。モジュール型はPerception（物体検知・環境認識）、Localization（自己位置推定）、Planning（軌道生成）、Control（操舵・加速指令）の4モジュールで構成され、各モジュールが独立した専門モデルを持つ。End-to-Endは単一ニューラルネットワークで入力から制御出力まで直結するが、ブラックボックス問題が残る。そこにLLMを適用する試みが2023年以降活発化している。LLMの自動運転への適用では、入力をトークン化する点がキーとなる。画像はVision Transformer（ViT）、LiDAR点群・RADAR点群・車線情報なども数値トークンに変換可能であり、Transformerのアーキテクチャ自体はモダリティ非依存で動作する。研究が活発な4領域は①Perception（環境記述、物体検出・追跡）、②Planning（行動決定・軌道生成）、③データ生成（Diffusionによる学習データ・シナリオ生成）、④Q&A（シーンに対する自然言語問答）である。Perceptionでは、GPT-4VがCOCOクラスの物体検出をテキスト出力として実現し、HiLM-D・MTD-GPT・PromptTrackがビデオ対応・ID付きトラッキングを実現している。Planningでは、DriveGPT4・GPT-Driver・DiMA等が鳥瞰図または前方カメラ画像を入力として「直進」「車線変更」等の行動を生成し、説明可能性（XAI）も同時に提供する。SurrealDriverは自然言語でドライバーエージェントをシミュレートする。データ生成分野ではChatSimがNeRFと組み合わせて自動運転シミュレーション環境を生成する。Q&A分野ではDriveVLMやDriveLMがシーン理解と行動根拠の言語説明を統合している。著者は「LLMが自動運転を完全解決するには至らないが、常識推論・説明可能性・エッジケース対応において既存手法を補完する可能性がある」と結論づけている。監査エージェント開発への示唆としては、センサーデータ等の非テキスト入力をトークン化してTransformerに投入するアーキテクチャパターンは、会計データ・ログデータの異常検知にも転用可能であり、Q&A型の説明生成（なぜその判断をしたか）は監査エージェントの根拠説明モジュールに直接応用できる。

## アイデア

- 画像・LiDAR・RADARなど異種センサーデータをすべて「トークン」に変換することで、モダリティ非依存なTransformerバックボーンを共有できる設計思想は、監査における多種データ統合にも応用可能
- PlanningモジュールにLLMを使うことで、行動決定と同時に自然言語による根拠説明（XAI）を無コストで生成できる点は、説明可能性が求められる監査・コンプライアンス判断と親和性が高い
- ChatSimのようにNeRF＋LLMでシミュレーション環境を自動生成するアプローチは、希少事例（不正会計パターン等）の学習データ拡張にも転用できる可能性がある

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **トークン化・埋め込み表現** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **LiDAR点群処理** (TODO: 読むべき)

## 関連記事

- /deep_1343 マルチトラバーサル再構成のための外観分解ガウシアンスプラッティング（ADM-GS）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_182 AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ
- /deep_1817 AIが中小セラーの商品開発を変える：AlibabaのAccioが示すAIソーシング・エージェントの実態

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
