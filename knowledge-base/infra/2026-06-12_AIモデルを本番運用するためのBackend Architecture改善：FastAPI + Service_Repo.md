---
title: "AIモデルを本番運用するためのBackend Architecture改善：FastAPI + Service/Repository層の分離"
url: "https://zenn.dev/parabolaml/articles/114474b575110b"
date: 2026-06-12
tags: [FastAPI, MLOps, Service Layer, Repository Pattern, SQLAlchemy, Alembic, PostgreSQL, Pydantic Settings, pytest, GitHub Actions, LSTM AutoEncoder, 異常検知]
category: "infra"
related: [6492, 1448, 327, 1645, 1791]
memo: "[Zenn 機械学習] AIモデルを本番運用するためのBackend Architecture改善"
processed_at: "2026-06-12T09:09:36.049355"
---

## 要約

NASA Turbofanデータセットを用いたLSTM AutoEncoderによる異常検知APIを題材に、「動くだけ」のサンプル構成から実務運用に耐えるBackend構成へリファクタリングした実践記録。

初期構成（Before）はFastAPI → Model推論 → SQLite保存という単純な構造で、/predictエンドポイント内に前処理・推論・閾値判定（0.05固定）・DB保存（cursor.execute直書き）が混在していた。これにより可読性の低下、テスト細分化の困難、PostgreSQL移行への脆弱性という3つの実務上の問題を抱えていた。

改善後（After）はFastAPI Endpoint → Service → Repository → SQLAlchemy ORM → PostgreSQLという層分離構成を採用。具体的には：

① **Service Layer**：前処理・推論・閾値判定・DB保存をPredictionServiceクラスに集約。閾値はPydantic Settingsから注入（コード直書き廃止）、保存先はRepositoryインターフェース経由に抽象化。Batch処理・Streamlit・CLI等の複数経路から同一Serviceを再利用可能にした。

② **Repository Layer**：create/find/updateなどのDB操作を隠蔽。SQLite直接操作からSQLAlchemyへ移行し、テスト時のmock化が容易になった。

③ **ORM + PostgreSQL + Alembic**：本番向けPostgreSQLへ移行し、スキーマ変更をAlembicでバージョン管理・rollback可能にした。

④ **async化とPydantic Settings**：API入口のみasync化（PyTorch推論はCPU/GPU計算のため全async化しても高速化しない点を明記）。設定は.envファイルへ分離しlocal/dev/prod切替を実現。

⑤ **pytest + GitHub Actions**：Service Layerの単体テストを整備し、push時にinstall → migration → pytest を自動実行するCI/CDパイプラインを構築。

最終ディレクトリ構成はapi/services/repositories/db/core/inference/tests/alembicの8層構造。反省点としてFastAPIのDepends()によるDI（Session → Repository → Service）の理解不足と、移行ステップを一括ではなく段階確認を怠ったことを挙げている。

監査エージェント開発への示唆：LangGraphベースの監査エージェントでも同様のService/Repository分離が有効。推論ロジック（エージェント判断）をServiceに集約し、証跡保存をRepository経由にすることで、テスト容易性と複数経路（API/バッチ/スケジューラ）からの再利用性を両立できる。

## アイデア

- PyTorch推論はCPU/GPU同期計算のためasync化しても高速化しない——async化の適用範囲をI/O待ち（DBアクセス等）に限定するという実践的な判断基準
- Service LayerをAPI経路から切り離すことで、同一ビジネスロジックをBatch/CLI/Schedulerから再利用できる設計——AIモデルの推論ロジックを複数トリガーから呼び出す監査エージェントに直接応用可能
- SQLite直書き → ORM → Repository → PostgreSQLという段階的移行パスを一括ではなく1ステップずつ検証する重要性——大規模リファクタリング時の回帰リスク管理手法として有用

## 前提知識

- **FastAPI** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **Repository Pattern** (TODO: 読むべき)
- **SQLAlchemy ORM** (TODO: 読むべき)
- **LSTM AutoEncoder** → /deep_6492 LSTM AutoEncoderによる異常検知モデルをMLOps化してみた
- **Dependency Injection** (TODO: 読むべき)

## 関連記事

- /deep_6492 LSTM AutoEncoderによる異常検知モデルをMLOps化してみた
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新
- /deep_327 音響プロファイリングによるデータ駆動型塑性変形モデリング
- /deep_1645 雰囲気でML運用してない？Google流「ML Test Score」でMLパイプラインの信頼性を数値化する
- /deep_1791 金融系データサイエンティストがAWS11冠を通して見えたこと

## 原文リンク

[AIモデルを本番運用するためのBackend Architecture改善：FastAPI + Service/Repository層の分離](https://zenn.dev/parabolaml/articles/114474b575110b)
