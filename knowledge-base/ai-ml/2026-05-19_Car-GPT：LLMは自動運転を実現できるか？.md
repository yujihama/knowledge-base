---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-19
tags: [LLM, 自動運転, Vision Transformer, マルチモーダル, Planning, End-to-End学習, GPT-4V, PromptTrack, DriveLM, 拡散モデル]
category: "ai-ml"
related: [3785, 4441, 3582, 4900, 1347]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-19T21:16:58.561919"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する研究動向を解説した入門的サーベイ。自動運転の従来アーキテクチャである「モジュール型（Perception→Localization→Planning→Control）」とEnd-to-Endニューラルネットワークの限界を整理した上で、LLMがその解決策になり得るかを考察している。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造を持つTransformerアーキテクチャ、および次トークン予測タスクを簡潔に説明。GPTのような純粋Decoderベースモデルとの違いにも触れている。

自動運転へのLLM適用は、入力をマルチモーダル（画像・LiDARポイントクラウド・RADAR等）に拡張し、Vision Transformerでトークン化することで実現する。研究が活発な領域は主に4つ：①Perception（シーン記述・物体検出・追跡）、②Planning（行動決定）、③生成（拡散モデルによるトレーニングデータ生成）、④Q&A（チャットインターフェース）。

Perceptionでは、GPT-4 Visionが画像内オブジェクトを記述できることを示し、HiLM-DやMTD-GPTなどのマルチビュー対応モデル、PromptTrack（DETRとLLMを組み合わせオブジェクトにユニークIDを付与）を紹介。PlanningではVAD（Vectorized Scene Representation）やDriveVLM、GPT-Driverなどが自然言語で運転判断を出力するアプローチを採用。Q&A系ではDriveLMがグラフ構造のVQAを構築し、因果関係を持つ推論チェーンを形成する。

データ生成では拡散モデル（MagicDrive等）を使い、LiDARや画像のシミュレーションデータを生成してトレーニングデータを補強する手法が紹介されている。

LLMの自動運転への利点として、①コモンセンス推論（「濡れた道→スリップリスク」のような論理）、②言語による説明可能性、③ゼロショット・フューショット汎化能力が挙げられる。一方で課題も明確で、LLMの推論レイテンシは自動運転の要求（数十ms以下）に対して著しく遅く、リアルタイム性が最大のボトルネックとなっている。また、ハルシネーションや信頼性の問題も未解決である。

記事全体としては入門記事の色が強く、研究論文の深い実験結果より概念紹介に重点が置かれているが、2023〜2024年時点の研究エコシステムのマッピングとして有用。監査エージェント開発への直接的な示唆は薄いが、マルチモーダルトークン化とPlanning段階へのLLM導入という設計パターンは、センサーデータや財務データを扱うエージェント設計の参考になる。

## アイデア

- LLMのコモンセンス推論能力（例：濡れた道→スリップリスクの因果連鎖）をPlanning層に組み込むことで、ルールベースでは記述困難なロングテールシナリオに対応できる点は、監査エージェントの例外ケース処理にも応用可能
- DriveLMのグラフ構造VQA（因果関係を持つQ&Aチェーン）は、エージェントの判断根拠を自然言語で説明可能にする設計パターンとして、LLM-as-judgeやReActエージェントの説明可能性向上に転用できる
- LiDARポイントクラウドや画像などの異種センサーデータをVision Transformerでトークン化して同一LLMに入力する統一アーキテクチャは、財務データ・ログ・テキストレポートなど異種データを扱う監査エージェントのマルチモーダル入力設計の参考になる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開
- **拡散モデル** → /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 関連記事

- /deep_3785 遮蔽に強い3D人体メッシュ復元のための識別・生成シナジーフレームワーク
- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
