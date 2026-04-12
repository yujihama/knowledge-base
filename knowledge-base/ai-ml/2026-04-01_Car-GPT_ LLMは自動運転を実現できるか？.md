---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-01
tags: [LLM, 自動運転, Vision Transformer, Perception, Planning, End-to-End学習, GPT-4V, DriveGPT4, マルチモーダル]
category: "ai-ml"
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-01T21:06:25.145018"
---

## 要約

本記事（The Gradient、2024年3月）は、LLM（大規模言語モデル）が自動運転の4大モジュール（Perception・Localization・Planning・Control）にどう応用できるかを解説した入門的サーベイ記事。

自動運転の従来アプローチは「モジュラー型」（知覚・自己位置推定・計画・制御を個別モジュールで構成）と「End-to-End学習」（単一ニューラルネットで操舵・加速を予測するが、ブラックボックス問題を抱える）の2系統が主流だった。LLMはこれに対する「第三の道」として位置付けられる。

LLMの仕組みとして、テキストをトークン（数値列）に変換するTokenization、Encoder-Decoder構造のTransformerによる処理、Next-Word Prediction出力の3点を説明。自動運転への適用では、入力を画像・LiDARポイントクラウド・RADARデータ等に拡張し（Vision Transformerが実現）、出力を車線変更等のドライビングタスクに変更する形で適応できる。

2023年時点の主要研究領域は4つ。①Perception：GPT-4 Vision・HiLM-D・MTD-GPTがカメラ画像からオブジェクト検出・追跡を実施。PromptTrackはDETRとLLMを組み合わせオブジェクトにユニークIDを付与。②Planning：DriveGPT4・DriveLikeHuman・MAPLM等が鳥瞰図や自然言語でルートや行動判断を生成。③Generation：DrivingDiffusion等が拡散モデルで学習用合成データ・代替シナリオを生成。④Q&A：自然言語インターフェースでシナリオ説明や行動根拠を出力するチャット型インターフェース。

課題として、LLMは解釈可能性（「なぜこの判断をしたか」の説明可能性）と推論速度の両面で課題があり、現実のリアルタイム制御への統合は未解決。End-to-End学習のブラックボックス問題をLLMが解決できるか、あるいはハイブリッドアーキテクチャ（モジュラー＋LLM判断）が現実的かが議論の焦点となっている。

## アイデア

- LLMをドメイン特化タスク（知覚・計画）に適用する際、入力モダリティ（画像・点群・テキスト）をトークン化して統一的なTransformerに通す設計パターンは、監査エージェントでも財務データ・文書・ログを統一的に扱う際に応用可能
- DriveGPT4等のPlanning LLMが自然言語で行動根拠を出力する設計は、LLM-as-judgeの文脈で「なぜその判断をしたか」の説明可能性（Explainability）を確保するアーキテクチャパターンとして参考になる
- 生成モデル（DrivingDiffusion等）で学習用合成データを大量生成するアプローチは、監査領域で希少な不正事例の合成データ生成に転用できる可能性がある

## Yujiの取り組みへの示唆

直接的な監査AI応用は薄いが、LLMをモジュラーシステムの各コンポーネント（知覚・判断・計画）に組み込むアーキテクチャ設計は、LangGraphベースの監査エージェントで各ノード（リスク認識・証跡評価・判断）にLLMを配置する設計と構造的に類似している。特に、Planning LLMが自然言語で行動根拠を生成するアプローチは、監査エージェントの判断ログ・説明可能性の実装に直接参考になる。

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
