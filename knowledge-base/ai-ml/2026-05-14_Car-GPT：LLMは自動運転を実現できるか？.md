---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-14
tags: [LLM, 自動運転, Vision-Language Model, Transformer, Planning, GPT-Driver, PromptTrack, End-to-End学習, マルチモーダル]
category: "ai-ml"
related: [216, 4906, 4441, 3582, 4900]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-14T21:13:36.315703"
---

## 要約

自動運転の歴史的アプローチは「モジュール型」（Perception・Localization・Planning・Controlを個別モジュールに分割）と「End-to-End学習」（単一ニューラルネットワークがステアリング・加速を直接予測）の2系統があったが、いずれも完全自律走行を達成するには至っていない。本記事はLLM（大規模言語モデル）が第三の解答となり得るかを検討する。LLMの基本はトークン化（テキストを数値列に変換）とTransformerアーキテクチャ（Encoder-Decoderまたはデコーダ単独構成、Multi-Head Attentionブロックで構成）であり、次単語予測タスクで訓練される。自動運転への適用では、入力をカメラ画像・LiDAR点群・RADARデータ・レーンライン等のトークン列に変換することで、同一のTransformerバックボーンをそのまま利用可能。2023年時点の主要研究領域は（1）Perception、（2）Planning、（3）データ生成（Diffusion活用）、（4）Q&Aインターフェースの4分野。Perceptionでは、GPT-4 Visionのようなマルチモーダルモデルが物体検出・説明生成を行い、HiLM-DやMTD-GPTが動画対応、PromptTrackがDETRと組み合わせてユニークID付き追跡を実現。PlanningではGPT-Driverが注目で、GPT-4に構造化された位置情報をプロンプトとして入力し、自然言語の説明付きで次の軌道を出力する手法を採用。nuScenesデータセットでIDという指標においてML-Plannerを上回る結果を報告している。また、DriveVLMのようにVision-Language Modelを活用し、シーン理解と高レベル計画を分離して処理する設計も登場。データ生成分野ではDiffusionモデルとLLMを組み合わせたコーナーケース生成が研究されており、学習データの多様性確保に貢献。Q&A用途ではDriveGPTやDriveLikeHuman等、ドライバーと対話しながら判断根拠を説明できるシステムが開発されている。一方で課題も明確で、LLMは推論速度が遅く（最新GPU環境でも数百ミリ秒以上かかる場合がある）、自動運転の実時間制御（数十ミリ秒単位の応答）とはギャップがある。またハルシネーション（事実と異なる出力）のリスクや、安全クリティカルな判断への信頼性評価手法が未確立である点も課題として挙げられる。監査エージェント開発への示唆としては、複雑な入力（センサ融合データ）を構造化プロンプトに変換してLLMに渡しつつ、判断根拠を自然言語で出力させるGPT-Driverのアーキテクチャパターンは、監査エージェントにおける証拠→判断→説明の流れと直接対応しており、ReActエージェントの「Reasoning」ステップをLLMに担わせる設計指針として参照価値がある。

## アイデア

- GPT-Driverの手法：センサから得た構造化位置情報をテキストプロンプトに変換してGPT-4に入力し、自然言語の説明付き軌道を出力させることで、ブラックボックス問題を緩和しつつPlanning性能をML-Plannerより向上させた点
- PromptTrackのアーキテクチャ：DETRの物体検出結果とLLMを組み合わせ、検出オブジェクトにユニークIDを付与して時系列追跡を行う設計は、ReActエージェントにおける状態管理（どの証拠が同一エンティティか）の参考になる
- LLMの推論レイテンシが自動運転のリアルタイム制御要件（数十ms）と根本的に相反するという制約は、監査エージェントでも長時間推論タスクと即応が必要なタスクを分離すべき設計指針として応用できる

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **LiDAR点群処理** (TODO: 読むべき)
- **nuScenesデータセット** (TODO: 読むべき)

## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_4906 連載｜生成AIの数理 第1回「次の言葉」を予測せよ ——n-gramからアテンションまで，必然の連鎖——
- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
