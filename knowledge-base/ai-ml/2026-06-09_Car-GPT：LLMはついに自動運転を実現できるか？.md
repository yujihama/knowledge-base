---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-09
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, PromptTrack, DriveVLM, 拡散モデル]
category: "ai-ml"
related: [3785, 1347, 558, 2171, 3746]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-09T09:22:52.398590"
---

## 要約

本記事はThe Gradientに掲載された解説記事で、LLM（大規模言語モデル）を自動運転に応用する可能性を体系的に整理している。

自動運転の従来アプローチは「モジュール型」設計で、Perception（物体認識）・Localization（自己位置推定）・Planning（経路計画）・Control（操舵・加速指令生成）の4モジュールに分割されていた。2010年代後半からはこれらを単一ニューラルネットワークで置き換えるEnd-to-Endアプローチが台頭したが、ブラックボックス問題が残る。そこに「LLMが第三の解になりうるか」という問いを立てている。

LLMの基本構造として、テキストをトークン（数値列）に変換するTokenization、EncoderとDecoderで構成されるTransformerアーキテクチャ（multi-head attention、layer normalization等）、そして次トークン予測による出力生成を解説。自動運転への転用では、入力を画像・LiDARポイントクラウド・RADARデータに置き換え（Vision Transformerと同様のトークン化）、出力を車線変更などのドライビングタスクにマッピングする。

2023年時点の主要研究領域として以下を挙げる：
- **Perception**：GPT-4 Visionによる物体検出、HiLM-D・MTD-GPTによる動画対応、PromptTrack（DETRとLLMの組み合わせによるID付きオブジェクト追跡）
- **Planning**：DriveVLM・DriveLLM・SurrealDriverなどが鳥瞰図や認識結果を入力に「直進」「譲る」等の行動を出力
- **Data Generation**：DrivingDiffusion等の拡散モデルを用いた学習データ・代替シナリオの合成生成
- **Q&A Interface**：シーン画像に基づくチャット型問いかけへの回答（説明可能性の向上）

LLMを自動運転に使う主な利点は、膨大な量の事前学習テキストから獲得した「世界モデル」的な常識推論能力。例えば「赤信号かつ子供が飛び出した場合にどう行動すべきか」といった長尾シナリオへの対応が期待される。一方で課題として、リアルタイム処理の遅延（推論レイテンシ）、センサーデータへの幻覚（hallucination）リスク、安全クリティカルな判断のVerifiabilityが挙げられる。

監査エージェント開発への示唆：自動運転の4モジュール分割（Perception→Localization→Planning→Control）は、監査エージェントの「証拠収集→リスク評価→判断→報告書生成」パイプラインと構造的に類似する。End-to-Endアプローチ vs. モジュール型の議論は、LangGraphによるReActエージェント設計でも同様に生じるトレードオフ（透明性 vs. 柔軟性）であり、設計指針として参照価値がある。

## アイデア

- LLMの事前学習で得た「世界知識」を自動運転の長尾シナリオ（子供の飛び出し等）への対応に活用する発想は、監査エージェントが会計基準や過去事例の知識を異常検知に転用する構造と同型
- PromptTrackがDETR（物体検出）とLLMを組み合わせてオブジェクトにIDを付与する手法は、監査で同一取引エンティティを複数証跡にわたって追跡するEntity Resolution問題への応用が考えられる
- 自動運転のモジュール型 vs End-to-Endの論争は、LangGraphでツール呼び出しチェーンを明示的に設計するか、単一LLMに推論を委ねるかのエージェント設計トレードオフそのものであり、どちらも説明可能性と性能のバランス問題として整理できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **multi-head attention** → /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜

## 関連記事

- /deep_3785 遮蔽に強い3D人体メッシュ復元のための識別・生成シナジーフレームワーク
- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成
- /deep_558 ReproMIA：プロアクティブなメンバーシップ推論攻撃のためのモデルリプログラミング包括分析
- /deep_2171 Multi-ORFT：協調運転のためのマルチエージェント拡散プランニングにおける安定したオンライン強化ファインチューニング
- /deep_3746 LLMs+：今AIで重要な10のこと（MIT Technology Review）

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
