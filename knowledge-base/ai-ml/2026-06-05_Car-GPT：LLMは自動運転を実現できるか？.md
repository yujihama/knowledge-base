---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-05
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, マルチモーダル, GPT-4V]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-05T21:21:23.247842"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する可能性をサーベイ的に解説したもの。従来の自動運転システムは「モジュール型」アプローチ（知覚・自己位置推定・計画・制御の4モジュール）で構成されていたが、2010年代後半からEnd-to-End学習（単一ニューラルネットワークが操舵・加速を直接予測）が注目された。LLMはこの文脈での「第三の選択肢」として位置づけられる。

LLMの基本構造として、テキストをトークン（数値）に変換するTokenization、EncoderとDecoderからなるTransformerアーキテクチャ、次単語予測（Next-Word Prediction）の3要素を解説。自動運転への適用では、入力をカメラ画像・LiDARポイントクラウド・RADARデータ等に置き換え、Vision Transformerで処理する形に拡張する。

研究が活発な4領域を紹介：①Perception（知覚）ではGPT-4 Vision、HiLM-D、MTD-GPT、PromptTrackが物体検出・追跡を実施。②Planning（計画）ではDriveGPT4やDriving with LLMsが鳥瞰図や画像から次のアクション（車線変更、徐行等）を出力。③Generation（生成）ではDiffusionモデルを用いた合成学習データの生成やシナリオ拡張に活用。④Q&A（質疑応答）ではDriveVLMやDriveLMがシナリオを説明・対話化し、判断根拠の透明性を高める。

LLMの自動運転への主な利点は3点：（1）マルチモーダル入力（画像・センサ・テキスト）を統合的に処理できる汎用性、（2）「なぜ右折するか」を言語で説明できる解釈可能性、（3）Instruction tuningによる柔軟なタスク適応。課題としては、リアルタイム推論に必要な低レイテンシ実現の難しさ、大規模モデルの計算コスト、自動運転に特化した学習データの不足が挙げられる。

監査エージェント開発への示唆：LLMが知覚・推論・行動を統合的に扱う構造は、監査エージェントが証跡データを「知覚」し、リスク判断を「計画」し、調査アクションを「制御」するパイプラインと同型である。特にDriveVLM的なQ&A機能（なぜその判断をしたかを言語で返す）は、監査ログの説明可能性要件に直接応用可能。

## アイデア

- LiDARポイントクラウドや画像をトークン化してTransformerに入力するアーキテクチャは、監査証跡（ログ・財務データ）を同様にトークン化してエージェントに処理させる設計と同型であり、KB-botのエージェント設計に転用できる
- DriveVLM/DriveLMのQ&Aアプローチ（判断理由を自然言語で返す）は、LLM-as-judgeパターンの自動運転版であり、判断根拠の透明性確保という観点で監査AIと課題が一致する
- End-to-Endモデルのブラックボックス問題に対してLLMが「解釈可能な中間表現」を提供するという構図は、ReActエージェントのThought/Action/Observation分離と同じ設計思想で、複雑なパイプラインのデバッグ容易性を高める

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Encoder-Decoder Transformer** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **マルチモーダルLLM** → /deep_6132 SVFSearch: ゲーム縦型ドメインにおける短尺動画フレーム検索のマルチモーダル知識集約型ベンチマーク
- **Instruction Tuning** → /deep_2008 舗装状態評価に特化したVision-Language基盤モデル：PaveGPTとPaveInstructデータセット

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
