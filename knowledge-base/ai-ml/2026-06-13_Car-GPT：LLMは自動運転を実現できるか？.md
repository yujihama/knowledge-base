---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-13
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, PromptTrack, DriveGPT, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 7556, 1527]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-13T09:27:56.010692"
---

## 要約

本記事は、Large Language Model（LLM）を自動運転に応用する研究動向を2024年時点で俯瞰した解説記事である。自動運転の従来アーキテクチャは「モジュール型」（Perception・Localization・Planning・Controlの4段階）と「End-to-End学習」（単一ニューラルネットワークで操舵・加速を予測）の2系統に分類される。LLMはこれらに対して第三の選択肢として台頭しつつある。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造を持つTransformer、そしてNext-Word Predictionによる出力生成の3要素を説明する。自動運転への適用では、入力を画像・LiDARポイントクラウド・RADARデータ等に拡張し（Vision Transformerと同様のアプローチ）、出力を車線変更等の運転タスクに変換する。

研究が活発な応用領域は4つ：（1）Perception：GPT-4 Visionによる物体記述、HiLM-DやMTD-GPTによる動画対応検出、PromptTrackによるDETRとLLMの組み合わせでのオブジェクトトラッキング（一意ID割り当て）。（2）Planning：DriveGPTやDriveVLMによる鳥瞰図ベースの行動計画生成。（3）Generation：Diffusionモデルを活用したトレーニングデータ・シナリオ生成（データ不足問題への対応）。（4）Q&A：チャットインターフェースによるシナリオへの質問応答。

LLMを自動運転に導入する利点として、（a）センサ融合の柔軟性（カメラ・LiDAR・RADARをトークンとして統一処理）、（b）常識推論能力（標識の文字を読んで判断するなど、従来手法が苦手としていた行動）、（c）Emergent Ability（訓練データに含まれない事象への汎化）が挙げられる。一方の課題は、（a）ハルシネーション（誤情報生成のリスク）、（b）処理速度（自動運転の30fps以上の要求に対し現状のLLMは遅延大）、（c）解釈可能性（ブラックボックス問題）、（d）大量の学習データ要求である。記事はLLMが即座の解決策ではなく、既存モジュール型・E2Eアプローチを補完する存在として現実的に位置づけている。監査エージェント開発への示唆として、LLMが「常識的な判断」と「既存手法の補完」を担う設計パターンは、ルールベースの監査チェックにLLM推論を組み合わせるハイブリッド構成と直接対応する。

## アイデア

- テキスト・画像・LiDARをすべて「トークン」として統一処理するアーキテクチャは、異種センサ融合の複雑さをTransformerの汎用性で吸収する設計思想であり、監査エージェントにおける異種データ（財務数値・テキスト・ログ）の統一処理にも転用できる
- PromptTrackのようにDERT（特化型検出器）とLLM（汎用推論器）を組み合わせるハイブリッド設計は、精度とコンテキスト理解を両立する実用的パターンであり、単一モデルに全責任を負わせない分担設計の好例
- Diffusionによるシナリオ生成（稀少事例のデータ拡張）は自動運転固有の課題（エッジケースの訓練データ不足）への対処だが、監査AIにおける不正事例の少なさという同じ問題にも適用可能な発想

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークナイゼーション** → /deep_2269 VideoFlexTok：粗から細へのコース・トゥ・ファイン動画トークナイゼーション
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_7556 マニュアル動画生成AI「MANAVO」開発ログ①：プロダクト構想と課題の背景
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
