---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-07
tags: [LLM, 自動運転, Transformer, End-to-End学習, Vision-Language Model, Planning, chain-of-thought, DriveVLM, BEV, GPT-Driver]
category: "ai-ml"
related: [216, 2219, 105, 1638, 672]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-07T12:48:15.815151"
---

## 要約

本記事は、Large Language Model（LLM）を自動運転に応用する「Car-GPT」的アプローチを解説する入門記事（The Gradient、2024年3月）。自動運転の歴史的アプローチとして、モジュラー型（Perception→Localization→Planning→Controlの分離）とEnd-to-End学習（単一ニューラルネットワークによるステアリング・加速度の予測）を対比し、そこにLLMという第3の軸を導入できるかを検討する。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造のTransformer、次単語予測（next-word prediction）の3要素を説明。自動運転への転用では、入力を画像・LiDARポイントクラウド・RADARデータなどに変更し、出力を車線変更・停止などのドライビングタスクや自然言語での状況説明に変更する形で適用できる。

研究が活発な4領域として、①Perception（HiLM-D、MTD-GPT、PromptTrackなどによる物体検出・追跡）、②Planning（DriveVLM、LanguageMPCなどによる行動決定）、③データ生成（拡散モデルによる合成トレーニングデータ生成）、④Q&A（シナリオへの自然言語応答）を挙げる。Planningでは、GPT-Driverのように路上状況をテキスト記述に変換してGPT-4で次の行動を推論させ、waypoint（通過点）を出力する手法や、LanguageMPCのようにLLMをModel Predictive Controlの高レベル計画器として使う手法が紹介される。

End-to-End LLMアーキテクチャとしては、Tesla Autopilotに類似したTransformer型E2Eパイプライン、および複数カメラ映像をBEV（Bird's Eye View）特徴量に変換して言語トークンとともにLLMへ入力するDriveVLMが紹介される。DriveVLMはchain-of-thought推論で自然言語による行動理由を生成した上でwaypoint列を出力する。

課題として、①LLMの推論速度（自動運転に必要なリアルタイム性との乖離）、②ハルシネーション（存在しない物体の幻覚）、③エッジケースへの対応不足、④大量の高品質な自動運転特化データの必要性が指摘される。監査エージェント開発への示唆としては、LLMをchain-of-thought推論で計画レイヤーに組み込み自然言語で判断根拠を出力させるアーキテクチャパターンは、監査ワークフローのPlanning層（リスク評価→手続き選択→証拠収集の逐次計画）に直接応用可能。DriveVLMのように推論ステップを言語化して出力することで、監査エージェントの説明可能性・レビュー容易性を高めるアプローチとして参考になる。

## アイデア

- LLMをPlanningレイヤーに限定して使い、chain-of-thoughtで行動根拠を自然言語出力させるGPT-Driverの手法は、監査エージェントの判断ログ生成にそのまま転用できる
- DriveVLMのように多視点画像→BEV特徴量→言語トークン統合という入力設計は、異種センサーデータ（財務・非財務）を統合する監査マルチモーダルモデルの設計参考になる
- LanguageMPCのようにLLMを高レベルプランナー、既存制御アルゴリズムを低レベル実行器とする2層分離設計は、エージェントのPlannerとExecutorを分離するReAct系アーキテクチャと構造的に同型

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **BEV (Bird's Eye View)** (TODO: 読むべき)
- **Model Predictive Control** (TODO: 読むべき)
- **chain-of-thought推論** (TODO: 読むべき)

## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_2219 テキストからモデルへの変換を支援するLLMコパイロット：Text2ModelとText2Zinc
- /deep_105 TransformerでAttention Residualsを観察する
- /deep_1638 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- /deep_672 Mambaの解説：Transformerに挑む状態空間モデル

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
