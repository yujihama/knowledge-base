---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-13
tags: [LLM, 自動運転, Vision Transformer, Perception, End-to-End学習, Planning, PromptTrack, DriveGPT, 拡散モデル]
category: "ai-ml"
related: [1347, 558, 1266, 1449, 564]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-13T12:48:35.437094"
---

## 要約

自動運転の歴史的アプローチは「モジュール型」と「End-to-End学習」の2系統に大別される。モジュール型は認識（Perception）・自己位置推定（Localization）・計画（Planning）・制御（Control）の4段階を独立したコンポーネントで処理する設計で、2010年代の主流だった。一方、End-to-Endは単一ニューラルネットワークがステアリングと加速度を直接予測するが、ブラックボックス問題を抱える。本記事はこれらの限界を踏まえ、LLM（大規模言語モデル）が第三の解になり得るかを検討する。

LLMの基礎として、テキストをトークン（数値）に変換するトークン化、エンコーダ・デコーダ構造のTransformerアーキテクチャ、次単語予測タスクの3点が解説される。自動運転への応用では、入力を画像・LiDARポイントクラウド・RADARデータ等に拡張し、Vision Transformerで処理することでLLMの枠組みをそのまま流用できる。

2023年の主要研究領域は4分野。①Perception：GPT-4 Visionが入力画像から物体・レーン情報を記述するタスク。HiLM-D、MTD-GPTが動画対応を実現し、PromptTrackはDETRとLLMを組み合わせてオブジェクトに一意IDを付与する追跡機能を持つ。②Planning：DriveGPTやDriveVLMは鳥瞰図やPerception出力を基に「車線維持」「譲行」等の行動判断をテキストで出力する。③データ生成：拡散モデル（Diffusion）を使ったトレーニングデータや代替シナリオの自動生成。④Q&A：シナリオに基づいた対話インタフェースの構築。

LLMの自動運転への貢献として特筆されるのは、テキストベースのコモンセンス推論により「見知らぬ道路状況」への汎化性能が期待できる点と、自然言語による説明可能性（XAI的機能）が付与される点である。一方、リアルタイム処理のレイテンシ、センサーデータとテキスト空間の統合コスト、hallucination問題は未解決の課題として残る。監査エージェント開発への示唆として、LLMがモジュール型パイプラインの各ステージを自然言語インタフェースで統合する設計パターンは、LangGraphベースの監査エージェントにおけるサブエージェント間のハンドオフ設計にも応用可能である。

## アイデア

- PromptTrackのようにDETR等の既存物体検出器とLLMを組み合わせるハイブリッド設計は、LLM単体の弱点（空間認識精度）を補いつつ自然言語推論を付加する現実的なアーキテクチャパターン
- 自動運転の4モジュール（Perception/Localization/Planning/Control）はそれぞれ独立したLLMサブエージェントに対応させられる構造であり、マルチエージェントシステム設計の参照モデルとして機能する
- LLMのhallucination問題は医療・金融と同様に自動運転でも致命的リスクになるため、LLM-as-judgeによる出力検証レイヤーの必要性が高まる

## 前提知識

- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **DETR** (TODO: 読むべき)
- **拡散モデル** → /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 関連記事

- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成
- /deep_558 ReproMIA：プロアクティブなメンバーシップ推論攻撃のためのモデルリプログラミング包括分析
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
