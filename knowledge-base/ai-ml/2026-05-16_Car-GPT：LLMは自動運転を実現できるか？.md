---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-16
tags: [LLM, 自動運転, Vision Transformer, Perception, Motion Planning, エンドツーエンド学習, GPT-4V, DriveDreamer, nuScenes]
category: "ai-ml"
related: [716, 1297, 4055, 1266, 1760]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-16T09:26:23.362460"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する研究動向を、2024年初頭時点での代表的手法を交えて解説する入門的レビューである。

自動運転の従来アプローチは「モジュラー設計」と「エンドツーエンド学習」の2系統に分かれる。モジュラー設計ではPerception・Localization・Planning・Controlの4モジュールを個別に開発・統合するが、モジュール間の誤差累積が課題。エンドツーエンド学習は単一ニューラルネットワークでステアリングと加速度を直接予測するが、ブラックボックス問題を抱える。LLMはこの両者の課題を補完する第三の経路として注目されている。

LLMの自動運転への適用は主に4領域で進む。①Perception（知覚）：GPT-4 VisionやHiLM-D、MTD-GPTが画像入力から物体・車線を記述し、PromptTrackはDETR検出器とLLMを組み合わせて物体にユニークIDを付与する。②Planning（計画）：SurrealDriverはドライバーエージェントと認知モジュールを組み合わせてシーンを解釈し、GPT-Driverは0-shot GPT-4推論でモーション計画を生成する。DriveVLMはVision-Language Modelを活用しnuScenesベンチマークで既存SOTAを上回る成績を達成。③Generation（生成）：DriveDreamerやDrivingDiffusion、MagicDriveがテキストプロンプトから訓練用シナリオを合成し、データ拡張コストを削減する。④Q&A：NuScenesQAやDriveVQAがシーン理解の質問応答タスクを提供し、評価基準として機能する。

エンドツーエンドLLMアーキテクチャとしてはUniADとOpenDriveが台頭しており、複数タスクを単一モデルで統合することで4モジュール間の情報断絶を解消しようとしている。また、Vision Transformer（ViT）とVideo Vision Transformerにより、画像・LiDAR・RADARなどのセンサーデータをトークン化してTransformerに入力する手法が確立されつつある。

課題としては、LLMの推論速度がリアルタイム制御（数十ms要求）に対して依然として遅い点、大量の高品質ラベル付き自動運転データが必要な点、安全性保証の困難さが挙げられる。記事の結論として、LLMは自動運転の全問題を単独で解決するわけではないが、Planningおよびシナリオ生成領域での補完的活用は現実的であり、モジュラー設計とLLMのハイブリッドが近中期の有力な方向性とされる。

## アイデア

- LiDAR・RADAR・画像などのマルチモーダルセンサーデータをトークン化してTransformerに統一入力する手法は、監査エージェントにおける複数データソース（財務データ・ログ・テキスト）の統合入力設計に応用できる
- Planning領域でGPT-4を0-shot利用するGPT-Driverは、事前訓練なしに推論のみで計画生成を行う点が特徴的であり、LLM-as-judgeアーキテクチャにおける判断根拠の生成手法として示唆を持つ
- DriveDreamerによる合成シナリオ生成（テキスト→訓練データ）は、監査AIにおける異常シナリオの合成データ生成（例：不正仕訳パターンの自動生成）に直接転用可能な発想

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **Transformerアーキテクチャ** → /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- **nuScenesデータセット** (TODO: 読むべき)
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開

## 関連記事

- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_4055 ARETE: HSV変換クラウドソース車両フリートデータを用いたアテンションベースのラスタライズ符号化による道路トポロジー推定
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
