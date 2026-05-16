---
title: "判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク"
url: "https://tldr.takara.ai/p/2604.27366"
date: 2026-05-08
tags: [VLA, CriticVLA, 自動運転, Bench2Drive, 軌跡最適化, マルチモーダル, クローズドループ評価, 合成データセット]
category: "ai-ml"
related: [3582, 1117, 2375, 1297, 3256]
memo: "[HF Daily Papers] Judge, Then Drive: A Critic-Centric Vision Language Action Framework for Autonomous Driving"
processed_at: "2026-05-08T12:45:25.711613"
---

## 要約

VLA（Vision Language Action）モデルは、カメラ映像・LiDAR・テキスト指示などのマルチモーダル入力を直接制御信号にマッピングする手法として自動運転分野で注目されている。しかし既存のVLAベース手法は、LLMベースの他分野（コード生成・数学推論など）で有効性が実証されているCritic（批評者）能力を自動運転の意思決定改善に明示的に活用していなかった。この欠如が、複雑なクローズドループシナリオでの性能限界を招いていた。

本論文ではCriticVLAという2段階フレームワークを提案する。第1段階でVLAが粗い走行軌跡（rough trajectory）を生成し、第2段階でVLAベースのCriticがその軌跡をマルチモーダル評価（視覚・言語・走行コンテキストを統合）し、1ステップ最適化によって軌跡を洗練する。Criticは単なる報酬スコアではなく、なぜその軌跡が不適切かを評価・理由付けした上でより安全な軌跡へと修正を行う点が特徴的である。

このCritic訓練を支えるために、多様な走行シナリオをカバーする1,290万件のアノテーション済み軌跡データセットを合成構築した。各サンプルには「軌跡候補」「その評価根拠」「改善後軌跡」が含まれており、CriticのReasoning能力と軌跡Refinement能力を同時に強化する設計になっている。

評価はBench2Driveベンチマーク（NuScenesベースのクローズドループ自動運転評価環境）を用いて実施。CriticVLAは総合成功率73.33%を達成し、困難なシナリオでは既存最先端手法に対して約30%の改善を実現した。特に交差点・歩行者回避・緊急停止などの複雑場面で顕著な改善が見られた。

監査エージェント開発への示唆として、「粗い判断→Criticによる再評価→最終判断」という2段階推論パターンは、LangGraphの多段階ノード設計と親和性が高い。監査判断においても、初期リスク評価をCriticエージェントが見直す構造を採用することで、複雑なリスクシナリオへの対応精度向上が期待できる。

## アイデア

- VLAのCritic能力を自動運転の軌跡Refinementに特化させる2段階アーキテクチャは、Actor-Criticの強化学習的発想をVLA推論時に応用した点が新しい
- 1,290万件の合成アノテーション済み軌跡データセットを構築することでCriticの推論訓練を可能にした手法は、データ設計自体がアーキテクチャの一部として機能している
- 「粗い軌跡を生成してからCriticで1ステップ最適化」というパターンは、自動運転以外のエージェント系タスク（コードレビュー、監査判断）にも転用可能な汎用的な設計原理を示唆する

## 前提知識

- **VLA (Vision Language Action)** (TODO: 読むべき)
- **クローズドループ評価** → /deep_765 AutoMIA: エージェント的自己探索による会員推論攻撃の改善ベースライン
- **Bench2Drive** (TODO: 読むべき)
- **Actor-Critic** → /deep_1618 Advantage Actor Critic（A2C）：アクター・クリティックによる方策勾配の分散低減
- **軌跡最適化** (TODO: 読むべき)

## 関連記事

- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_1117 WebSightデータセット：スクリーンショットからHTMLコードへの変換を実現する大規模合成データセット
- /deep_2375 VLAジャンプスタート強化学習（VLAJS）：Vision-Language-ActionモデルによるRLの探索効率化
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_3256 Gemma 4 VLAデモ：Jetson Orin Nano Super上でのローカル実行

## 原文リンク

[判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク](https://tldr.takara.ai/p/2604.27366)
