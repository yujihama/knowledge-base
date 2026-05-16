---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-11
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, マルチモーダル, Perception, Planning, 拡散モデル, PromptTrack, DETR]
category: "ai-ml"
related: [3785, 4441, 3582, 4900, 1347]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-11T21:51:09.086090"
---

## 要約

本記事は、The Gradientに2024年3月掲載された解説記事で、LLM（大規模言語モデル）を自動運転に応用する研究動向を体系的に整理している。

自動運転の歴史的アプローチとして、まず「モジュール型」（Perception・Localization・Planning・Controlの4モジュールを独立設計）と、それに続く「End-to-End学習」（単一ニューラルネットワークで操舵・加速度を直接予測するが、ブラックボックス問題を内包）の2軸を説明する。その上で、LLMがこれらの限界を超える「第三の道」となりうるかを検討している。

LLMの基礎として、トークン化（テキスト→数値変換）、Transformerアーキテクチャ（Encoder-Decoderまたはデコーダ専用構成）、next-word predictionの仕組みを概説。自動運転への適用では、画像・LiDARポイントクラウド・RADARデータもVision TransformerやVideo Vision Transformerによってトークン化可能なため、同じTransformerバックボーンを転用できると論じる。

具体的な研究事例として以下が紹介される：
- **Perception**：GPT-4Vによる物体検出・シーン記述、HiLM-D、MTD-GPT（動画対応）、PromptTrack（DETRとLLMを組み合わせたID付き物体追跡）
- **Planning**：DriveVLM・DriveLLM（鳥瞰図から車線変更等の行動を生成）、DiMA（マルチエージェント間の意図共有）、LMDrive（センサー入力を言語コマンドに変換しCarlaシミュレータで検証）
- **Data Generation**：WoVogen・BEVGen（拡散モデルで走行シナリオを生成、エッジケースのデータ拡張に活用）
- **Q&A**：DriveChatGPT・MAPLM（チャット形式で走行状況を問い合わせ可能なインターフェース）

記事はLLMの自動運転適用における課題として、リアルタイム性（推論レイテンシ）、センサーデータの高次元性、安全保証の難しさを挙げつつ、ペニシリンの偶発的発見に喩えながら「LLMが予期せぬブレークスルーになりうる」という楽観的見解で締めくくる。監査エージェント開発への示唆としては、マルチモーダルトークン化とPlanning段階でのLLM活用パターン（状況認識→行動選択）がReActエージェントの設計と構造的に類似しており、センサー入力を監査証跡・ログに置き換えることで参照可能なアーキテクチャパターンを示している。

## アイデア

- LiDARやRADARのポイントクラウドをトークン化してTransformerに入力する発想は、監査ログや構造化データをトークン列として扱いLLMで異常検知するアーキテクチャに直接転用できる
- DiMAのようなマルチエージェント間で意図（Intention）を言語として共有する設計は、LangGraphベースの監査エージェントにおける複数エージェント間のコンテキスト受け渡しパターンとして参考になる
- WoVogenのようなエッジケースシナリオの自動生成（拡散モデル活用）は、監査エージェントのテストデータ生成（異常取引シナリオの合成）に応用可能

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **拡散モデル** → /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 関連記事

- /deep_3785 遮蔽に強い3D人体メッシュ復元のための識別・生成シナジーフレームワーク
- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
