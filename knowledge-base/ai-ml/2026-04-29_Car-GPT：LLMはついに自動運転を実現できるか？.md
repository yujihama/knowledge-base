---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-29
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, PromptTrack, GPT-4V, DriveGPT4, 説明可能AI]
category: "ai-ml"
related: [1346, 1266, 1760, 1449, 2837]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-29T12:20:28.073368"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する可能性を、入門者向けに体系的に解説したサーベイ記事である。自動運転の従来アプローチとして「モジュール型」（Perception・Localization・Planning・Controlの4モジュール分離）と「End-to-End学習」（単一ニューラルネットワークで操舵・加速度を直接予測）の2系統を概説した上で、LLMがこれらの課題をどのように補完・代替できるかを論じる。LLMの基礎としてトークン化（テキストを数値列に変換）とTransformerアーキテクチャ（エンコーダ・デコーダ構造、マルチヘッドアテンション）を説明し、画像・LiDAR点群・RADARデータも「トークン化可能」であることを示している。自動運転への応用領域は4つに分類される。①Perception：GPT-4 VisionやHiLM-D、MTD-GPTによる画像からの物体検出・説明生成、PromptTrackによる物体追跡（DETR+LLM）。②Planning：DriveGPT4やGPT-Driverによる鳥瞰図・知覚出力を入力とした行動計画生成（「右折すべき理由」の自然言語説明付き）。③データ生成：拡散モデルを用いた訓練データ・代替シナリオの合成生成（データ不足問題への対処）。④Q&A・対話型インターフェース：DriveLMやCarPalermoによるシーン内容への自然言語問い合わせ。LLM適用の主な利点として、①コモンセンス推論（標識が見えなくても文脈から停車を判断）、②説明可能性（判断根拠を自然言語で出力）、③データ拡張（稀なエッジケースの合成）が挙げられる。一方、課題として低レイテンシ要件（リアルタイム制御との相性）、限られたコンテキストウィンドウ（高頻度センサーデータ処理）、ドメイン外シナリオへの汎化、幻覚（hallucination）による誤判断リスクが指摘されている。監査エージェント開発への示唆としては、複数モジュール（知覚・判断・実行）をLLMで統合するアーキテクチャ設計パターンが参考になる。特に「説明可能な判断出力」は监査レポート生成エージェントに直接応用可能であり、PromptTrackのようなID管理手法はエンティティ追跡（取引・仕訳の追跡）にも転用できる。

## アイデア

- LiDARやRADAR点群データもトークン化してTransformerに入力できるという発想は、監査ログや構造化データをLLMに直接入力する際のアーキテクチャ設計に応用できる
- PromptTrackのDETR+LLM構成のように、既存の特化型検出器とLLMを組み合わせるハイブリッドアーキテクチャは、専門ドメイン（監査・法規制）での精度と汎用推論の両立に有効
- LLMの「コモンセンス推論」を自動運転に使う考え方は、監査エージェントが明文化されていないルール（慣習・業界標準）を文脈推論で補完するユースケースと構造的に同一

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **拡散モデル** → /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 関連記事

- /deep_1346 LLM述語からLogic Tensor Networkへ：規制調達における神経記号的オファー検証
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_2837 非対称損失関数を用いたハイブリッドCNN-BiLSTM-Attentionモデルによる産業機器の残余寿命予測と解釈可能な故障ヒートマップ

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
