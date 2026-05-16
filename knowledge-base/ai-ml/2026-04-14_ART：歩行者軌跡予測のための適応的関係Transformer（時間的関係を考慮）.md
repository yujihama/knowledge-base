---
title: "ART：歩行者軌跡予測のための適応的関係Transformer（時間的関係を考慮）"
url: "https://tldr.takara.ai/p/2604.03649"
date: 2026-04-14
tags: [Transformer, 軌跡予測, グラフニューラルネットワーク, 歩行者行動モデル, マルチエージェント相互作用, Attention Pruning, ETH/UCY]
category: "ai-ml"
related: [1494, 113, 216, 1482, 370]
memo: "[HF Daily Papers] ART: Adaptive Relational Transformer for Pedestrian Trajectory Prediction with Temporal-Aware Relations"
processed_at: "2026-04-14T12:26:52.783362"
---

## 要約

歩行者の軌跡予測は、自律ロボットや自動運転など多様な応用において重要な課題である。従来手法はグラフベースまたはTransformerベースのフレームワークを採用しているが、グラフベース手法は計算コストが高く、Transformerベース手法は人間のインタラクションが時間とともに変化する「時変性」と「多様性」を十分に表現できないという課題がある。本研究では、これらの問題を同時に解決するAdaptive Relational Transformer（ART）を提案する。

ARTの核心は2つのコンポーネントにある。第一は「Temporal-Aware Relation Graph（TARG）」で、歩行者ペア間のインタラクションの時間的な変化を明示的にモデル化する。静的なグラフではなく、時刻ごとにインタラクションの強度や種類が変わることを考慮した動的グラフ表現を採用し、例えば「すれ違い」「並走」「追従」などの異なる社会的関係を区別してエンコードする。第二は「Adaptive Interaction Pruning（AIP）」機構で、全ペア間の関係を計算する際に生じる冗長な計算を動的に削減する。重要度の低いインタラクションをプルーニングすることで、精度を保ちながら計算効率を向上させる。

評価は標準的なベンチマークであるETH/UCY（実世界の歩行者データセット）およびNBAデータセット（スポーツ選手の動作予測）で実施し、ARTは最先端（state-of-the-art）の予測精度と高い計算効率を両立していることを示している。特にNBAデータセットでの評価は、密集した複雑なインタラクションに対する汎化性能を示す点で注目に値する。

監査エージェント開発への示唆としては、エージェントシステム内の複数エージェント間の相互作用モデリングに応用可能な点が挙げられる。TARGのように時間的に変化するエージェント間の依存関係を動的グラフで表現し、AIPのように重要度の低い関係を刈り込む設計は、マルチエージェント環境でのリソース効率の高い情報共有アーキテクチャの設計指針として参考になる。

## アイデア

- 静的グラフではなく時変グラフ（TARG）でインタラクションの動的変化を表現する設計は、時系列データにおけるグラフ構造学習の汎用的アプローチとして応用範囲が広い
- Adaptive Interaction Pruning（AIP）によるスパース化は、全対全（O(n²)）の関係計算を動的に削減するアイデアで、大規模マルチエージェントシステムのスケーラビリティ問題に対する解決策として参考になる
- ETH/UCYとNBAという性質の異なる2種のベンチマークで評価することで、密集インタラクション環境への汎化性能を示す検証設計が堅実

## 前提知識

- **Transformer (Self-Attention)** (TODO: 読むべき)
- **Graph Neural Network** → /deep_311 リレーショナルデータのためのグラフ基盤モデル
- **軌跡予測 (Trajectory Prediction)** (TODO: 読むべき)
- **Social Force Model** (TODO: 読むべき)
- **Attention Pruning** (TODO: 読むべき)

## 関連記事

- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_1482 部分観測下における制御指向原子炉熱水力予測のためのグラフニューラルODEデジタルツイン
- /deep_370 設計段階でのスパース化によるクロスモダリティ予測：信頼性と効率的学習のためのL0ゲート表現

## 原文リンク

[ART：歩行者軌跡予測のための適応的関係Transformer（時間的関係を考慮）](https://tldr.takara.ai/p/2604.03649)
