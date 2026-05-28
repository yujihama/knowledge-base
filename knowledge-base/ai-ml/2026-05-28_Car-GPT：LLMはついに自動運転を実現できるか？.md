---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-28
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, マルチモーダル, PromptTrack, GPT-4V]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-28T09:26:53.678876"
---

## 要約

本記事は2024年3月に The Gradient に掲載された解説記事で、LLM（大規模言語モデル）を自動運転車に適用する研究動向を俯瞰している。自動運転の従来アーキテクチャは「モジュラー型」（Perception・Localization・Planning・Controlの4モジュール分離）と「End-to-End学習」（単一ニューラルネットワークによるステアリング・加速度の直接予測）の2系統に大別される。いずれも完全な自動運転には至っておらず、LLMがその突破口となり得るかを検証する。

LLMの基本構造として、テキストをトークン列（数値列）に変換するTokenization、Encoder-DecoderまたはDecoder-only構造のTransformer（Multi-Head Attention・Layer Normalizationなどのブロックで構成）、そして次単語予測（next-word prediction）という3要素を説明している。自動運転への適用では入力をカメラ画像・LiDARポイントクラウド・RADARデータなどにトークン化（Vision Transformerや Video Vision Transformer）し、出力を走行タスク（車線変更等）や環境記述に変換する設計となる。

2023年時点の主要研究領域は4つ。①Perceptionでは、GPT-4 VisionによるオブジェクトリストアップのほかHiLM-D・MTD-GPTによる動画対応検出、PromptTrackによるオブジェクトIDトラッキングが行われている。②Planningでは、BEV（鳥瞰図）画像または知覚出力を基に「直進継続」「徐行」などの行動決定を生成する研究が進む。③Generationでは、Diffusionモデルを組み合わせた学習データ・代替シナリオ生成が活発。④Q&A（チャットインターフェース）では、シーンに対して自然言語で質問・回答できるシステムが研究されている。

課題として、①LLMの推論速度（自動運転はリアルタイム性が必須）、②大量の専用学習データの確保、③ブラックボックス性による説明可能性・安全保証の困難さが挙げられている。一方で、LLMの強みである自然言語による推論能力・ゼロショット汎化・マルチモーダル入力対応はPlanning層での意思決定品質向上に寄与する可能性がある。監査AIへの示唆として、LLMをPerception（異常検知・証跡解析）とPlanning（対応方針決定）に分離して活用するモジュラーvsEnd-to-Endの設計議論は、監査エージェントのアーキテクチャ選択（LangGraphによるノード分離 vs 単一エージェント）に直接対応する。特にPromptTrackのようにID付きトラッキングをLLMで行う発想は、監査証跡の一貫追跡ロジックへの応用が考えられる。

## アイデア

- モジュラー型 vs End-to-End のアーキテクチャ議論は自動運転に限らず、監査エージェント設計（LangGraphのノード分離 vs 単一LLMによる直接判断）にそのまま適用できる構図であり、設計トレードオフの整理に有用
- PromptTrackがDETRとLLMを組み合わせてオブジェクトにユニークIDを付与しトラッキングする手法は、監査証跡における取引・エンティティの一貫追跡問題へのアナロジーとして面白い
- LLMのPlanning層への適用（BEV画像から行動方針を自然言語で生成）は、LLM-as-judgeやReActパターンと構造が類似しており、エージェントの意思決定説明可能性の実装アイデアとして参照できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **BEV（鳥瞰図表現）** (TODO: 読むべき)

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
