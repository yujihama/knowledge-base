---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-24
tags: [LLM, 自動運転, End-to-End学習, Vision Transformer, Perception, Planning, HiLM-D, DriveGPT4, PromptTrack, コモンセンス推論]
category: "ai-ml"
related: [1266, 1760, 1449, 2449, 1969]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-24T12:25:00.250150"
---

## 要約

自動運転の伝統的アプローチは「モジュラー方式」で、Perception・Localization・Planning・Controlの4モジュールを独立して設計するものだった。2010年代後半からEnd-to-End学習（単一ニューラルネットがステアリングや加速を直接予測）への移行が進んだが、ブラックボックス問題が残存する。本稿はLLMをこの領域に適用する可能性を、トークン化・Transformer・次単語予測という3つの基礎概念から解説した上で、実際の研究事例を紹介する。

LLMの自動運転への適用において、入力は画像・LiDARポイントクラウド・RADARデータなどをトークン化したもの、出力は環境記述や走行命令となる。主な研究分野は4つ：(1) Perception（HiLM-D、MTD-GPT、PromptTrackなど）、(2) Planning（DriveGPT4、DiMA、Agent Driver、BEV-Plannerなど）、(3) データ生成（拡散モデルによる訓練データ・シナリオ生成）、(4) Q&A（DriveLLM、Talk2Carなど会話インタフェース）。

Planningでは、GPT-4Vを用いたDriveGPT4が視覚入力から走行アクションの説明を生成でき、Agent Driverはシーン記述から「車線変更すべきか」等の意思決定を行う。BEV-Plannerはbird-eye-view表現とLLMを組み合わせ、waypoint予測を実現している。PromptTrackはDETRと組み合わせてマルチビュー画像から物体追跡（一意ID付与）を行う。

LLMの主な強みとして「コモンセンス推論」が挙げられる。例えば「赤信号では止まれ」「学校ゾーンでは徐行」といった常識的ルールを事前学習から活用できる点は、エッジケース対応において従来手法より優位性がある。一方で課題は多い：(1) 推論速度（LLMはリアルタイム制御に対して遅すぎる可能性）、(2) ハルシネーション（誤った知覚・判断の出力）、(3) 訓練データの偏り（主に晴天・一般道路）、(4) LLMが直接制御コマンドを生成しない点（制御モジュールは依然必要）。

現状の評価では、LLMはPerceptionとPlanningの説明性・汎化性を高める補助的役割が現実的で、制御全体を代替する段階には至っていない。監査エージェント開発への示唆としては、LLMをEnd-to-Endな意思決定者として使うのではなく、複雑なシーン解釈や例外ケースの自然言語説明を担うモジュールとして組み込む設計パターンが参考になる。

## アイデア

- LLMのコモンセンス推論能力（事前学習で獲得した交通ルール知識）をモジュラー自動運転のPlanningに組み込むことで、エッジケースへの対応力を向上させるハイブリッドアーキテクチャの可能性
- 画像・LiDAR・RADARなど異種センサデータをトークン化することでLLMに統一的に入力できるという発想は、監査エージェントで財務・テキスト・ログなど異種データを単一LLMに統合する設計にも応用可能
- PromptTrackのように既存の特化型モデル（DETR等）とLLMを組み合わせるアーキテクチャは、LLMを全置換せずに説明性・推論性を追加するモジュール連携パターンとして汎用性が高い

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **拡散モデル** → /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 関連記事

- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_2449 静的ペルソナを超えて：LLMのための状況依存パーソナリティ制御
- /deep_1969 階層的SVGトークン化：スケーラブルなベクターグラフィックスモデリングのためのコンパクトな視覚プログラム学習

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
