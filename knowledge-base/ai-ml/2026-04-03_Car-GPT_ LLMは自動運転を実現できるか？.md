---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-03
tags: [LLM, 自動運転, Vision Transformer, Perception, Planning, End-to-End学習, DriveLM, DriveVLM, Chain-of-Thought, 拡散モデル]
category: "ai-ml"
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-03T21:06:10.184973"
---

## 要約

本記事はThe Gradientに掲載された自動運転×LLMの技術解説記事（2024年3月）。自動運転の従来アプローチであるモジュール式（Perception・Localization・Planning・Controlの4モジュール分離）とEnd-to-End学習の限界を整理した上で、LLMが第三の解法になり得るかを論じている。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造のTransformerアーキテクチャ、Next-Word Predictionによる出力生成の3点を解説。自動運転への適用では、入力をカメラ画像・LiDARポイントクラウド・RADARデータなどに置き換え、Vision Transformerで同様にトークン化できる点を強調する。

2023年時点の主要研究領域は4つ：①Perception（画像からの環境記述・物体検出・追跡）、②Planning（Bird-Eye-Viewや知覚出力からの行動決定）、③Generation（拡散モデルを用いた訓練データ・シナリオ生成）、④Q&A（シナリオへの自然言語問答）。

Perceptionでは、GPT-4 Visionによる物体記述、HiLM-DやMTD-GPTによる動画対応、PromptTrack（DETRとLLMの組み合わせによるオブジェクトID付き追跡）などが紹介される。Planningでは、DriveLM（シーングラフ＋LLMによる視覚的Q&A駆動のプランニング）、DriveVLM（Chain-of-Thought推論で走行シーンを段階的に解析）が登場。Generationでは拡散モデルによる合成データ生成でロングテールシナリオをカバーする手法が示される。

LLMの自動運転への利点として、①少数サンプルでの汎化（Few-shot learning）、②自然言語による行動説明でブラックボックス問題を緩和、③複雑な交通ルール・常識の事前知識の活用が挙げられる。一方、リアルタイム推論の速度制約、幻覚（Hallucination）による誤判断リスク、センサーデータへの適用限界が課題として残る。記事全体を通じ、LLMは単体の解法というよりモジュール式とEnd-to-Endを補完するハイブリッド要素として機能する可能性が示唆されている。

## アイデア

- PromptTrackのようにDETR等の既存検出器とLLMを組み合わせ、オブジェクトIDの一貫した追跡を実現するアーキテクチャは、複数エージェントが同一エンティティを参照する監査エージェント設計に転用できる
- DriveLMのシーングラフ＋Q&A駆動のPlanningは、LLMに『なぜその行動を取るか』を自然言語で説明させる手法であり、監査証跡の自動生成・説明可能なエージェント判断に直結する
- 拡散モデルによるロングテールシナリオ生成は、実データが少ない監査異常ケースの合成データ拡張に応用できる可能性がある
## 関連記事

- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成
- /deep_558 ReproMIA：プロアクティブなメンバーシップ推論攻撃のためのモデルリプログラミング包括分析
- /deep_1252 DSPyによる宣言的学習を用いたLLMプロンプトエンジニアリングの最適化
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
