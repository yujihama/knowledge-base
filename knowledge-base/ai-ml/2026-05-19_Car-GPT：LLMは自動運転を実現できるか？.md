---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-19
tags: [自動運転, LLM, Vision Transformer, End-to-End学習, Perception, Planning, GPT-4V, Diffusion, 説明可能AI]
category: "ai-ml"
related: [4439, 1346, 4015, 5220, 1266]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-19T09:27:41.662801"
---

## 要約

本記事は、2024年時点での自動運転へのLLM適用可能性をサーベイ的に解説したもの。自動運転の技術的枠組みとして、Perception（環境認識）・Localization（自己位置推定）・Planning（経路計画）・Control（操舵・加速指令生成）の4モジュール構成が従来アプローチであり、2010年代はこのモジュール型設計が主流だった。対してEnd-to-End学習は全モジュールを単一ニューラルネットで置換するが、ブラックボックス問題が残る。LLMはこの両者とは異なる第三の候補として注目されている。LLMの基礎としてTokenization（テキストを数値トークン列に変換）、Transformerアーキテクチャ（エンコーダ・デコーダ構造、Multi-Head Attention）、Next-Word Predictionの3要素を解説。自動運転への適用では、画像・LiDAR点群・RADAR点群・レーン検出結果などをVision Transformer（ViT）やVideo Vision Transformerを通じてトークン化し、同一のTransformerバックボーンに入力する形で処理する。研究が活発な4領域として：(1) Perception：GPT-4VやHiLM-D、MTD-GPT、PromptTrackが物体検出・予測・追跡を実施。PromptTrackはDETR検出器とLLMを組み合わせ、物体に一意IDを付与する。(2) Planning：DriveVLM、DriveWithLLM、GPT-Driver等がシーン記述から行動決定を生成。(3) Generation：Diffusionモデルと組み合わせたデータ拡張・シナリオ生成（WoVogen等）により学習データのロングテール問題を緩和。(4) Q&A：DriveLM等がシーン理解に基づく対話インターフェースを提供。LLMの自動運転への強みとして、常識推論（工事現場でのコーン認識等）、説明可能性（意思決定の言語化）、Few-shot汎化が挙げられる。一方、推論速度（リアルタイム要件に対するレイテンシ）、センサーデータのトークン化コスト、安全保証の困難さが課題として残る。監査AI文脈では、意思決定の言語的説明生成はAIの説明可能性・監査証跡確保の観点と直結し、LLMベースのPlanning層が「なぜその判断をしたか」をテキスト出力できる点は内部監査ロジックへの応用示唆がある。

## アイデア

- LiDAR・RADAR点群やレーン検出アルゴリズム出力をトークン化することで、異種センサーデータを統一的なTransformerバックボーンに入力できる設計は、マルチモーダルエージェントの入力設計として汎用性が高い
- Planning層でLLMが意思決定を自然言語で出力する仕組みは、監査エージェントにおける「証跡の自動生成」と構造的に同一であり、ReActパターンの思考ステップ可視化に直接応用できる
- DiffusionモデルとLLMを組み合わせたシナリオ生成によるロングテール対応は、監査異常検知における低頻度・高リスク事象の合成データ生成戦略として転用可能

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Transformer / Attention** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **LiDAR点群** (TODO: 読むべき)
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開

## 関連記事

- /deep_4439 Pragmos：プロセスエージェント型モデリングシステム
- /deep_1346 LLM述語からLogic Tensor Networkへ：規制調達における神経記号的オファー検証
- /deep_4015 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
