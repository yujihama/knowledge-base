---
title: "競馬AI開発記録 #17 LightGBM rank_xendcg との死闘：勾配爆発を防ぐためのターゲット設計"
url: "https://zenn.dev/ricotiler/articles/keiba-ai-17-rank-xendcg-gradient-explosion"
date: 2026-06-10
tags: [LightGBM, Learning to Rank, rank_xendcg, 勾配爆発, ターゲット設計, Optuna, スピアマン相関]
category: "ai-ml"
related: [1429, 122, 113, 6527, 7700]
memo: "[Zenn 機械学習] 競馬AI開発記録 #17 LightGBM rank_xendcg との死闘：勾配爆発を防ぐためのターゲット設計"
processed_at: "2026-06-10T21:17:18.985860"
---

## 要約

本記事は競馬AIの開発記録第17話で、LightGBMのランキング学習目的関数 rank_xendcg を導入した際に発生した勾配爆発問題とその解決策を詳述する。

前回（第16話）は二値分類で穴馬識別（KS統計量0.50）を達成したが、レース全体の期待値最大化には全出走馬の相対的序列予測が必要と判断。objective を binary から rank_xendcg に変更した。rank_xendcg を選択した理由は、lambdarank が整数ラベルのみ受け付けるのに対し、rank_xendcg は連続値（浮動小数点）を扱えるため、着順だけでなく走破タイム偏差に基づく細粒度な実力差をラベルに反映できる点にある。

しかし導入直後、RMSEが1.85965e+13（18兆超）を記録し、feature_importanceも1.798997e+32という浮動小数点限界近傍の値を出力。スピアマン相関係数は0.0000となり、モデルが完全に崩壊した。原因は rank_xendcg 内部の利得計算式 Gain = 2^rel - 1 にある。頭数（最大18頭）をそのままターゲットラベルとして渡すと、例えば rel=18 で 2^18-1=262143 となり、さらに α=20 等の不適切なスケーリングで rel=30 相当になると 2^30-1≒10億 という極大な勾配が発生、連鎖的に重みが発散する。

解決策は2段階。第1に、ターゲットを (num_horses + 1 - rank) / num_horses で正規化し 0 < target ≤ 1 の範囲に収める。第2に、Optunaでハイパーパラメータ探索を行い、target_alpha の範囲を 1.1〜1.9 に制限した線形リレーション設計 target = (num_horses + 1 - rank) × (alpha/10) を採用。これにより最大ラベル値でも 2^1.9-1≒2.7 程度に抑えられ数値的安定性を確保。また metric を ndcg から rmse に切り替え（ndcg 指定時にターゲットが整数キャストされ情報欠損が発生する問題を回避）。

結果、RMSE は 0.3〜0.5 の正常値に収束し、スピアマン相関係数は 0.00 から 0.4021 へ劇的に改善。教訓として、LTR目的関数の内部仕様（指数関数的利得計算）を理解しないままの導入はサイレント失敗を招くこと、ターゲットのスケール設計はチューニングではなく前提条件であること、ConstantInputWarning 等の警告ログがデバッグの鍵になることが挙げられる。監査AIへの示唆として、複数証拠の相対的優先順位付けにLTRを活用する際も同様のスケール問題が発生しうるため、目的関数の数学的仕様確認は必須。

## アイデア

- rank_xendcg の内部利得計算 Gain=2^rel-1 が指数爆発する仕組みを実測値（RMSE=18兆）で可視化しており、LTR導入時のアンチパターンとして非常に教育的
- ターゲット正規化と alpha の範囲制限という2段階アプローチで 0<target≤1.9 に収める設計は、LTR以外の指数損失関数を使う場面にも汎用的に応用可能
- metric='ndcg' が連続値ターゲットで型エラーを起こすという LightGBM の実装上の罠を、rmse での収束監視という実用的な回避策で解決している点が実践的

## 前提知識

- **LightGBM** → /deep_866 AIに180回の株価予測実験を丸投げしてわかったこと——「AIだけでは正しく評価できない」という話
- **Learning to Rank (LTR)** (TODO: 読むべき)
- **lambdarank / rank_xendcg** (TODO: 読むべき)
- **NDCG** → /deep_1658 推薦システムにおけるデータの驚くべき有効性
- **Optuna** → /deep_103 OptunaとLLMを組み合わせたハイパーパラメータ最適化の比較実験

## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_122 ML学習記録 #1 — 初めてのKaggleコンペ（Store Sales時系列予測）でやったこと
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_6527 競馬予想MLでデータリーケージを正攻法で潰した話 — race_dateフィルタを4箇所に入れて気づいたこと
- /deep_7700 競馬AI開発記録 #15 バックテストの異常な高ROIを疑う：時点固定（PiT）生成とリークの物理的遮断

## 原文リンク

[競馬AI開発記録 #17 LightGBM rank_xendcg との死闘：勾配爆発を防ぐためのターゲット設計](https://zenn.dev/ricotiler/articles/keiba-ai-17-rank-xendcg-gradient-explosion)
