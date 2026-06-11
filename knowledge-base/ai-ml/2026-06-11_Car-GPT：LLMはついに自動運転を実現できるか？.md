---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-11
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, HiLM-D, DriveVLM, PromptTrack, Diffusion]
category: "ai-ml"
related: [4015, 5220, 1266, 1760, 1449]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-11T12:33:35.868672"
---

## 要約

自動運転の従来アーキテクチャは「モジュール型」で、Perception（環境認識）・Localization（自己位置推定）・Planning（経路計画）・Control（制御命令）の4モジュールに分割されていた。2010年代末からEnd-to-End学習（単一ニューラルネットが操舵・加速を直接出力）が台頭したが、ブラックボックス問題が残る。本記事はLLMをこの問題の「予期せぬ解答」と位置付け、自動運転への適用可能性を検討する。

LLMの基本構造として、テキスト→トークン変換（Tokenization）、Transformer（エンコーダ・デコーダ構造、Multi-Head Attention）、次単語予測（Next-Word Prediction）を解説。自動運転への転用では、入力を画像・LiDARポイントクラウド・RADARデータなどに置き換え、Vision Transformerでトークン化する。出力は「シーン説明」「走行判断（車線変更など）」に変更する。

自動運転でLLMが有効な4領域として、①Perception：HiLM-D、MTD-GPT、PromptTrackなどが物体検出・追跡・ID割当を実行。GPT-4 Visionはシーン記述が可能。②Planning：DriveLikeAHuman、DriveVLMなどが鳥瞰図や認識結果から「直進継続」「停車」等の行動を生成。③Generation：Diffusionモデルによるシミュレーションデータや代替シナリオの自動生成。④Q&A：シナリオに基づく自然言語インタフェース、の4つを挙げる。

課題として、LLMは推論レイテンシが高く、リアルタイム制御（数十ms以下）との整合が難しい。またハルシネーション（誤った出力）は自動運転では致命的となる。現実的な統合戦略は「LLMをPlanning・QAに限定し、低レイヤ制御は従来手法と併用」するハイブリッド構成。

監査エージェント開発への示唆：LLMをアクションの「説明・計画」層に配置し、実行は専用エンジンに委ねるアーキテクチャは、監査エージェントのReActパターン（LLMがreasoning、ツールが実行）と構造的に同一。自動運転でのハルシネーション対策（出力検証・ガードレール）は監査エージェントの判断信頼性確保にも直接応用できる。

## アイデア

- LLMをPlanning層に限定してリアルタイム制御と分離するハイブリッド構成は、監査エージェントでLLMをreasoning専用にしてツール実行と分離するReActパターンと同型であり、アーキテクチャ設計の汎用原則として参照できる
- Vision TransformerによるLiDAR/RADARのトークン化は、テキスト以外のモダリティをLLMパイプラインに統合する標準手法であり、監査ログや構造化データをLLMに入力する際のトークン設計に応用できる
- 自動運転でのハルシネーション対策（出力検証・確率的サンプリング・ガードレール）は、LLM-as-judgeによる監査エージェントの判断品質保証設計に直接転用可能な研究領域

## 前提知識

- **Transformer / Multi-Head Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **LiDARポイントクラウド** (TODO: 読むべき)

## 関連記事

- /deep_4015 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
