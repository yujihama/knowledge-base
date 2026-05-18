---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-18
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, GPT-4 Vision, PromptTrack, DriveVLM, BEV]
category: "ai-ml"
related: [5535, 5220, 1266, 1760, 1449]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-18T09:21:23.596305"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する研究動向を解説したサーベイ記事である。自動運転の従来アプローチは「モジュラー型」（Perception→Localization→Planning→Controlの4段階パイプライン）と「End-to-End学習」（単一ニューラルネットが操舵・加速を直接予測）の2系統に大別されるが、どちらも完全自動運転の実現には至っていない。そこでLLMをこの問題に適用する試みが2023年頃から活発化している。

LLMの自動運転への適用は主に4領域で進む。①Perception（知覚）：GPT-4 VisionやHiLM-D、MTD-GPTが画像から物体・レーン検出を行い、PromptTrackはDETRと組み合わせてオブジェクトトラッキングとユニークID付与を実現。②Planning（計画）：DriveVLM、GPT-Driver、DiMA等がBEV（Bird's Eye View）画像や知覚出力を受け取り「車線変更すべきか」等の行動計画を生成。LLMの常識推論と世界知識をプランニングに活用する点が特徴。③Data Generation（データ生成）：拡散モデルを組み合わせ、合成トレーニングデータや代替シナリオを生成しデータ不足を補う。④QA（質問応答）：シーンに基づく自然言語での問答インターフェースを提供し、解釈可能性を高める。

LLMを自動運転に使う主なメリットは3点。第一に、テキスト・画像・センサーデータ（LiDARやRADAR点群）・アルゴリズム出力（レーン線・物体等）をすべてトークン化してTransformerに入力できる汎用性。第二に、事前学習済みの世界知識と常識推論能力を活用できる点（例：「赤信号では止まる」を学習データなしで理解済み）。第三に、自然言語での説明生成による解釈可能性の向上。

一方、課題も明確である。リアルタイム推論速度（LLMの低速さとオンボード計算リソースの制約）、センサーモダリティ（特にLiDAR/RADAR）との統合の難しさ、ハルシネーションによる安全リスク、そして学習データの質と量の確保が依然として大きな障壁となっている。

監査エージェント開発への示唆としては、自動運転における「モジュラー型 vs End-to-End」の議論は、LLMベースの監査エージェントにおける「ステップ分解型（LangGraph等） vs 統合型」の設計判断と構造的に同型である。また、LLMの常識推論をドメイン固有タスク（監査判断）に組み込む際のトレードオフ（解釈可能性 vs 速度 vs 精度）は直接参照できる知見を含む。

## アイデア

- センサーデータ（LiDAR点群、RADAR等）を含むあらゆる入力をトークン化してTransformerに統一入力できるという発想は、マルチモーダルエージェントの設計原則として汎用性が高い
- LLMの事前学習済み常識推論（赤信号で止まる等）を自動運転プランニングに直接活用するアプローチは、ドメイン固有ルールを明示的にコーディングせずに済む可能性を示す
- ハルシネーションが安全クリティカルな領域（自動運転・監査等）でどう対処されるかという問いは、LLM-as-judgeや検証ループの設計において核心的な課題を示している

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **BEV (Bird's Eye View)** (TODO: 読むべき)
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開

## 関連記事

- /deep_5535 GEM: 変形可能Mambaによるリダールワールドモデル生成
- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
