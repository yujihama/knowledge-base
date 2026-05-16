---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-03
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, GPT-4 Vision, PromptTrack, LMDrive, Transformer]
category: "ai-ml"
related: [216, 2975, 1855, 105, 694]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-03T12:50:54.335921"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する可能性を解説した入門的技術記事（The Gradient、2024年3月）。自動運転の歴史的アプローチとして、Perception・Localization・Planning・Controlの4モジュールに分割する「モジュラーアプローチ」と、単一ニューラルネットワークで入出力を直結する「End-to-End学習」の2系統を概観した上で、LLMがこれらに加わる第三の可能性として位置づけられている。

LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-DecoderまたはDecoder-onlyのTransformerアーキテクチャ（GPTは純粋なDecoder型）、Multi-Head Attention、次単語予測タスクを説明する。

自動運転への適用可能性として、以下の4領域が整理されている。①Perception：GPT-4 Visionによる画像内オブジェクト認識・描写、HiLM-D・MTD-GPT・PromptTrack（DETRとLLMの組み合わせによる固有ID付きオブジェクト追跡）などのモデルが例示される。②Planning：GPT-4を使いシーン画像からドライビングアクション（車線変更、減速等）を推論するモデルとして、DriveGPT4・DiMA・LMDrive（LiDARとテキストを融合）が紹介される。③データ生成：拡散モデルと組み合わせてトレーニングデータや代替シナリオを生成する用途。④Q&A：チャットインターフェース経由でシナリオに関する質問応答を行う用途。

LLMの自動運転適用における課題として、①リアルタイム推論速度（LLMは一般に低速）、②センサーデータ（LiDAR点群・RADAR等）のトークン化の難しさ、③ハルシネーション（誤情報生成）の安全上のリスク、④大量トレーニングデータの必要性が挙げられている。

Vision Transformer（ViT）や Video Vision Transformerにより画像・動画をトークン化してTransformerに入力する手法が自動運転LLM研究の共通基盤となっており、End-to-Endモデルとの組み合わせが有望な方向性として示されている。監査エージェント開発への示唆としては、複数の異質なデータソース（構造化・非構造化）をトークン化して単一モデルに統合する設計思想、及びPlanning段階での「状況認識→行動推論」のLLM活用パターンが参考になる。

## アイデア

- 異質なセンサーデータ（LiDAR点群・画像・テキスト）をすべてトークン化してTransformerに統一入力する設計は、監査エージェントで財務数値・PDF文書・ログを単一モデルに統合する際のアーキテクチャ参考になる
- PromptTrackのようにDETR等の既存専門モデルとLLMを組み合わせる「ハイブリッド構成」は、既存ルールベース監査ロジックとLLM推論を共存させる設計パターンと対応する
- 自動運転のPlanning段階でLLMが『シーン記述→次の行動推論』を行う構造は、ReActエージェントの『観察→思考→行動』ループと同型であり、エージェント設計の汎用性を示す

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **Multi-Head Attention** → /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜

## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_2975 正規化フリーTransformerの初期化時における劣臨界信号伝播
- /deep_1855 機械学習をコードとして扱う時代の到来
- /deep_105 TransformerでAttention Residualsを観察する
- /deep_694 QUEST: クエリ変調球面アテンションによるロバストなアテンション定式化

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
