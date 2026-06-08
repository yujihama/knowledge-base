---
title: "【Snowflake Summit 2026】Agentic ML in Snowflakeの新機能まとめ"
url: "https://zenn.dev/finatext/articles/snowflake-summit-2026-agentic-ml"
date: 2026-06-08
tags: [Snowflake, Agentic ML, Snowflake CoCo, MLOps, Cortex Training, Online Feature Store, GPU多重化, LLMポストトレーニング, DAGパイプライン, A/Bテスト]
category: "infra"
related: [1645, 1794, 1791, 6494, 7178]
memo: "[Zenn 機械学習] 【Snowflake Summit 2026】What's New: Agentic ML in Snowflake"
processed_at: "2026-06-08T09:12:55.249028"
---

## 要約

Snowflake Summit 2026のセッション「What's New: Agentic ML in Snowflake」の内容レポート。データサイエンティストの60%以上の時間がデータクリーニングに費やされているという課題に対し、Snowflakeはプラットフォーム統合型のAgentic MLで解決を図る。中核となるのがSnowflake CoCo（旧Cortex Code）というコーディングエージェントで、Snowflakeのデータプラットフォームにネイティブ統合されており、テーブル・ノートブック・モデル・実験ログを事前に把握した状態でタスクを自律実行できる。Claude Codeに近い設計だが、Snowflakeのデータ・コンピュート・RBACにシームレスに接続されている点が差別化要素。新機能はDevelop・Orchestrate・Deploy・Monitorの4ステージで整理される。Developでは、VS Code/Cursor拡張（PrPr）によるローカルIDE開発とSnowflakeリモート実行の連携、エンタープライズ向けのCustom Container Runtime、フルマネージドLLMポストトレーニング基盤「Cortex Training」が追加された。Cortex TrainingはFine-Tuning・強化学習・継続事前学習に対応し、VeRL・DeepSpeedエンジンをサポート。GPUを多重化することで利用率を60%から100%近くに引き上げ、同一予算で約2倍のスループットを実現する。既存学習基盤はPyTorchベンチマークで競合比約2.5倍速・3倍安とされる。OrchestrateではSnowsight Pipeline BuilderによりNotebookとML JobsをDAGとしてビジュアル構築できる（PrPr）。DeployではOnline Feature StoreにストリーミングIngestionが追加され、ストリーミングイベントから2〜3秒以内にPython変換、Postgresバックエンドで10ms未満のFeature取得レイテンシを実現。競合比でレイテンシ2.5倍低・TPS7倍高を主張。MonitorではA/Bテストでchampion/challengerにトラフィックを50/50分割し、one-click rollbackとUnified observabilityをSnowsight上で提供。監査エージェント開発への示唆として、ガバナンス・RBACが統合されたMLプラットフォームは監査証跡の一元管理に有効であり、CoCoのようなコンテキスト統合型エージェント設計はLangGraphベースの監査エージェントが直面するデータサイロ問題への実装参照として価値がある。

## アイデア

- GPUを複数ジョブで多重化（multiplex）することで利用率を60%→100%近くに引き上げ、同一GPU予算で約2倍スループットを得る設計は、ローカルLLMインフラ構築時のGPU効率化にも応用可能
- CoCoは「データ・コンピュート・RBACをすでに知っている」コーディングエージェントという設計思想で、エージェントのコンテキスト断絶問題をインフラ統合で解決するアプローチ——LangGraphエージェント設計でも同様にツール間コンテキストの一元化が性能を左右する
- Cortex TrainingがVeRL（強化学習フレームワーク）をサポートしている点は、GRPO/RLAIFベースのLLMカスタマイズをフルマネージドで実施できる環境として注目に値する

## 前提知識

- **MLOps** → /deep_6677 LLM観測性ツール5社の実装思想を並べてみた
- **Feature Store** → /deep_4194 Snowflake Online Feature Serving で作るリアルタイムレコメンデーション - Two-Tower ネットワーク
- **DAGオーケストレーション** (TODO: 読むべき)
- **LLMファインチューニング** → /deep_133 分離型報酬モデリングによる差分プライバシー保護RLHFフレームワーク
- **RBAC** → /deep_5264 Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS

## 関連記事

- /deep_1645 雰囲気でML運用してない？Google流「ML Test Score」でMLパイプラインの信頼性を数値化する
- /deep_1794 長期埋め込み（LTE）によるバランスの取れたパーソナライゼーション
- /deep_1791 金融系データサイエンティストがAWS11冠を通して見えたこと
- /deep_6494 製造業AIでPoC止まりになるテーマと、事業実装まで進むテーマの違い
- /deep_7178 生成AI時代に問われるのは「評価する力」である

## 原文リンク

[【Snowflake Summit 2026】Agentic ML in Snowflakeの新機能まとめ](https://zenn.dev/finatext/articles/snowflake-summit-2026-agentic-ml)
