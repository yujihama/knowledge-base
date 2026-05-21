---
title: "Muonを事前学習以降へ拡張する再考：VLAとRLVRにおけるスペクトル破綻とハイパスによる解決策"
url: "https://tldr.takara.ai/p/2605.19282"
date: 2026-05-21
tags: [Muon, Pion, GRPO, RLVR, VLA, スペクトルホワイトニング, Newton-Schulz, LLM最適化, ロボット学習, GRPOポストトレーニング]
category: "ai-ml"
related: [1737, 1156, 5079, 2931, 2667]
memo: "[HF Daily Papers] Rethinking Muon Beyond Pretraining: Spectral Failures and High-Pass Remedies for VLA and RLVR"
processed_at: "2026-05-21T21:03:19.588782"
---

## 要約

Muonは、Newton-Schulz（NS）反復を用いてモメンタム行列の全特異値を1に近づける「均一スペクトルホワイトニング」を行う行列対応オプティマイザである。LLM事前学習においてAdamWを上回る性能を示す一方、本論文は事前学習以降の2つのシナリオでMuonが根本的な限界を持つことを示す。

第1の問題はVLA（Vision-Language-Action）訓練である。ロボット制御などのアクションモジュールの勾配は本質的に低ランクであり、均一ホワイトニングがノイズの多い末尾の特異値方向を増幅してしまう。第2の問題はRLVR（Reinforcement Learning with Verifiable Rewards）のポストトレーニングである。GRPOなどの強化学習では勾配のSNR（信号対雑音比）が低く、かつ事前学習で獲得したアテンションヘッドごとの特化（per-head specialization）を保持する必要があるため、ホワイトニングが不安定化を招く。

これを解決するために提案されるのが**Pion**である。PionはMuonのドロップイン代替として設計され、計算効率を維持しつつ均一ホワイトニングを「Promotion+Suppression（P+S）機構」に置き換える。具体的には、高域通過フィルタ型のNS反復（High-Pass NS iteration）を採用し、支配的な特異値を1に固定したまま、ノイズの多い末尾成分を0に向けて抑制する。フィルタ強度は制御可能なパラメータとして調整できる。さらに、アテンションヘッドの異質性（per-head heterogeneity）を保持するため、テンソルをreshapeするだけで各ヘッドに独立してアップデートを適用する「per-headモード」も追加コストなしでサポートする。

実験結果は顕著である。VLA訓練（LIBEROおよびLIBERO-Plusベンチマーク）において、Pionはl1回帰ベースのVLA-AdapterとフローマッチングベースのVLANeXtの両アーキテクチャでベースラインを一貫して上回り、VLA-AdapterでLIBERO Objectタスクの1,500ステップ時点の成功率はPionが100%、Muonが97.0%、AdamWがわずか32.2%であった。実機ロボット（Franka Research 3、pi_0.5バックボーン、DROIDセットアップ）での3つの把持・配置タスクでも優位性を確認している。RLVR後処理においては、Qwen3-1.7B/4BにGRPOおよびGMPOを適用した場合、MuonはMATH・GSM8Kでゼロに崩壊するのに対し、PionはAdamWを上回る性能を達成した。監査エージェント開発への示唆として、GRPOベースのRLVRポストトレーニングにおけるオプティマイザ選択の重要性が再確認され、特に低SNR勾配環境での安定した学習手法としてPionは有望な代替候補となりうる。

## アイデア

- 均一スペクトルホワイトニングが「低ランク勾配」環境でノイズ増幅を引き起こすという発見は、オプティマイザの適用域を訓練フェーズ別に分けて評価する必要性を示す
- High-Pass NS反復という概念は、信号処理のハイパスフィルタをオプティマイザの更新則に組み込んだものであり、勾配スペクトルをフィルタリングするという新しい設計パラダイムを提示している
- per-headモードはreshapeのみで実現されるため、既存のMuon実装への移行コストが極めて低く、RLVR後処理での実用的な採用が容易である

## 前提知識

- **Muon optimizer** (TODO: 読むべき)
- **Newton-Schulz反復** (TODO: 読むべき)
- **GRPO** → /deep_152 トークンを流し続けろ：16のオープンソースRLライブラリから学ぶ非同期学習アーキテクチャ
- **特異値分解（SVD）** (TODO: 読むべき)
- **VLA（Vision-Language-Action）** (TODO: 読むべき)

## 関連記事

- /deep_1737 難問を「選択肢」に変える：RLVRの探索限界を突破するCog-DRIFT
- /deep_1156 結果誘導ステップのためのプロセス報酬を用いたLLM推論：PROGRSフレームワーク
- /deep_5079 二値報酬と強化学習：根本的な課題
- /deep_2931 ロボットはどのように学習するか：現代史概観
- /deep_2667 ロボットはいかに学習するか：現代史の概観

## 原文リンク

[Muonを事前学習以降へ拡張する再考：VLAとRLVRにおけるスペクトル破綻とハイパスによる解決策](https://tldr.takara.ai/p/2605.19282)
