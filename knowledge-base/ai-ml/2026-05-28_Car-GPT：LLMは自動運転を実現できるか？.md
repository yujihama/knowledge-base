---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-28
tags: [LLM, 自動運転, End-to-End学習, Vision Transformer, Perception, Planning, GPT-4V, PromptTrack, DriveVLM, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-28T21:21:25.692929"
---

## 要約

本記事は、LLM（大規模言語モデル）が自動運転の未解決問題を解決する可能性について、2024年時点の研究動向を整理した解説記事である。

自動運転の従来アプローチは「モジュール型」で、Perception（認識）・Localization（自己位置推定）・Planning（経路計画）・Control（制御）の4モジュールに分割されていた。2010年代後半からEnd-to-Endアプローチが注目され、単一ニューラルネットワークでステアリング・加速度を直接予測する試みが増えたが、ブラックボックス問題が残る。ここにLLMを投入する研究が2023年以降活発化している。

技術的な仕組みとして、LLMへの入力は画像・LiDAR点群・RADAR点群・レーン情報などで、Vision TransformerやVideo Vision Transformerによりトークン化される。Transformerアーキテクチャ自体はモーダルに非依存であるため、出力タスクを変えることで自動運転の各タスクに対応できる。

研究が活発な領域は主に4つ。①Perception：GPT-4 VisionやHiLM-D、MTD-GPTが画像からオブジェクト検出・追跡を実施。PromptTrackはDETRとLLMを組み合わせ、車両に一意IDを付与する4D Perceptionを実現。②Planning：DriveVLMやDriveWithLLMが鳥瞰図・センサ入力から「車線維持」「譲る」等の行動を生成。③Data Generation：拡散モデルを用いてレアシナリオの学習データを生成し、ロングテール問題に対処。④QAインタフェース：シーンに対して自然言語で問い合わせ可能なチャット型インタフェースの構築。

LLMを使う利点は、①常識推論（工事中の道路での暗黙ルール理解等）、②Few-shotによるレアシナリオへの汎化、③自然言語での意思決定の説明可能性、の3点に集約される。一方、課題はレイテンシ（リアルタイム制御に対するLLMの推論速度）とエッジデプロイ時のリソース制約である。

監査エージェント開発への示唆として、センサ入力→トークン化→Transformer→タスク別出力という構造は、非構造化データ（監査証跡ログ、財務文書）を複数モーダルで統合し、リスク判断を行う監査エージェントの設計パターンと類似する。特に「説明可能な意思決定」と「Few-shotによるレアケース対応」は、監査領域での異常検知エージェントに直接応用可能な概念である。

## アイデア

- LiDAR点群・RADAR点群・画像をすべて「トークン」として統一的に扱うことで、モーダル非依存なTransformerアーキテクチャをそのまま自動運転に転用できる点は、異種データ統合が必要な監査エージェント設計に示唆を与える
- Few-shot learningによるレアシナリオへの汎化：従来の自動運転では学習データが存在しないエッジケース（緊急車両、工事現場等）に対し、LLMの常識推論と少数例で対応できる可能性がある
- 拡散モデルによる合成データ生成でロングテール問題に対処するアプローチは、監査領域での不正事例（頻度が極めて低い）に対するデータ拡張戦略としても応用可能

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer Attention** (TODO: 読むべき)
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **Few-shot learning** → /deep_189 EmoTaG: 感情認識型トーキングヘッド合成 — 3D Gaussian Splattingとフューショット個人化の統合

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
