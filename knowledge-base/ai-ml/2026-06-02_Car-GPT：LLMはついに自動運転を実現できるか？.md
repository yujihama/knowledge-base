---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-02
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, DriveGPT4, PromptTrack, マルチモーダル]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-02T09:23:58.479991"
---

## 要約

自動運転は2010年代から「モジュラーアプローチ」（Perception・Localization・Planning・Controlの4モジュール分離）が主流だったが、依然として完全自律走行は実現していない。本記事はLLM（大規模言語モデル）を自動運転に適用する研究動向を整理したサーベイ記事である。

LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造を持つTransformerアーキテクチャ、そして次トークン予測による出力生成の3要素を解説する。自動運転への適用にあたっては、入力を画像・LiDARポイントクラウド・RADARデータに拡張し（Vision Transformerが担う）、出力を「レーン変更」等のドライビングタスクに置き換えることで、同一のTransformer構造を転用できる。

Perception領域では、GPT-4 Visionによる物体認識、HiLM-DやMTD-GPTによる動画対応検出、PromptTrack（DETRとLLMの統合による固有IDトラッキング）などが活発に研究されている。Planning領域では、DriveGPT4やDriveVLMが鳥瞰図や前方画像からの行動計画生成を実現。データ生成領域では拡散モデルと組み合わせた合成シナリオ生成が研究されている。

End-to-End学習との統合も重要なテーマで、UniADやVADといったモデルがPerceptionからPlanningまでを単一ネットワークで結合しようとしている。しかしLLM適用には課題も多く、①リアルタイム推論の計算コスト、②自然言語出力から物理制御コマンドへの変換精度、③高精度地図データへの依存、④レアシナリオへの汎化性能が未解決問題として残る。

監査エージェント開発への示唆としては、自動運転の「モジュラー→E2E」転換は、監査プロセスの各ステップ（データ収集・異常検知・判断・レポート生成）を分離したパイプラインから、LLMベースの統合エージェントへの移行と構造的に類似している。複数モダリティ（数値・テキスト・ログ）を単一Transformerで処理しPlanning出力を得る設計は、監査エージェントのマルチモーダル入力対応に直接応用可能。PromptTrackのように既存の特化型モデル（異常検知器）とLLMを組み合わせるハイブリッドアーキテクチャも参考になる。

## アイデア

- 自動運転の4モジュール（Perception・Localization・Planning・Control）をLLMで統合するアプローチは、監査エージェントの各フェーズ統合と同型問題であり、設計パターンを直接借用できる
- PromptTrackのようにDETR等の特化モデルをEncoderとして使いLLMをDecoderに接続するハイブリッド構成は、既存の異常検知モデル資産を活かしつつLLMの推論能力を加える監査システム設計に応用可能
- 自然言語でのPlanning出力（「右車線に変更すべき理由」）はブラックボックス問題を緩和する説明可能性を持ち、監査における判断根拠の自動文書化に直結する

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Encoder-Decoder** → /deep_317 回帰言語モデル（RLM）による大規模システムのシミュレーション
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ
- **拡散モデル** → /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
