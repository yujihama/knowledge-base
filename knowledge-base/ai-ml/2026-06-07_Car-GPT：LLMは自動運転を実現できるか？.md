---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-07
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, マルチモーダル, DriveGPT4, PromptTrack]
category: "ai-ml"
related: [4441, 3582, 4900, 7556, 1527]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-07T21:30:05.965026"
---

## 要約

本記事は、自動運転へのLLM適用可能性を解説した入門的技術解説記事（The Gradient, 2024年3月）。自動運転の従来アーキテクチャである「モジュラー型」（Perception・Localization・Planning・Controlの4分割）と「End-to-End学習」の限界を整理した上で、LLMがその突破口になり得るかを論じる。

LLMの基礎としてTokenization（テキストを数値に変換）とTransformerのEncoder-Decoder構造、Next-Word Predictionを説明。自動運転への適用では、入力をカメラ画像・LiDARポイントクラウド・RADARデータ等のマルチモーダルトークンに変換し、Vision Transformerと同様の処理で扱うことが可能とされる。

2023年の主要研究領域として以下4つを挙げる。①Perception：HiLM-D、MTD-GPT、PromptTrack（DETR+LLMでオブジェクトにユニークIDを付与）などが画像入力から物体・車線を検出。②Planning：DriveGPT4（GPT-4V使用）やDriveLM（シーングラフ構築後にQ&Aで行動判断）が鳥瞰図や知覚出力から次の操作（車線変更等）を生成。③データ生成：拡散モデルを用いた訓練データ・代替シナリオの合成。④Q&A：自然言語でシナリオに質問応答するチャットインターフェース。

実用上の課題として、①計算コスト（LLMのリアルタイム推論は高負荷）、②外挿能力（未経験シナリオへの対応不確実性）、③LiDAR等センサーとのマルチモーダル統合の難しさを挙げる。一方で、人間のフィードバックや自然言語での説明可能性（ブラックボックス問題の緩和）においてLLMの優位性を評価している。

監査エージェント開発への示唆：複数モジュールを単一LLMで統合するEnd-to-Endアプローチは、監査プロセス（データ収集・リスク判定・報告生成）の統合エージェント設計と構造的に類似する。PromptTrackのように外部検出器（ルールエンジン等）とLLMを組み合わせるハイブリッド構成は、監査エージェントにおける説明可能性と精度の両立に応用できる視点を提供する。

## アイデア

- 自動運転の4モジュール（Perception/Localization/Planning/Control）をLLMで統合するEnd-to-Endアプローチは、監査エージェントの複数フェーズ統合設計に直接応用可能な構造的類比を持つ
- PromptTrackのようにDETRなど専門検出器とLLMを組み合わせるハイブリッド設計は、ルールベース監査チェックとLLM推論を組み合わせるReActエージェントの設計指針として参考になる
- DriveLMのシーングラフ+Q&A方式は、複雑な状況を構造化した上でLLMに意思決定させるアプローチであり、監査シナリオの知識グラフ化とLLM-as-judgeの組み合わせと対応する

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **LiDARポイントクラウド** (TODO: 読むべき)
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_7556 マニュアル動画生成AI「MANAVO」開発ログ①：プロダクト構想と課題の背景
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
