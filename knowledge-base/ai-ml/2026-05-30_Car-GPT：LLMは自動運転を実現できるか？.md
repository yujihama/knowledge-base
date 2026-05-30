---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-30
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, GPT-Driver, DriveVLM, PromptTrack, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-30T09:20:28.029946"
---

## 要約

本記事は、自動運転へのLLM（大規模言語モデル）応用の可能性を解説した入門的技術解説記事（2024年3月）。従来の自動運転システムは「モジュール型」アプローチ（Perception・Localization・Planning・Controlの4モジュール構成）と、単一ニューラルネットワークで操舵・加速を予測する「End-to-End学習」の2系統が主流だった。筆者はこれらが未解決であることを前提に、LLMを「予期せぬ答え」として位置づける。LLMの基礎としてTokenization（テキスト→数値変換）、Transformerアーキテクチャ（Encoder-Decoder構造、Multi-head Attention）、Next-Word Predictionを説明した上で、自動運転への転用方法を論じる。入力はカメラ画像・LiDAR点群・RADARデータなどに拡張（Vision Transformerの手法で「トークン化」）し、出力はレーン変更等のドライビングタスクに変更する。自動運転でLLMが活躍する研究領域として、①Perception（HiLM-D、MTD-GPT、PromptTrackなどのモデルが物体検出・追跡を実施）、②Planning（GPT-Driverがテキストベースで走行計画を記述し、DriveVLMが鳥瞰図を解析）、③データ生成（Diffusion Modelによる学習データ・代替シナリオの合成）、④Q&A（チャットインターフェース経由のシナリオ問い合わせ）の4領域を挙げる。特にPlanningでは、従来のEnd-to-End手法のブラックボックス問題に対し、LLMが自然言語で計画根拠を説明可能な点が差別化要因として強調される。一方で、リアルタイム処理の計算コスト、センサーデータ（特にLiDAR点群）のトークン化効率、低レイテンシでの推論実行など未解決の実用課題も明示している。監査エージェント開発への示唆としては、複数モダリティ入力（構造化データ・非構造化文書・数値ログ）を統一的にトークン化してTransformerに入力するアーキテクチャパターンが参考になる。また、意思決定の根拠をテキストで説明可能にするLLMの特性は、監査トレーサビリティ要件に直接適用可能な設計思想といえる。

## アイデア

- LiDAR点群・RADARデータ・カメラ画像を統一的にトークン化してTransformerに入力する設計は、監査システムで財務数値・契約文書・ログデータを単一モデルで処理する際のアーキテクチャ参考になる
- GPT-Driverのように意思決定を自然言語で記述・説明可能にするアプローチは、ブラックボックス問題の解決策として監査エージェントの説明可能性要件に直接応用できる
- PromptTrackがDETR（物体検出器）とLLMを組み合わせたように、既存の専門モデルとLLMをハイブリッドで使う設計パターンは、監査ドメイン固有の分類器＋LLMの組み合わせ設計に示唆を与える

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **マルチモーダルLLM** → /deep_6132 SVFSearch: ゲーム縦型ドメインにおける短尺動画フレーム検索のマルチモーダル知識集約型ベンチマーク

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
