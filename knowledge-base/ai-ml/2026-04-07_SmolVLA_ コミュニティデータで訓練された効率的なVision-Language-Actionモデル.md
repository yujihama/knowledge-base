---
title: "SmolVLA: コミュニティデータで訓練された効率的なVision-Language-Actionモデル"
url: "https://huggingface.co/blog/smolvla"
date: 2026-04-07
tags: [VLA, Vision-Language-Action, SmolVLM2, Flow-Matching, LeRobot, ロボティクス, 非同期推論, action-chunk, SmolLM2, SigLIP]
category: "ai-ml"
memo: "[HF Blog] SmolVLA: Efficient Vision-Language-Action Model trained on Lerobot Community Data"
processed_at: "2026-04-07T21:03:12.423456"
---

## 要約

SmolVLAは、HuggingFaceが発表した450Mパラメータのオープンソースなロボティクス向けVision-Language-Action（VLA）モデル。消費者向けハードウェアで動作・訓練可能な点が特徴。

**アーキテクチャ**: VLMバックボーンにSmolVLM2（SigLIPビジョンエンコーダ＋SmolLM2言語デコーダ）を採用。RGBカメラ画像・自然言語命令・センサーモーター状態をトークン化して統合し、約100Mパラメータのアクションエキスパート（Flow Matching Transformer）が将来の行動シーケンス（action chunk）を生成する。

**効率化の設計**: (1)ビジョンモデルのレイヤーを半分スキップして推論高速化、(2)自己注意とクロスアテンションのインターリーブ、(3)視覚トークン削減、(4)非同期推論スタックの導入（推論と行動実行を分離）。非同期推論により応答速度30%向上・タスクスループット2倍を達成。

**訓練データ**: LeRobotタグの付いたコミュニティ公開データセットのみを使用。訓練エピソード数は3万件未満で、他のVLAモデルより1桁少ない。データの前処理として、タスクアノテーションの改善とカメラビューの標準化を実施。

**性能**: シミュレーション（LIBERO、Meta-World）および実機タスク（SO100、SO101ロボットアーム）において、ACTなどの強力なベースラインや大規模VLAモデルを上回る結果を示した。CPU・単一GPU・MacBook上での動作も可能。

**訓練手法**: LLMの訓練パラダイムを参考に、汎用マニピュレーションデータによる事前学習とタスク特化のファインチューニングの2段階構成を採用。LeRobotフレームワーク経由でファインチューニングが容易。

モデル重み・訓練コード・推論レシピが全公開されており、SO-100/SO-101等の低価格ハードウェアでのデプロイも想定している。

## アイデア

- Flow Matching TransformerをAction Expertとして使う設計：離散トークン化ではなく連続行動空間に対してflow matchingを適用することで、高精度な行動チャンク生成とサンプリング効率を両立している点が技術的に興味深い
- 非同期推論スタック：VLMの推論ループとロボットの行動実行ループを分離することで、遅延を隠蔽しつつスループットを2倍にする設計は、リアルタイムエージェントシステム全般に応用可能なアーキテクチャパターン
- LLMの2段階訓練パラダイム（事前学習＋タスク特化ファインチューニング）をロボティクスポリシーに適用：データ量が1桁少なくても大規模モデルを上回る汎化性能を達成しており、少量データでのエージェント訓練戦略として参照価値がある
## 関連記事

- /deep_143 LeRobot v0.5.0: あらゆる次元でのスケーリング
- /deep_154 ロボティクスAIを組み込みプラットフォームへ展開：データセット収録・VLAファインチューニング・オンデバイス最適化
- /deep_651 LeRobotコミュニティデータセット：ロボティクスの「ImageNet」はいつ、どのように実現するか
- /deep_413 AMD オープンロボティクスハッカソン参加募集
- /deep_1651 多様性考慮型レッドチーミングによるVision-Language-Actionモデルの言語的脆弱性の発見

## 原文リンク

[SmolVLA: コミュニティデータで訓練された効率的なVision-Language-Actionモデル](https://huggingface.co/blog/smolvla)
