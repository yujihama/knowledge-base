---
title: "Car-GPT: LLMは自動運転車を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-11
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Planning, Perception, GPT-Driver, PromptTrack, 拡散モデル, マルチモーダル]
category: "ai-ml"
related: [3785, 4441, 3582, 4900, 1347]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-11T09:04:54.809283"
---

## 要約

本記事は、The Gradient掲載の2024年3月の解説記事で、大規模言語モデル（LLM）が自動運転の4つの基本モジュール（Perception・Localization・Planning・Control）をどのように代替・補完できるかを論じている。

自動運転の歴史的背景として、2010年代主流の「モジュラーアプローチ」（各機能を独立モジュールに分割）と、その後台頭した「End-to-End学習」（単一ニューラルネットワークで操舵・加速を直接予測）の2系統が紹介される。後者はブラックボックス問題を抱えており、LLMがその突破口になり得るという仮説が本稿の主軸である。

LLMの基礎として、トークン化（テキスト→数値変換）、Transformer（エンコーダ・デコーダ構造、Multi-head Attention）、次単語予測の仕組みが平易に説明される。自動運転への適用では、入力をカメラ画像・LiDAR点群・RADARデータなどに拡張し（Vision Transformerが対応）、出力を運転タスク（車線変更など）に変換するアーキテクチャが基本的な枠組みとして示される。

具体的な研究事例として以下が挙げられる：
- **Perception（知覚）**: GPT-4 Visionによる物体記述、HiLM-D・MTD-GPTによる動画対応検出、PromptTrack（DETRとLLMの組み合わせによるID付き追跡）
- **Planning（計画）**: DriveGPT4（多視点カメラ＋走行データでの行動説明生成）、GPT-Driver（GPT-3.5をmotion plannerとして転用、ベクトル化HD地図を入力）、DiMA（Mixtureモデルで複数シナリオのdiverseな軌跡生成）
- **Generation（データ生成）**: DrivingDiffusion・MagicDriveなどの拡散モデルによる合成訓練データ生成
- **Q&A・説明性**: NuScenesデータセット上の質疑応答、DriveLMによるグラフ構造VQA

LLMの自動運転への主な貢献として、（1）コモンセンス推論の活用、（2）説明可能なplanningの実現、（3）合成データによる訓練データ拡充、（4）マルチモーダル入力への対応が整理される。一方、リアルタイム処理要件（LLMの推論遅延との矛盾）、ハルシネーション、センサーフュージョンとの統合という課題も明示される。

監査エージェント開発への示唆：LLMを「説明可能な意思決定エンジン」として活用するアーキテクチャパターン（入力の構造化→LLM推論→行動出力）は、監査判断の根拠生成にも直接応用可能。特にGPT-Driverのように既存の構造化データ（HD地図→監査証跡）をLLMのコンテキストとして渡すアプローチは、ReActエージェントにおけるツール出力の解釈と同一のパターンである。

## アイデア

- GPT-Driverのアプローチ（GPT-3.5をmotion plannerとして転用し、構造化されたHD地図データをテキスト化してコンテキスト入力）は、LLMに構造化データを食わせて判断を生成するという手法であり、監査エージェントのルール解釈や証跡分析に直接応用できるパターン
- PromptTrackがDETR（既存の物体検出器）とLLMを組み合わせてID付き追跡を実現しているように、既存の専門モジュールとLLMを組み合わせるハイブリッド設計は、完全End-to-Endより実用性が高く、段階的な信頼性検証が可能
- DrivingDiffusionなどの拡散モデルによる合成訓練データ生成は、希少シナリオ（コーナーケース）のカバレッジ問題を解決する手法として、監査における異常パターンの合成生成にも転用できる可能性がある

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End learning** (TODO: 読むべき)
- **拡散モデル** → /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く

## 関連記事

- /deep_3785 遮蔽に強い3D人体メッシュ復元のための識別・生成シナジーフレームワーク
- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成

## 原文リンク

[Car-GPT: LLMは自動運転車を実現できるか？](https://thegradient.pub/car-gpt/)
