---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-19
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, PromptTrack, GPT-4V, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 7556, 1527]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-19T21:33:23.346380"
---

## 要約

本記事は、自動運転へのLLM（大規模言語モデル）適用の可能性と限界を解説する入門的解説記事（2024年3月）。自動運転の従来アプローチとして、Perception・Localization・Planning・Controlの4モジュールから成る「モジュラー型」と、単一ニューラルネットワークで操舵・加速を予測する「End-to-End学習」の2系統が存在する。LLMをこの問題に適用するアイデアの核心は、画像・LiDAR点群・RADARデータをトークン化し、Vision Transformer（ViT）等を通じて既存のTransformerアーキテクチャに入力することにある。自動運転における主なLLM適用領域として、(1) Perception（環境記述・物体検出・追跡）、(2) Planning（次の行動決定）、(3) 学習データ生成（Diffusion活用）、(4) Q&Aインターフェース、の4分野が挙げられる。具体的なモデルとして、GPT-4 Visionによる画像中の物体列挙、HiLM-D・MTD-GPTによる動画対応の知覚、PromptTrack（DETRとLLMの組み合わせによるマルチビューからのID付き追跡）が紹介される。Planning領域ではDriveGPT4、SurrealDriver、LMDrive、DiMA等が言及され、テキスト指示に基づく経路追従や複雑シナリオへの推論適用が試みられている。また、GPT-4を用いてシナリオ生成やデータ拡張を行うGenerationタスクへの応用も進んでいる。課題としては、LLMの推論レイテンシ（リアルタイム制御への不適合）、センサーデータの直接処理の難しさ、ハルシネーションのリスク、解釈可能性の欠如が指摘される。著者はLLMを自動運転の「完全な解答」とは位置づけず、むしろ補助的なコンポーネント（例：Planning補助、シナリオ説明）として最も有望と結論づける。監査エージェント開発への示唆としては、自律システムにおけるモジュール型とEnd-to-End型のトレードオフ（解釈可能性 vs 性能）は監査AIの設計にも直結する。また、LLMをOrchestrator的に使い、専門モジュールを呼び出すアーキテクチャ（LangGraph的発想）が自動運転でも有効視されている点は、ReActベースの監査エージェント設計と同型の課題構造を持つ。

## アイデア

- センサーデータ（LiDAR・RADAR点群）をトークン化してTransformerに入力するアプローチは、監査ログや構造化データをLLMに入力する際の前処理設計と同じ抽象問題を持つ
- PromptTrackのように既存の専門モデル（DETR）とLLMを組み合わせるハイブリッド構造は、LLMをオーケストレーターとして専門ツールを呼び出すエージェントアーキテクチャの典型例
- LLMの推論レイテンシがリアルタイム制御の障壁になるという問題は、監査エージェントでのオンライン判断 vs バッチ分析の設計判断にも類似した制約として現れる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **マルチモーダルLLM** → /deep_6132 SVFSearch: ゲーム縦型ドメインにおける短尺動画フレーム検索のマルチモーダル知識集約型ベンチマーク

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_7556 マニュアル動画生成AI「MANAVO」開発ログ①：プロダクト構想と課題の背景
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
