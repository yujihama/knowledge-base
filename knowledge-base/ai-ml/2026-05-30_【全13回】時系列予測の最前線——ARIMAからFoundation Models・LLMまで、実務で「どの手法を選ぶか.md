---
title: "【全13回】時系列予測の最前線——ARIMAからFoundation Models・LLMまで、実務で「どの手法を選ぶか」を決める"
url: "https://zenn.dev/salt2/articles/time-series-prediction-book-intro"
date: 2026-05-30
tags: [時系列予測, ARIMA, GBDT, Transformer, Foundation Models, TimesNet, Chronos, Diffusionモデル, 需要予測, 不確実性定量化]
category: "ai-ml"
related: [6566, 1494, 3654, 6284, 113]
memo: "[Zenn 機械学習] 【全13回】時系列予測の最前線——ARIMAからFoundation Models・LLMまで、実務で「どの手法を選ぶか」を決める"
processed_at: "2026-05-30T09:09:12.976876"
---

## 要約

ZennのSALT2テックブログが公開した全13回の時系列予測シリーズ（Zenn Books形式）。統計手法（ARIMA/SARIMA）からML（GBDT）、DL（Prophet・N-HiTS・PatchTST・TimesNet）、Foundation Models（Chronos・Lag-Llama・TimeGPT）、LLM・Diffusionモデルまでを体系的に解説する。

最大の特徴は「手法から入るのではなく、課題・ニーズから入る」という学習設計である。スコープはForecastingタスクに絞り（異常検知・分類は対象外）、軸ドメインを小売・ECの需要予測に設定することで、ビジネス課題との接点を常に意識した構成となっている。

全13回は3フェーズに分割される。第1〜5回（基礎）ではビジネス課題の整理、トレンド・季節性・定常性・自己相関・外れ値・欠損などデータの性質の理解、手法の全体マップを提供する。第6〜9回（手法詳解）ではARIMAの限界→GBDTへの橋渡し→DL系手法の系譜（Prophet・N-HiTS・PatchTST）という流れで「なぜ次の手法が必要になったか」を背景から解説し、第9回では「TransformerよりシンプルなMLP・線形モデルが勝つ条件」という重要な実務知見を示す。第10〜13回（最前線）ではTimesNet（時系列を2次元画像に変換して学習）、Foundation ModelsによるZero-shot予測（Chronos・Lag-Llama・TimeGPT）、LLMおよびDiffusionモデルによる確率的予測・不確実性定量化を扱い、「研究段階の手法」と「実務で今使える手法」を明確に区分する。

監査エージェント開発への示唆として、本シリーズが示す「手法選択の意思決定フレームワーク」はエージェントの判断ロジック設計に直接応用可能である。例えば、データ量・定常性・外れ値の有無・予測ホライズンに応じて手法を動的に選択するエージェントを構築する際の設計指針となる。また、確率的予測・不確実性定量化（Diffusionモデル・LLM応用）の概念は、監査エージェントがリスクスコアの信頼区間を提示する機能設計にも参考になる。Foundation Modelsによるゼロショット予測が実務適用可能かどうかを懐疑的に評価している点も、エージェントシステムへの無批判な最新手法導入を戒める視点として有用。

## アイデア

- TransformerよりシンプルなMLP・線形モデルが時系列予測で勝つケースが存在するという実証的知見——最新手法の無条件採用への警告
- TimesNetが時系列を2次元画像（テンソル）に変換することでCNN系アーキテクチャを適用するという発想の転換
- Foundation ModelsのZero-shot予測（Chronos・Lag-Llama・TimeGPT）が実務でどこまで使えるかを懐疑的研究も含めフラットに評価する姿勢

## 前提知識

- **ARIMA/SARIMA** (TODO: 読むべき)
- **GBDT** → /deep_5473 Kaggle参戦記録V0.6：特徴量エンジニアリングとLightGBMの学習回数増加でROC-AUC 0.852を達成
- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Prophet** → /deep_6566 時系列予測の最前線：手法選択から Foundation Models まで
- **Foundation Models** → /deep_791 ウェルビーイングに根ざしたAIのポジティブビジョンが必要である

## 関連記事

- /deep_6566 時系列予測の最前線：手法選択から Foundation Models まで
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_3654 電気自動車充電需要の時空間モデリング：スコットランド大規模データセットとINLAによるベイズ推論
- /deep_6284 長い時系列予測における効率的なTransformer：LogTrans・Informer・Reformer・Pyraformerの比較整理
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた

## 原文リンク

[【全13回】時系列予測の最前線——ARIMAからFoundation Models・LLMまで、実務で「どの手法を選ぶか」を決める](https://zenn.dev/salt2/articles/time-series-prediction-book-intro)
