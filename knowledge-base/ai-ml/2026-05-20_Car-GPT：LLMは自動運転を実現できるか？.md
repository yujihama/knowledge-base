---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-20
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, DriveGPT4, PromptTrack, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-20T09:30:08.519577"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する可能性を整理した解説記事（2024年3月）。自動運転の従来アーキテクチャとLLMの基礎を説明した上で、知覚・計画・生成・Q&Aの4領域でLLMがどう活用されているかを紹介する。

従来の自動運転システムは「モジュラー型」（Perception→Localization→Planning→Control）で構成されていたが、近年はEnd-to-End学習（単一ニューラルネットワークが操舵・加速を直接予測）が注目されている。LLMはその第三の選択肢として期待される。

LLMの基礎として、テキストをトークン（数値）に変換するTokenizationと、Encoder-Decoder構造を持つTransformerアーキテクチャ（Multi-head Attention等）、そして次トークン予測タスクが解説される。Vision Transformerにより画像・LiDAR点群・RADARデータも同様にトークン化可能であり、入力の種類に依らずTransformerブロックをそのまま適用できる点が自動運転への転用を容易にする。

知覚（Perception）領域では、GPT-4 Visionが画像から物体・車線を検出・記述できることが示されており、HiLM-D、MTD-GPT、PromptTrack（DETRとLLMの組み合わせ、追跡IDの割り当てが可能）などの専用モデルも登場している。計画（Planning）領域では、DriveGPT4やDriveVLMがマルチビュー画像やBird-Eye Viewを入力に、車線変更・停止などの行動決定を言語で説明しながら出力する。また、DriveLLMやGPT-Driver（GPT-4をwaypoint予測器として使用）も開発されている。生成（Generation）領域では、拡散モデルを用いた学習データ生成・シナリオ拡張が可能であり、データ不足の問題を補う手段として活用される。Q&A領域では、LingoQAなどがシナリオに関する質問応答を実現している。

課題としては、LLMの推論速度（リアルタイム制御への適用困難）、ハルシネーション（誤認識）、センサーデータとの統合の複雑さが挙げられる。現時点では完全自律走行の実現には至っていないが、知覚の説明可能性向上や複雑シナリオでの判断支援において実用的な貢献が見込まれる。監査エージェント開発への示唆として、LLMを意思決定の「説明生成モジュール」として組み込む設計思想（行動＋理由を同時出力）は、監査ログの自動説明生成や異常検知の根拠説明に直接応用可能である。

## アイデア

- LLMを自動運転の計画モジュールとして使い、行動決定と同時にその理由を自然言語で出力させる設計は、監査エージェントの判断根拠説明生成に直接転用できる
- PromptTrackがDETR（物体検出器）とLLMを組み合わせてトラッキングIDを言語モデルに統合した設計は、構造化データと非構造化推論を橋渡しするエージェント設計パターンとして参考になる
- 拡散モデルを用いたシナリオ生成による学習データ拡張は、監査データが少ない領域でのエージェント訓練データ生成戦略としても応用可能

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
