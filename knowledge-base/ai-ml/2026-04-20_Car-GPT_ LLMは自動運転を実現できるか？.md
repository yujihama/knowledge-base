---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-20
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, PromptTrack, GPT-4V]
category: "ai-ml"
related: [1266, 1760, 1449, 1969, 564]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-20T12:11:53.013699"
---

## 要約

本記事はThe Gradient誌（2024年3月）に掲載された解説記事で、大規模言語モデル（LLM）が自動運転技術にどう応用されるかを体系的に紹介している。自動運転の従来アーキテクチャは「モジュール型」（Perception→Localization→Planning→Control の4段階）と「End-to-End学習」（単一ニューラルネットが操舵・加速を予測）の2系統が主流だったが、どちらも完全自動運転の実現には至っていない。LLMはこの閉塞状況を打破する「ペニシリン的偶然」となりうるかという問いから議論が始まる。

LLMの基本原理として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造のTransformerアーキテクチャ（マルチヘッドアテンション、Layer Normalization等）、Next-Word Predictionによる出力生成の3要素を解説。画像・LiDARポイントクラウド・RADARデータも「トークン化可能」（Vision Transformer経由）なため、同一のTransformerバックボーンで扱えると説明する。

自動運転における2023年時点の主要研究領域は4つ：(1) Perception（画像から環境・物体を記述）、(2) Planning（鳥瞰図や知覚出力から行動を決定）、(3) Generation（拡散モデルによる訓練データ・代替シナリオ生成）、(4) Q&A（シナリオへの問い合わせインターフェース）。PerceptionではGPT-4 Vision、HiLM-D、MTD-GPT、PromptTrack（DETRとLLMを組み合わせ、物体に一意IDを付与）などが挙げられる。PlanningではDriveVLM・DriveWithLLM等が鳥瞰図入力から次の行動を出力する研究として紹介されている。

監査エージェント開発への示唆：LLMをブラックボックス的に使うEnd-to-Endアプローチと、モジュール型の説明可能アーキテクチャの対比は、監査AIにも直接当てはまる。監査エージェントでは判断根拠の説明可能性（XAI）が必須であり、LLMのPlanning段階をQ&Aインターフェースと組み合わせる設計（「なぜこの取引を異常とみなしたか」を自然言語で出力）は参考になる。また、Generation（拡散モデルによるシナリオ生成）は監査用の合成データ生成や例外シナリオの拡張にも応用可能。

## アイデア

- 画像・LiDAR・RADARといった異種センサデータを全てトークン化してTransformerに入力できるという設計思想は、マルチモーダルエージェントの入力統一化に応用可能
- PromptTrackがDETRとLLMを組み合わせて物体に一意IDを付与する手法は、監査ログの各エンティティ（取引、担当者）を一意に追跡するエージェント設計のアナロジーとして興味深い
- 自動運転のPlanning段階をLLMに担わせQ&Aで意思決定を説明させるアプローチは、ReActパターンによる監査エージェントの判断根拠出力と構造的に同一

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer（Attention）** (TODO: 読むべき)
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開

## 関連記事

- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_1969 階層的SVGトークン化：スケーラブルなベクターグラフィックスモデリングのためのコンパクトな視覚プログラム学習
- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
