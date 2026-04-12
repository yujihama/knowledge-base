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
## 関連記事

- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_986 ドキュメント画像向けマルチモーダルTextImageデータ拡張の紹介
- /deep_305 オープンモデルでOCRパイプラインを強化する：VLMベースドキュメントAIの実践ガイド
- /deep_1117 WebSightデータセット：スクリーンショットからHTMLコードへの変換を実現する大規模合成データセット
- /deep_1257 Saliency-R1: 顕著性マップ整合報酬によるVLMの解釈可能性と忠実性の強化

## 原文リンク

[NVIDIAがDGX SparkとReachy Miniでエージェントを現実世界に具現化](https://huggingface.co/blog/nvidia-reachy-mini)
