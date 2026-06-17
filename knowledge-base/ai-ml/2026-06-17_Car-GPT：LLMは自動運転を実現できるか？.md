---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-17
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, GPT-4V, Perception, Planning, DriveGPT4, GPT-Driver, PromptTrack]
category: "ai-ml"
related: [5220, 1266, 1760, 1449, 7835]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-17T21:23:00.233838"
---

## 要約

自動運転の歴史的アプローチは「モジュラー型」（Perception・Localization・Planning・Controlの4モジュール）と「End-to-End学習」（単一ニューラルネットが操舵・加速を直接予測）の2系統に大別される。後者はブラックボックス問題を抱えており、どちらも自動運転を完全に解決していない。この文脈で、LLMを自動運転に適用する「Car-GPT」的アプローチへの関心が高まっている。

技術的基盤として記事はLLMの3要素を説明する。①トークン化（テキスト→数値変換）、②Transformerアーキテクチャ（Encoder-Decoder構造、Multi-Head Attention）、③次単語予測タスク。自動運転への適用時は入力を画像・LiDARポイントクラウド・RADARデータに変換し（Vision Transformerが担当）、出力を車線変更等の運転命令に変える。

研究が活発な4領域として以下が挙げられる。(1) Perception：GPT-4 Visionが画像から物体を検出・記述。HiLM-D、MTD-GPT、PromptTrack（DETRとLLMを組み合わせ固有IDを付与）が代表例。(2) Planning：DriveGPT4、GPT-Driver（GPT-3.5ベース、nuScenesデータセットで評価）がシーン理解と行動計画を実行。(3) データ生成：拡散モデルを用いた合成トレーニングデータ・代替シナリオ生成。(4) Q&A：NuScenesQAやリアルタイムチャットインターフェースによる状況説明。

限界も明示されている。LLMの推論速度（GPT-4は最速でも〜100トークン/秒）は自動運転に必要なリアルタイム性（数十ms）を満たさない。またLLMは自然言語から学習しており、センサーデータへの一般化が未検証。さらに解釈可能性・安全性の担保が不十分。

結論として、LLMは自動運転の「補助的なインテリジェンス」として有望であるものの、単独での自動運転実現には至っておらず、モジュラー型またはEnd-to-Endとのハイブリッドが現実的とされている。監査エージェント開発への示唆としては、複数センサーデータを統合して意思決定するLLMのアーキテクチャ（Vision Transformer＋LLM）は、監査における非構造化データ（PDF・画像・ログ）の統合解析に転用可能なパターンである。

## アイデア

- LLMをPerceptionモジュールとして使う際、PromptTrackはDETRとLLMを組み合わせて物体に固有IDを付与する——これは監査トレースで証跡オブジェクトを一意追跡する設計と同型
- GPT-Driverがテキスト形式のウェイポイントをChain-of-Thought推論で生成する手法は、監査エージェントが根拠付き判断を出力するReAct/CoTパターンの直接的な類似例
- 自動運転でのLLM最大の障壁は推論レイテンシ（〜100トークン/秒）——エージェントシステム設計において「リアルタイム判断」が必要なノードにLLMを置くコストを定量的に意識する必要性を示唆

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ
- **Chain-of-Thought推論** (TODO: 読むべき)

## 関連記事

- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_7835 鮮度は精度ではない：RAGに必要なのは最新順ではなく参照資格である

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
