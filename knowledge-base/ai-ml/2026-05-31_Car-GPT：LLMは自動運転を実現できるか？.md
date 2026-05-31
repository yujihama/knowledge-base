---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-31
tags: [LLM, 自動運転, Vision Transformer, エンドツーエンド学習, Perception, Planning, DriveGPT4, PromptTrack, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 716, 1527]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-31T09:22:04.959162"
---

## 要約

自動運転の研究は2010年代から「モジュラーアプローチ」（知覚・位置推定・計画・制御の4モジュール構成）を主流としてきたが、エンドツーエンド学習の台頭とともに、LLMを自動運転に応用する研究が2023年以降活発化している。本記事はその技術的可能性を整理した解説記事である。

LLMの基礎として、テキストをトークン（数値列）に変換するトークン化、Encoder-Decoder構造に基づくTransformerアーキテクチャ（Multi-head Attention, Layer Normalization等）、次単語予測タスクの3点が説明される。GPT系モデルはDecoder-onlyであるのに対し、BERTはEncoder-only、T5はEncoder-Decoderという違いがある。

自動運転へのLLM適用は主に4分野で研究が進む。①知覚（Perception）：GPT-4 Visionによる物体検出・記述、HiLM-D・MTD-GPTによるマルチビュー画像解析、PromptTrackによるDETRとLLMの組み合わせによるオブジェクトトラッキング（ID付与）。②計画（Planning）：DriveGPT4やDriveVLMなどVision-Language Modelによるbird-eye view解析と行動指示生成。③データ生成（Generation）：拡散モデル（Diffusion Model）を組み合わせた学習用シナリオデータの合成。④Q&Aインターフェース：自然言語でシナリオに関する質問に回答するチャットUI。

技術的な課題として、LLMの推論遅延（リアルタイム制御への不適合）、ハルシネーション（誤認識）、センサーデータ（LiDAR・RADAR点群）のトークン化効率、解釈可能性の担保が挙げられる。一方で、自然言語による説明可能性やfew-shot学習による汎化能力は従来手法に対する優位点として評価されている。

Vision Transformerによる画像トークン化技術がLLMと自動運転を接続する鍵であり、センサーフュージョン（カメラ・LiDAR・RADAR）をTransformerの入力として統一的に扱える点が研究上の重要な方向性となっている。監査エージェント開発への示唆としては、複数の異種データソース（ログ・数値・テキスト）をトークン化して単一モデルで横断処理するアーキテクチャ設計の参考になる。

## アイデア

- LiDAR・RADAR点群データをVision Transformerでトークン化し、テキストと同一Transformerに入力するマルチモーダルアーキテクチャは、監査ログ・財務数値・テキスト報告書を横断処理する監査エージェントの設計に直接応用できる
- PromptTrackがDETR（物体検出器）とLLMを組み合わせることで「このオブジェクトはID#3」と一意識別する手法は、監査エージェントが取引エンティティや異常イベントを追跡する際のエンティティトラッキング機構として参考になる
- 自動運転における説明可能性（「なぜこの行動を選択したか」を自然言語で出力）の要求は、監査AI における判断根拠の文書化要件と構造的に同一であり、LLMベースの計画モジュールが解釈可能性問題を解決する共通アプローチとなりうる

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **マルチモーダルLLM** → /deep_6132 SVFSearch: ゲーム縦型ドメインにおける短尺動画フレーム検索のマルチモーダル知識集約型ベンチマーク

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
