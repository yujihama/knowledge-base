---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-02
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, GPT-4 Vision, GAIA-1, PromptTrack, DriveGPT4]
category: "ai-ml"
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-02T21:09:29.373150"
---

## 要約

本記事はThe Gradient誌（2024年3月）に掲載された解説記事で、LLM（大規模言語モデル）が自動運転の4大要素（Perception・Localization・Planning・Control）にどう応用されるかを概観する。従来の自動運転ソフトウェアはモジュール型アーキテクチャが主流だったが、2010年代後半からEnd-to-End学習が注目され、単一ニューラルネットワークでステアリングと加速を予測する手法が台頭した。LLMの基礎としてTokenization（テキストを数値列に変換）・Transformerアーキテクチャ（Encoder-Decoder構造、Multi-head Attention）・次単語予測タスクを解説し、これらを自動運転に適用する際の変更点を整理する。入力は画像・LiDARポイントクラウド・RADARデータなどに置き換えられ、Vision Transformer（ViT）や Video Vision Transformerによりトークン化が可能。出力は状況説明や車線変更などのドライビングタスクに変更される。具体的なLLM応用研究として、Perceptionでは GPT-4 Visionによる物体認識・HiLM-D・MTD-GPT・PromptTrack（DETR+LLMでオブジェクトID追跡）が紹介される。Planningでは DriveGPT4・GPT-Driver（GPT-4をゼロショットで使用し0.44mの平均変位誤差）・DiMA（Driveの模倣学習アーキテクチャ）・SurrealDriver（ドライバーペルソナを設定するLLMプランナー）などが挙げられる。生成タスクでは拡散モデルを使ったトレーニングデータ生成・シナリオ拡張が可能で、GAIA-1（Wayveが開発した900万パラメータの世界モデル）が現実的な走行シナリオを動画生成する。QAインターフェースとしてDriveVLM・NuScenes-QA・Dolphins等が対話型シナリオ解析を実現する。課題としては、センサーデータの完全な言語モデル化・リアルタイム推論の計算コスト・安全性保証・エッジケース対応の困難さが指摘される。記事全体としてはLLMの自動運転応用を教育的観点から網羅しており、2023年時点の研究状況を俯瞰するサーベイとしての価値がある。

## アイデア

- GPT-Driverがゼロショット（追加学習なし）でGPT-4を使い平均変位誤差0.44mを達成している点は、既存の大規模モデルをプロンプト設計だけで専門タスクに転用できることを示す事例として注目に値する
- GAIA-1（900万パラメータ）が走行シナリオの動画を生成する世界モデルとして機能する点は、合成データによるトレーニングデータ拡張のアプローチとして、データ不足問題への対処策になり得る
- PromptTrackがDETR（既存の物体検出器）とLLMを組み合わせてオブジェクトIDの一貫追跡を実現している構造は、既存の専門モジュールとLLMをハイブリッドで組み合わせるアーキテクチャパターンの典型例

## Yujiの取り組みへの示唆

自動運転へのLLM適用における「モジュール型 vs End-to-End」の設計トレードオフは、監査エージェントの設計において個別検証モジュール（証憑照合・リスク評価等）をLangGraphのノードとして分離するか、単一LLMで処理するかの判断に直接対応する。GPT-DriverのゼロショットアプローチはGPT-4をPydanticで型付けした出力スキーマと組み合わせ、監査判断タスクにプロンプトエンジニアリングのみで適用する可能性を示唆する。ただし本記事は2024年初頭の解説記事であり、最新の研究成果を追うにはHiLM-D・GPT-Driverの原著論文にあたることを推奨する。

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
