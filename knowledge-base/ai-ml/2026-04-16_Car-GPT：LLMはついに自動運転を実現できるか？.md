---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-16
tags: [LLM, 自動運転, Vision Transformer, Perception, Planning, エンドツーエンド学習, PromptTrack, MagicDrive, DriveLLM]
category: "ai-ml"
related: [716, 1266, 1760, 1449, 1969]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-16T12:37:57.845167"
---

## 要約

自動運転の開発アプローチは大きく「モジュール型」と「エンドツーエンド学習」に分けられてきた。モジュール型は知覚（Perception）・位置推定（Localization）・計画（Planning）・制御（Control）の4段階に分離して設計するが、各モジュール間の誤差伝播が課題。エンドツーエンドは単一ニューラルネットワークがステアリングや加速度を直接予測するが、ブラックボックス問題が残る。本記事はこの文脈で「LLMが自動運転の予想外の答えになり得るか」を検討する。LLMの基本構造として、テキストをトークン（数値）に変換するTokenizationと、Encoder-Decoder構造のTransformerによる次単語予測が説明される。自動運転への応用では、入力を画像・LiDARポイントクラウド・RADARデータ等に置き換え、Vision Transformer（ViT）や Video Vision Transformerでトークン化する。出力は車線変更などの行動コマンドや環境記述に変えることで、同一のTransformerアーキテクチャをそのまま活用できる。研究が活発な応用領域は4つ：①Perception（GPT-4 Visionによる物体検出、HiLM-D・MTD-GPT等のモデルが画像・動画から物体リストを生成、PromptTrackはDETR検出器とLLMを組み合わせて一意IDを付与）、②Planning（UniAD、NuScenesデータセットを用いたBEV＋LLMによる行動生成、Think2Driveでは強化学習とLLMを統合）、③Generation（DiffusionモデルによるCornercaseや希少シナリオの訓練データ生成、MagicDriveなど）、④Q&A（DriveLLMやDriveVLMがシナリオに対してチャット形式で回答）。課題として、自動運転の入力データはLLMが元来学習してきたテキストと大きく異なるため、ドメイン適応が必要であり、リアルタイム推論のレイテンシ・計算コスト・安全保証も依然未解決である。LLM単独の完全自動運転の実用化には至っていないが、特定サブタスクでの活用とモジュール型システムへの統合が現実的な方向性として示されている。監査エージェント開発への示唆としては、LLMをサブタスク単位（知覚・判断・生成）に分割して統合するアーキテクチャは、監査フローの各工程（データ収集・リスク評価・報告生成）への分割適用と類似しており、ReActやLangGraphによるエージェント設計の参考になる。

## アイデア

- LLMのTransformerアーキテクチャはトークン列を入力とするため、画像・LiDAR・RADARもViTでトークン化すれば同一モデルで処理可能という汎用性の高さ
- Diffusionモデルによるコーナーケース生成（MagicDrive等）で希少シナリオの訓練データを補完するアプローチは、データ不足が課題の専門ドメイン全般に応用できる
- PromptTrackがDETR（既存の専門モデル）とLLMを組み合わせて一意ID付与を実現した手法は、既存ツールとLLMをハイブリッド統合する設計パターンの好例

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ
- **Diffusionモデル** → /deep_1306 Intel CPU上でのStable Diffusionモデルのファインチューニング

## 関連記事

- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_1969 階層的SVGトークン化：スケーラブルなベクターグラフィックスモデリングのためのコンパクトな視覚プログラム学習

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
