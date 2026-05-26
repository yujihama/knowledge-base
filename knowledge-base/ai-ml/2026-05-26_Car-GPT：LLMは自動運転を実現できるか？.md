---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-26
tags: [LLM, 自動運転, Vision Transformer, Perception, Planning, エンドツーエンド学習, GPT-4 Vision, PromptTrack, DriveLM]
category: "ai-ml"
related: [716, 5220, 1266, 1760, 1449]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-26T09:26:19.428209"
---

## 要約

本記事はThe Gradientに掲載された解説記事で、LLM（大規模言語モデル）を自動運転に応用する研究動向を体系的にまとめている。自動運転の従来アプローチは「モジュラー型」（Perception・Localization・Planning・Controlを個別モジュールで処理）と「エンドツーエンド学習」（単一ニューラルネットワークで操舵・加速を予測）の2系統だが、どちらも完全自動運転を実現できていない。そこにLLMを第三の選択肢として位置づけている。

LLMの基礎として、テキストを数値トークンに変換するトークナイゼーション、Encoder-Decoderアーキテクチャを持つTransformer（マルチヘッドアテンション、層正規化等で構成）、次単語予測タスクの3要素を解説。自動運転への転用では、入力を画像・LiDARポイントクラウド・RADARデータ等に変更し、Vision TransformerやVideo Vision Transformerで視覚トークン化することで同じTransformerバックボーンを流用できる。

2023年時点でLLMが活用されている自動運転タスクとして4領域を挙げる。①Perception：GPT-4 VisionやHiLM-D、MTD-GPTが画像から物体・車線を検出・記述。PromptTrackはDETR物体検出器とLLMを組み合わせてオブジェクトへのユニークID割り当て（4D Perception相当）を実現。②Planning：DriveLM、DriveVLMなどがBird-Eye-View画像や知覚出力を受け取り「車線変更すべきか」等の判断を出力。GPT-Driverは推論チェーンを活用して人間的な運転判断を模倣。③Data Generation：拡散モデルと組み合わせて学習用の合成シナリオや代替シーンを生成。④Q&A／チャットインターフェース：シナリオに基づいてドライバーや研究者が対話的に質問できる仕組み。

LLMを自動運転に適用する上での技術的課題として、リアルタイム処理の遅延（GPT-4の推論速度はセンサーフュージョン処理に比べて桁違いに遅い）、センサーデータ（LiDARの3Dポイントクラウド等）のトークン化コスト、エッジデバイス上での計算リソース制約を指摘している。記事全体を通じて、LLMは自動運転の「すべてを置き換える」解ではなく、Planningや知識推論など特定の高次タスクで既存パイプラインを補強するコンポーネントとして最も有望と結論付けている。監査エージェント開発への示唆として、複数の専門モジュールをLLMで統合するアーキテクチャ設計（Planningレイヤーへの言語モデル組み込み）は、ReActやLangGraphベースの監査推論エージェントでも同様の分業パターンが有効であることを示している。

## アイデア

- LLMの「次トークン予測」機構をそのまま自動運転のPlanning出力（操舵・加速コマンド）に転用できる点：テキストトークンを運転行動トークンに置換するだけでアーキテクチャを再利用可能
- PromptTrackのようにDETR等の既存物体検出器をEncoder側に置き、LLMをDecoder側でID管理・追跡に使う「検出器+LLMハイブリッド」構成は、監査エージェントでの証跡抽出＋推論分離設計に応用可能
- Data Generationへの拡散モデル活用：稀少な危険シナリオの合成データ生成は、監査でも異常取引パターンの訓練データ不足問題を解決する手法として参考になる

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **LiDAR点群処理** (TODO: 読むべき)
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
