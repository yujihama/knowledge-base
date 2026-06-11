---
title: "Next Forcing：マルチチャンク予測によるCausal World Modeling"
url: "https://tldr.takara.ai/p/2606.11187"
date: 2026-06-11
tags: [World Action Model, 自己回帰型動画生成, Multi-Token Prediction, マルチチャンク予測, ビデオデノイジング, RoboTwin, カusal World Model, 推論加速]
category: "ai-ml"
related: [1342, 7354, 5217, 1341]
memo: "[HF Daily Papers] Next Forcing: Causal World Modeling with Multi-Chunk Prediction"
processed_at: "2026-06-11T12:20:50.422481"
---

## 要約

Next Forcingは、自己回帰型動画生成におけるWorld Action Models（WAMs）の訓練収束速度・精度・推論速度の3つを同時に改善するマルチチャンク予測（MCP）フレームワークである。

既存の自己回帰型動画生成モデルは、訓練時の監督信号が現在のチャンクに限定されており、未来のダイナミクスに関する明示的なシグナルがないため、特に高フレームレート環境での収束が遅く、精度も低い。また推論時には逐次的な動画デノイジングが必要となり、速度が遅いという課題がある。

Next Forcingはこれに対し、LLMにおけるMulti-Token Prediction（MTP）の考え方を動画生成に転用する。具体的には、メインモデルに軽量な補助MCPモジュールを追加し、next¹・next²・next³チャンクという複数の未来時間軸で同時にビデオチャンクをデノイジングする訓練目標を導入する。各MCPモジュールはメインモデルの複数レイヤーから融合した中間特徴量を活用してカusal連鎖を形成し、近未来予測が遠未来予測を情報補完する構造になっている。これにより、密なマルチスケール時間監督シグナルがメインモデルへ逆伝播される。

実験結果として、50fpsの条件下でLingBot-VAと比較した場合、5,000ステットの訓練でRelative Improvement 93.1%を達成し、収束速度は2.3倍速い。ロボット操作ベンチマークRoboTwinでは、Clean/Randomの両条件でそれぞれ94.1%/93.5%という新たなState-of-the-Art結果を記録した。推論時にはMCPモジュールを残存させることで現在チャンクと次チャンクを並列生成でき、推論速度2倍の加速を実現する。また物理法則遵守を評価するPhyWorldベンチマークでも有意な改善を示し、一般動画事前訓練においてFVD（Fréchet Video Distance）を50%以上削減している。

監査エージェント開発への示唆：Next Forcingのアーキテクチャ設計（補助ヘッドによる複数ホライゾン同時予測・密な監督信号）は、逐次的意思決定を行うエージェントが複数ステップ先の状態を同時予測する訓練構造として応用可能である。LangGraphベースのReActエージェントにおいても、次アクションだけでなく複数ステップ先の中間状態をaux lossで予測させることで、収束速度と精度の向上が期待できる。

## アイデア

- LLMのMulti-Token Predictionをそのまま動画生成に転用し、複数未来チャンクの同時デノイジングで密な時間監督シグナルを生成するアイデアは、モダリティを超えたアーキテクチャ設計原則の汎用性を示している
- 推論時にもMCPモジュールを保持して現在・次チャンクを並列生成することで、訓練と推論の両フェーズで同一モジュールを活用する効率的なdual-use設計が実現されている
- near-futureの予測がfar-futureの予測を情報補完するカusal連鎖構造は、長期計画が必要なロボティクスや意思決定エージェントへの転用可能性を持つ

## 前提知識

- **自己回帰型動画生成** (TODO: 読むべき)
- **Diffusion Model / デノイジング** (TODO: 読むべき)
- **Multi-Token Prediction (MTP)** (TODO: 読むべき)
- **World Model / WAM** (TODO: 読むべき)
- **FVD（Fréchet Video Distance）** (TODO: 読むべき)

## 関連記事

- /deep_1342 一貫した世界モデルに向けて：マルチトークン予測と潜在意味強化
- /deep_7354 WALL-WM: イベント境界でワールドアクションモデリングを彫刻する
- /deep_5217 MTP（Multi-Token Prediction）の系譜とメカニズムを徹底解説
- /deep_1341 Action Images: マルチビュー動画生成によるエンドツーエンドのロボット方策学習

## 原文リンク

[Next Forcing：マルチチャンク予測によるCausal World Modeling](https://tldr.takara.ai/p/2606.11187)
