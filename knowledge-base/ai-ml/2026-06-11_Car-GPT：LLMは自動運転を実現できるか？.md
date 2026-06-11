---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-11
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, DriveGPT4, PromptTrack, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 7556, 1527]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-11T21:19:41.792068"
---

## 要約

本記事は、2024年3月にThe Gradientが公開した自動運転とLLMの統合に関する解説記事である。自動運転の従来アーキテクチャは「モジュール型」（Perception→Localization→Planning→Control）と「End-to-End学習」の2系統が主流だったが、いずれも完全な自動運転を実現するには至っていない。そこで筆者は、LLMが「予期せぬ解」となり得るかを検討する。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造のTransformerアーキテクチャ、そしてNext-Word Predictionによる出力生成の3点を解説する。自動運転への適用においては、入力を画像・LiDARポイントクラウド・RADARデータ等に拡張し、Vision TransformerやVideo Vision Transformerを通じてトークン化する。出力は車線変更などの直接的な運転タスクや自然言語説明に設定できる。

2023年時点でLLMが活用されている主要タスクは4つ。①Perception（認識）：GPT-4 VisionやHiLM-D、MTD-GPTがカメラ映像から物体・車線を検出し、PromptTrackはDETR検出器とLLMを組み合わせて物体IDの追跡も実現する。②Planning（計画）：DriveGPT4やDriveLLMなどが鳥瞰図や知覚出力を元に「直進」「停車」「譲る」といった行動判断を出力する。③Generation（生成）：Diffusionモデルを用いて訓練データや代替シナリオを生成し、データ不足問題に対処する。④QA（質疑応答）：MAPLM、DriveLMなどがシナリオ画像に対して自然言語で質問に答えるチャットインターフェースを実現する。

LLMを自動運転に統合する際の主な課題は、(1)リアルタイム推論の計算コスト（LLMは重い）、(2)安全性の担保（ハルシネーションが命に関わる）、(3)センサーデータのトークン化効率の3点である。現実的な活用方針として、LLMを全モジュールの代替とするのではなく、既存パイプラインの特定箇所（例：Planning層のみ）に組み込むハイブリッドアプローチが有望とされる。監査エージェント開発への示唆としては、複数の異種センサー入力を統一的にトークン化してTransformerで処理するアーキテクチャは、監査における複数データソース（財務数値・契約書・ログ）の統合処理パターンと構造的に類似しており、入力モダリティの拡張設計の参考となる。

## アイデア

- LiDARポイントクラウドや画像など異種センサーデータをすべてトークン化することでTransformerの汎用アーキテクチャをそのまま流用できる点は、マルチモーダル統合の設計パターンとして広く応用可能
- Planning層にのみLLMを使うハイブリッド構成（既存モジュール+LLM）は、既存システムへの段階的なLLM統合の現実的な指針を示す
- PromptTrackがDETR（既存物体検出器）とLLMを組み合わせた事例は、専門特化モデルとLLMのオーケストレーション設計における役割分担の具体例として参考になる

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Diffusionモデル** → /deep_3423 LLMs+：今AIで重要な10のこと

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_7556 マニュアル動画生成AI「MANAVO」開発ログ①：プロダクト構想と課題の背景
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
