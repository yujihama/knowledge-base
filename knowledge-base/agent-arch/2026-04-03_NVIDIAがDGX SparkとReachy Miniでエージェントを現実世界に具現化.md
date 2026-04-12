---
title: "NVIDIAがDGX SparkとReachy Miniでエージェントを現実世界に具現化"
url: "https://huggingface.co/blog/nvidia-reachy-mini"
date: 2026-04-03
tags: [NeMo Agent Toolkit, ReAct, マルチモーダル, ロボティクス, NVIDIA Nemotron, VLM, ルーティング, ツール呼び出し, DGX Spark]
category: "agent-arch"
memo: "[HF Blog] NVIDIA brings agents to life with DGX Spark and Reachy Mini"
processed_at: "2026-04-03T09:10:11.585043"
---

## 要約

CES 2026にてNVIDIAがDGX SparkとオープンソースロボットReachy Miniを組み合わせ、デスク上で動作するパーソナルAIエージェントのデモを公開した。構成要素は推論モデル（NVIDIA Nemotron 3 Nano、約65GB）、ビジョンモデル（NVIDIA Nemotron Nano 2 VL、約28GB）、音声合成（ElevenLabs）、ロボット本体（Reachy Mini）の4つ。オーケストレーションにはNVIDIAのNeMo Agent Toolkitを使用し、LangChain・LangGraphとも連携可能な軽量フレームワークとして機能する。エージェントの構成はReActパターンを採用し、テキスト質問・ビジュアル質問・ツール呼び出しを必要とするアクション要求の3種類にルーティングする設計となっている。テキスト系はNemotron 3 Nanoで処理、カメラ映像を伴う質問はVLM（Nemotron Nano 2 VL）に転送、リアルタイム情報が必要な場合はReActエージェントがWikipedia検索等のツールを呼び出す。Reachy Miniはカメラ・スピーカー・サーボモーターを備え、PythonのAPIから直接制御可能。エージェントが応答する際には発話と連動してロボットの動作（首振り・表情等）が生成される。モデルのデプロイ方式はローカル（DGX Spark等）、クラウドGPU（NVIDIA Brev・HuggingFace Inference Endpoints）、サーバーレスエンドポイント（build.nvidia.com）の3形態をサポートし、APIキー設定のみで切り替え可能。NeMo Agent Toolkitはトークン使用量・レイテンシのプロファイリングとハイパーパラメータの自動チューニング機能を内蔵し、コスト最適化の観点でも実用的な設計となっている。ソースコードはbrevdev/reachy-personal-assistantとして公開されており、uv環境で再現可能。本デモはクローズドなパーソナルアシスタントとは異なり、モデル・プロンプト・ツール・ロボット動作のすべてをユーザーが制御できる完全オープンな構成である点が特徴。

## アイデア

- テキスト・ビジョン・ツール呼び出しの3経路ルーティングをNeMo Agent Toolkitで実装しており、意図分類なしにheuristics/軽量分類器でルーティングする実装パターンが参考になる
- 物理アクション前に「confirm before actuation」パターンを推奨しており、エージェントが外部システムに副作用を与える前の承認ステップの設計思想として応用可能
- NeMo Agent Toolkitがトークン使用量・レイテンシのプロファイリングと自動ハイパーパラメータチューニングを内蔵している点は、本番運用コスト管理の観点で実装時に検討価値がある

## Yujiの取り組みへの示唆

ReActパターンによるツール呼び出しとマルチモーダルルーティングの実装がLangGraph上の監査エージェント設計に直接応用できる。特に「テキスト質問・視覚情報を含む質問・外部ツール呼び出しを要する質問」の3経路ルーティングは、監査証跡の種別（テキストログ・画像証跡・外部DB照会）に対応したエージェント設計と構造的に類似している。NeMo Agent ToolkitはLangGraphとの互換性があるため、既存の開発スタックを維持しながら部分的に導入してプロファイリング機能を活用することも検討に値する。

## 原文リンク

[NVIDIAがDGX SparkとReachy Miniでエージェントを現実世界に具現化](https://huggingface.co/blog/nvidia-reachy-mini)
