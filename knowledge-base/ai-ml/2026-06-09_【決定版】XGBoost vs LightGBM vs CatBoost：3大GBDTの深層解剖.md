---
title: "【決定版】XGBoost vs LightGBM vs CatBoost：3大GBDTの深層解剖"
url: "https://zenn.dev/mkawa_pani/articles/05eab23d9e2fba"
date: 2026-06-09
tags: [GBDT, XGBoost, LightGBM, CatBoost, Tabularデータ, Target Encoding, Histogram-based, GOSS, EFB, 正則化, Kaggle]
category: "ai-ml"
related: [1429, 5729, 5473, 5658, 634]
memo: "[Zenn 機械学習] 【決定版】XGBoost vs LightGBM vs CatBoost：3大GBDTの深層解剖"
processed_at: "2026-06-09T12:01:04.000106"
---

## 要約

本記事は、Tabularデータ分析における3大勾配ブースティング決定木（GBDT）ライブラリであるXGBoost・LightGBM・CatBoostを、アルゴリズム設計思想から実務的な使い分けまで体系的に解説する。

GBDTの基本原理は「前の木の残差を次の木が補正する」逐次的アンサンブルであり、並列構築のRandom Forestとは本質的に異なる。LLM時代においてもTabPFN・TabICLなどのNN系モデルが台頭しているが、速度・精度・扱いやすさのバランスでKaggle等のコンペではGBDT三強の優位性が続いている。

**XGBoost**は目的関数に正則化項Ω(f)=γT+(1/2)λΣw_j²を明示的に組み込み、リーフ数増加ペナルティ（γ）と出力値過大ペナルティ（λ）で過学習を抑制する。木の成長はdepth-wise（level-wise）で、同じ深さのノードを横並びに分割するため構造が安定しやすい。特徴量エンジニアリングとOptunaによるパラメータ探索との組み合わせで最終的に最強の単体モデルになることが多い。

**LightGBM**の高速化の核心はHistogram-based algorithm（連続値をbinに量子化して分割点候補を削減）、GOSS（勾配が大きい＝未学習のサンプルを優先してサンプリング）、EFB（One-Hot由来の相互排他的スパース特徴量を束ねて次元削減）の3技術にある。木の成長はleaf-wise（損失減少量最大のリーフを優先して深掘り）で非対称な木構造になりやすく、交互作用・Count Encoding・Target Encodingが効くデータで特に強い。過学習制御のためnum_leaves・min_child_samples・feature_fractionなどのパラメータ管理が重要。

**Target Encoding**についても詳しく解説されており、TE(k)=(Σy_i + αμ)/(n_k + α)のsmoothing付き数式でカテゴリをターゲット統計量に変換する。データ数が少ないカテゴリでは全体平均μに引き寄せることでノイズを抑制する。GBDTは数値の大小で分割するため、カテゴリ変数をそのまま渡すより目的変数の統計量に変換した方が相性が良い。ただしリーク（自身の目的変数を自身の特徴量に使用）への対策としてクロスバリデーション内での計算が不可欠。

**CatBoost**はカテゴリカル特徴量のネイティブ処理を最大の特徴とし、Ordered Boostingという手法でリーク防止付きのTarget Encodingを内部で自動実行する。学習データの順序を工夫してターゲット統計量計算時のリークを排除するため、前処理なしでカテゴリ変数を直接投入できる。一方でLightGBMほどの速度はなく、カテゴリ変数が少ないデータセットでは優位性が薄れる傾向がある。

監査エージェント開発への示唆として、構造化データ（取引ログ・仕訳データ等）の異常検知や分類タスクにGBDTは依然有効であり、特にCatBoostのカテゴリ変数処理は勘定科目コードや取引先コードなど高カーディナリティカテゴリを多用する監査データと親和性が高い。

## アイデア

- GOSS（Gradient-based One-Side Sampling）の「まだ間違えているサンプルを優先」という発想は、強化学習のPrioritized Experience ReplayやLLM学習でのDPOにおけるハード例重視の考え方と同型であり、学習効率化の普遍的原理として捉えられる
- EFB（Exclusive Feature Bundling）による相互排他的特徴量の束ね処理は、疎な高次元空間の効率的な情報圧縮であり、スパースAttentionやMoEのゲーティングと概念的に近い次元削減戦略として興味深い
- CatBoostのOrdered Boostingは時系列順にデータを処理してリークを排除する設計であり、「過去データのみで現在を予測する」という監査・コンプライアンス文脈のタイムスタンプ厳守要件と自然に整合する

## 前提知識

- **勾配ブースティング** → /deep_2559 LLMエンベディングを用いた臨床記録からの外傷後てんかん予測
- **決定木** → /deep_3207 Adaptive MSD-Splitting：歪んだ連続属性に対するC4.5とランダムフォレストの改善手法
- **正則化（L1/L2）** (TODO: 読むべき)
- **Target Encoding** (TODO: 読むべき)
- **One-Hot Encoding** (TODO: 読むべき)

## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_5729 XGBoostを初心者向けにざっくり理解する
- /deep_5473 Kaggle参戦記録V0.6：特徴量エンジニアリングとLightGBMの学習回数増加でROC-AUC 0.852を達成
- /deep_5658 オープンソースSIEMにおけるMITRE ATT&CK強化行動プロファイリングによるコンテキスト認識型Web攻撃検知
- /deep_634 TrialsBankを用いた臨床試験の運用成功予測のための潜在リスク認識機械学習アプローチ

## 原文リンク

[【決定版】XGBoost vs LightGBM vs CatBoost：3大GBDTの深層解剖](https://zenn.dev/mkawa_pani/articles/05eab23d9e2fba)
