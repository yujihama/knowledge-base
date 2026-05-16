---
title: "Car-GPT: LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-23
tags: [自動運転, LLM, Vision Transformer, End-to-End学習, Perception, Planning, DriveGPT4, UniSim, マルチモーダル]
category: "ai-ml"
related: [1527, 1297, 182, 1817, 17]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-23T12:46:24.847269"
---

## 要約

自動運転の歴史は「モジュール型アプローチ」から始まった。知覚（Perception）・位置推定（Localization）・計画（Planning）・制御（Control）という4つのモジュールを独立して開発し、パイプラインとして接続する手法だ。2010年代にはEnd-to-End学習（単一ニューラルネットで操舵・加速を予測）も登場したが、ブラックボックス問題が残る。本記事は、LLMをこれら4つの柱に適用できるかを検討したサーベイ的解説記事である。

LLMの基本構造として、テキストをトークン（数値列）に変換するTokenization、TransformerのEncoder-Decoder構造、next-word predictionによる出力生成が説明される。自動運転への適用では、入力を画像・LiDARポイントクラウド・RADARデータなどに置き換え、出力をレーンチェンジなどの運転タスクに対応させることが核心となる。

Perceptionタスクでは、GPT-4 VisionやHiLM-D、MTD-GPTが物体検出・追跡（PromptTrackはDETRとLLMを組み合わせてオブジェクトにID付与）に活用される。Planningタスクでは、DriveGPT4やDriveVLMがシーン理解から走行判断を生成し、LLM Driverはゼロショットで運転方針を推論する。Generationタスクでは、UniSim（NVIDIA）やDriveDreamerがReal World Modelとして機能し、稀少シナリオの訓練データを拡散モデルで生成する。QAタスクでは、NuScenesデータセットを活用したDriveMLMやEM-VLMがマルチモーダルな質問応答を実現する。

LLMを自動運転に用いる最大の課題はリアルタイム性である。LiDARや複数カメラからの大量トークンを処理しながら安全制御レベル（ISO 26262）の応答速度を達成するには、推論効率の大幅な改善が必要だ。また、LLMの判断が自然言語的な「説明」に留まるのか、実際の制御コマンドに直結できるのかという問題も未解決である。記事は楽観的に、LLMが自動運転の「ペニシリン的発見」になりうると結論付けているが、その実現には知覚精度・推論速度・安全性の三点において従来のシステムとの統合設計が不可欠と指摘する。監査エージェント開発への示唆としては、複数モジュールをLLMで統合するEnd-to-End的アーキテクチャ設計と、自然言語による推論根拠の生成（説明可能性）の組み合わせが参考になる。

## アイデア

- LiDAR・RADAR・カメラなど異種センサーデータをすべて「トークン化」して単一Transformerに入力するアーキテクチャは、監査エージェントが財務データ・テキスト・ログなど異種情報を統一的に処理する設計に直接応用できる
- NVIDIAのUniSimのように、稀少シナリオ（コーナーケース）を拡散モデルで生成して訓練データに加える手法は、内部監査でも不正・異常の合成データ生成による教師データ拡充に転用可能
- DriveGPT4やLLM Driverが示す「ゼロショット・少数ショットでの運転判断」は、ルール未整備領域での監査判断をLLMで補完するアプローチと構造的に同じであり、説明可能AIとしての活用可能性を示唆する

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_182 AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ
- /deep_1817 AIが中小セラーの商品開発を変える：AlibabaのAccioが示すAIソーシング・エージェントの実態
- /deep_17 AI vs. アンチボット：LLMが書き換えるウェブスクレイピングの全ルール

## 原文リンク

[Car-GPT: LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
