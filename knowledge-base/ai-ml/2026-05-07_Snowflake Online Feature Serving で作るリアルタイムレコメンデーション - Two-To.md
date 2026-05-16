---
title: "Snowflake Online Feature Serving で作るリアルタイムレコメンデーション - Two-Tower ネットワーク"
url: "https://zenn.dev/snowflakejp/articles/35e615c568f7c9"
date: 2026-05-07
tags: [Two-Tower, Online Feature Serving, Snowflake, レコメンデーション, EMA, Feature Store, Dynamic Tables, リアルタイム推論]
category: "ai-ml"
related: [889, 3784, 2875, 1704, 2370]
memo: "[Zenn 機械学習] Snowflake Online Feature Serving で作るリアルタイムレコメンデーション - Two-Tower ネットワーク"
processed_at: "2026-05-07T21:22:02.741113"
---

## 要約

本記事は、Snowflake Online Feature Serving と Two-Tower ニューラルネットワークを組み合わせたリアルタイム商品レコメンデーションシステムの構築方法を解説する。

従来のバッチ処理型レコメンデーションでは、1時間〜1日単位の更新遅延が生じ、ユーザーが電化製品をクリックしてもファッション商品が表示され続けるといった問題が発生する。新規ユーザーへのパーソナライズも次回バッチまで待機が必要となる。これらを解消するため、バッチの信頼性とリアルタイム応答性を両立した3層アーキテクチャを採用している。

アーキテクチャの中核はSnowflake Online Feature Servingで、2025年11月のSnowflake年次カンファレンス「BUILD」で発表された機能。内部ではDynamic Tablesが動作し、target_lag="10 seconds"と設定することでオンラインストアをソースデータから10秒以内の鮮度に維持する。特徴量取得は100ms未満のレイテンシを実現し、store_type=StoreType.ONLINEパラメータによりSnowflakeの最適化済みサービングインフラへリクエストが転送される。

Two-Towerモデルは、ItemTowerとUserTowerの2つのニューラルネットワークで構成される。ItemTowerは入力次元8・隠れ層64・出力32次元のMLPで商品埋め込みを事前計算（バッチ処理）。UserTowerは入力次元38の同構成で、Online Feature Storeから取得したリアルタイム特徴量（RECENT_CLICK_IDS, CATEGORY_PREFERENCE等）からユーザー埋め込みを生成する。両タワーの出力はL2正規化され、同一埋め込み空間上でコサイン類似度によりマッチングされる。

瞬時パーソナライゼーションの鍵はデルタ埋め込みで、指数移動平均（EMA）を用いてクリックのたびにインメモリでユーザー埋め込みを更新する（new_delta = 0.7 * current_delta + 0.3 * item_embedding）。ベース埋め込み（Feature Storeから10秒ごと更新）とデルタ埋め込み（クリックごとにリアルタイム更新）を組み合わせることで、長期的嗜好と現在セッションの即時適応を両立する。

実装はSnowflake MLのFeatureStore APIで行い、Entity定義・FeatureView登録・OnlineConfig設定の3ステップで構成される。Online Feature Servingは専用コンピュートリソースを使用するため、開発時はenable=Falseで無効化してコスト管理することを推奨している。

応用領域として不正検知（リアルタイム取引特徴量による即時リスクスコアリング）・動的価格設定・コンテンツパーソナライゼーションが挙げられており、監査AIへの転用可能性も高い。完全なソースコードはSnowflake-Labs GitHubリポジトリで公開されている。

## アイデア

- デルタ埋め込みとベース埋め込みの分離設計：長期嗜好（Feature Store、10秒ラグ）と短期嗜好（クリックごとEMA更新）を独立したベクトルとして保持し合成する設計は、モデル再学習なしでセッション内パーソナライゼーションを実現する軽量なアーキテクチャパターンである
- target_lagによるコスト・鮮度トレードオフの明示的制御：Snowflake Dynamic Tablesの増分同期を利用し、ユースケースに応じてデータ鮮度（秒〜分〜時間）を宣言的に設定できる点は、MLOpsにおけるSLA設計を単純化する
- 不正検知への転用可能性：リアルタイム取引特徴量の即時スコアリングという応用例は、監査エージェントシステムにおける異常トランザクション検知（リアルタイムリスクスコアリング）に直接応用できるアーキテクチャパターンである

## 前提知識

- **Two-Tower Network** (TODO: 読むべき)
- **Feature Store** → /deep_4047 Snowflake Online Feature Serving で作るリアルタイムレコメンデーション - Two-Tower ネットワーク
- **EMA（指数移動平均）** (TODO: 読むべき)
- **コサイン類似度** → /deep_371 選択的勾配射影による継続学習での忘却軽減
- **Dynamic Tables** → /deep_4047 Snowflake Online Feature Serving で作るリアルタイムレコメンデーション - Two-Tower ネットワーク

## 関連記事

- /deep_889 自律走行のための深層ニューラルネットワークを用いた道路工事検知システム
- /deep_3784 脳腫瘍自動分類のための解釈可能なVision Transformerフレームワーク
- /deep_2875 第4回海事コンピュータビジョンワークショップ（MaCVi 2026）：チャレンジ概要
- /deep_1704 機械学習ディレクターたちの現場インサイト【前編】：メディア・製薬・研究分野での実践知
- /deep_2370 クロスレイヤー協調最適化LSTMアクセラレータによるリアルタイム歩行分析

## 原文リンク

[Snowflake Online Feature Serving で作るリアルタイムレコメンデーション - Two-Tower ネットワーク](https://zenn.dev/snowflakejp/articles/35e615c568f7c9)
