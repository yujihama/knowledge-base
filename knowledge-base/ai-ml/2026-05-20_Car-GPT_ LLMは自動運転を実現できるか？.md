---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-20
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, UniAD, PromptTrack, Diffusion Model, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 3717, 4900, 3260]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-20T21:37:18.526264"
---

## 要約

本記事は、LLM（大規模言語モデル）を自動運転に応用する可能性を体系的に解説したThe Gradientの技術解説記事（2024年3月）。

自動運転の従来アーキテクチャは「モジュール型」（Perception→Localization→Planning→Control）とEnd-to-End学習の2系統が主流だが、いずれも完全自律走行の実現には至っていない。本記事はLLMを第三の解として位置づけ、その可能性を検証する。

LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-Decoderアーキテクチャを持つTransformerブロック（Multi-Head Attention、Layer Normalization等）、そしてNext-Word Predictionによる出力生成の3要素を説明。GPTは純粋なDecoder型であることも明示される。

自動運転への適用においては、入力をカメラ画像・LiDAR点群・RADARデータ等にTokenize（Vision Transformerを活用）し、Transformerモデルはそのまま流用、出力タスクに応じてカスタマイズする設計となる。

2023年時点で研究が活発な適用領域は4つ：
1. **Perception（知覚）**: GPT-4 Visionが画像内オブジェクトを検出・記述。HiLM-D、MTD-GPTが物体検出・予測・追跡を実施。PromptTrackはDETRと LLMを組み合わせ、オブジェクトに一意のIDを付与する4D Perception的動作を実現。
2. **Planning（計画）**: UniAD（NeurIPS 2023採択）がEnd-to-Endの統合的計画を実現。DriveVLMやDriveGPT4は自然言語での走行シナリオ説明と行動計画を生成。
3. **Generation（生成）**: 拡散モデル（Diffusion Model）を活用し、学習用合成データや代替シナリオを自動生成。データ不足問題へのアプローチとして機能。
4. **Q&A（質疑応答）**: チャットインターフェースを通じて走行シナリオへの質問応答が可能。説明可能性の向上に寄与。

課題として、LLMは推論速度が遅く（リアルタイム制御への適用困難）、センサーデータの直接処理に不向きな点が挙げられる。現実的なアプローチは、LLMをモジュール型の一部として組み込むハイブリッド設計（特にPlanning層への適用）とされている。

監査エージェント開発への示唆：LLMを特定モジュール（Planning相当の意思決定層）として組み込むアーキテクチャ設計の考え方は、監査エージェントにおけるReActベースのPlanning-Actionループ設計と構造的に類似している。UniADのようなEnd-to-Endアプローチを参考に、監査フロー全体をLLMで統合するか、各サブタスクにLLMを限定適用するかのトレードオフ検討に応用できる。

## アイデア

- LLMのTokenizationはテキストに限らず、LiDAR点群やカメラ画像など任意のセンサーデータにも適用可能であり、Vision Transformerと組み合わせることで入力モダリティを統一できる点は、マルチモーダルエージェント設計の汎用性を示している
- UniAD（NeurIPS 2023）のようにPerception・Prediction・Planning全体をEnd-to-Endで統合するアーキテクチャは、個別モジュールの積み上げより統一的な目標関数で最適化できる利点があり、監査エージェントの全体最適化設計に応用可能な視点を提供する
- LLMのPlanning層への限定適用（ハイブリッド設計）という現実解は、低レイテンシが要求されるリアルタイムシステムでのLLM活用の一般的な設計パターンであり、監査エージェントにおける非同期・バッチ処理とリアルタイム判断の分離設計に直接対応する

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **LiDAR点群処理** (TODO: 読むべき)

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_3717 今AIで重要な10のこと：LLMs+時代の到来
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_3260 LLMs+：今AIで重要な10のこと（MIT Technology Review）

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
