---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-28
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, Chain-of-Thought, GPT-4V, マルチモーダル]
category: "ai-ml"
related: [2219, 2789, 1527, 141, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-28T12:31:55.893359"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する研究動向を体系的に解説したサーベイ記事（The Gradient、2024年3月）。自動運転の従来アプローチとして、Perception・Localization・Planning・Controlの4モジュールに分割する「モジュラー型」と、単一ニューラルネットワークで入力から制御命令を直接予測する「End-to-End学習」を紹介し、これらに代わる第3の可能性としてLLMを位置づける。

LLMの基礎としてTokenization（テキストを数値トークン列に変換）とTransformerアーキテクチャ（Encoder-Decoder構造、Multi-head Attention、次単語予測）を説明した後、自動運転への応用方法を具体的に示す。入力として画像・LiDARpoint cloud・RADARデータをVision Transformerでトークン化し、既存Transformerブロックをほぼそのまま利用できる点が強調される。

研究活発な4領域を紹介する。①Perception：GPT-4 VisionやHiLM-D、MTD-GPTが画像から物体・レーン検出を行い、PromptTrackはDETRとLLMを組み合わせてオブジェクトへのID付与（追跡）を実現。②Planning：DriveLikeHuman（GPT-4ベース、長期・短期・反射的意思決定の3階層）、DriveVLM（VLMによるChain-of-Thought推論で走行軌跡を出力）、SurrealDriver（ドライバー行動をLLMでシミュレート）。③Data Generation：言語プロンプトで合成学習データ・コーナーケースシナリオを生成（ChatSim等、拡散モデルと組み合わせ）。④Q&A：DrivingWithLLMsはLLMにシーン説明を与えてドライバーへ自然言語で回答。

現状の課題として、①処理速度（LLMは高レイテンシでリアルタイム制御に不適）、②ハルシネーション（誤った物体認識・誤判断）、③センサーデータの入力フォーマット適合（LiDAR等の非テキストデータの効率的トークン化）、④大量の自動運転専用学習データ不足を挙げる。著者はLLMが単独で完全自動運転を実現するのは困難との見方を示しつつ、モジュラー型・End-to-End型を補完するハイブリッドな役割（特にPlanningとQ&A）に期待を寄せる。監査エージェント開発との示唆として、複数モジュールの判断をLLMがChain-of-Thoughtで統合するアーキテクチャは、監査における複数証拠の統合・説明生成プロセスと構造的に類似しており、DriveLikeHumanの3階層意思決定モデルはReActエージェントの階層化設計に参考になる。

## アイデア

- DriveLikeHumanの「長期・短期・反射的」3階層意思決定フレームワークは、LLMエージェントの階層型推論設計（戦略レイヤー／タクティカルレイヤー／即応レイヤー）として監査エージェントにも転用できる
- LiDARやRADARのpoint cloudをVision Transformerでトークン化してLLMに入力する手法は、非構造化センサーデータを既存LLMパイプラインに組み込む汎用的なパターンであり、監査証跡ログのトークン化にも応用可能
- ハルシネーション問題が安全クリティカルな自動運転で特に深刻であることは、LLM-as-judgeや監査AIで誤判断を防ぐための検証レイヤー（セカンドオピニオンエージェント等）の必要性を裏付ける

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **LiDARトークン化** (TODO: 読むべき)
- **Chain-of-Thought推論** (TODO: 読むべき)

## 関連記事

- /deep_2219 テキストからモデルへの変換を支援するLLMコパイロット：Text2ModelとText2Zinc
- /deep_2789 VRAG-DFD: MLLMベースのディープフェイク検出のための検証可能な検索拡張
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_141 Hugging Faceにおけるオープンソースの現状：2026年春
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
