---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-15
tags: [自動運転, LLM, Vision Transformer, Planning, Perception, LanguageMPC, DriveVLM, エンドツーエンド学習]
category: "ai-ml"
related: [716, 1266, 1760, 1449, 564]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-15T12:38:44.191515"
---

## 要約

自動運転の従来アプローチは「モジュール型」と「エンドツーエンド学習」の2つに大別される。モジュール型はPerception・Localization・Planning・Controlの4段階に分割し各専用モデルで処理する。エンドツーエンド学習は単一ニューラルネットワークでステアリング・加速度を直接予測するが、ブラックボックス問題が残る。本記事はLLMをこの課題の第三の解として検討する。LLMの基本構造はTokenization（テキストを数値トークン列に変換）とTransformer（Encoder-Decoderアーキテクチャによる次トークン予測）から成る。自動運転への適用では入力を画像・LiDAR点群・RADARデータに変更し、Vision Transformerによるトークン化を経て同一のTransformerブロックで処理する。研究が活発な適用領域は4つ。①Perception：GPT-4 Visionが画像から物体・レーン等を記述。HiLM-D、MTD-GPTが動画対応、PromptTrackがDETRと組み合わせてユニークID付き物体追跡を実現。②Planning：LanguageMPC（自然言語の交通ルール記述をコスト関数に変換してMPCで制御）、SurrealDriverがGPT-4に役割設定して運転挙動を生成。DriveVLMはVLMでチェーンオブソートを生成し軌道計画まで行う。③Data Generation：LLMやDiffusionモデルで訓練データ・代替シナリオを合成し、データ不足問題を緩和。④Question & Answering：NuScenesデータセット上でQA形式の評価を行うNuScenesQAなどが登場。課題も明確である。現在のLLMは推論速度が遅く（数秒単位）、自動運転が要求するリアルタイム性（100ms以下）を満たせない。また自動運転特化の大規模データセットが不足しており、ハルシネーション問題も未解決である。著者はLLMを自動運転の万能解ではなく、特定モジュール（特にPlanningやQ&A）を補強する部分的な解として位置づけており、モジュール型・エンドツーエンド・LLMのハイブリッドアプローチが現実的と結論づけている。監査エージェント開発への示唆として、LLMをブラックボックスな全体制御ではなく特定判断ステップ（例：異常検知後の対処方針生成）に限定投入する設計思想は、信頼性が求められる監査ワークフローにも直接応用可能である。

## アイデア

- LanguageMPCが自然言語の交通ルール（例：『歩行者優先』）を数値コスト関数に自動変換してModel Predictive Controlに渡すアーキテクチャは、LLMの知識を既存制御系へブリッジする汎用パターンとして興味深い
- DriveVLMがVision Language Modelでチェーンオブソートを生成し軌道計画まで一貫処理する点は、Perceptionから意思決定までをシングルモデルで繋ぐ端緒であり、エージェントの観察→推論→行動ループの実装例として参考になる
- LLMのハルシネーション問題が自動運転では安全上致命的になるという指摘は、監査エージェントでも同様であり、LLMの出力を構造化検証レイヤー（Pydantic等）で常にサニタイズする設計の必要性を再認識させる

## 前提知識

- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Model Predictive Control** (TODO: 読むべき)
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **Chain-of-Thought** → /deep_59 EcoThink: 持続可能でアクセスしやすいエージェントのためのグリーン適応的推論フレームワーク

## 関連記事

- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
