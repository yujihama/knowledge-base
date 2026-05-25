---
title: "LSTM AutoEncoderによる異常検知モデルをMLOps化してみた"
url: "https://zenn.dev/parabolaml/articles/450d7586390d4e"
date: 2026-05-25
tags: [LSTM, AutoEncoder, MLOps, FastAPI, Docker, 異常検知, NASA Turbofan, Pydantic, SQLite, Streamlit, 時系列]
category: "infra"
related: [1448, 280, 1385, 3946, 1915]
memo: "[Zenn 機械学習] LSTM AutoEncoderによる異常検知モデルをMLOps化してみた"
processed_at: "2026-05-25T09:09:32.830341"
---

## 要約

NASA Turbofan データセット（航空機エンジンの時系列センサーデータ）を用いて、LSTM AutoEncoder ベースの異常検知モデルを構築し、それをMLOpsとして実運用可能な形に整備した実装事例。

モデルの核心は AutoEncoder の復元誤差（reconstruction error）を異常スコアとして利用する点にある。正常データのみで学習させた LSTM AutoEncoder は、正常パターンをうまく復元できる一方、劣化・異常パターンは復元失敗する。この差分（|X - X_hat|^2）を異常スコアとして扱う。NASA Turbofan では unit_number ごとに時系列 window を切ることが重要で、unit をまたいだ window 化は LSTM の劣化パターン学習を妨げる。

MLOps化は以下5段階で実施した。①推論処理の関数化：前処理（scaler による標準化）・LSTM 推論・reconstruction error 計算・異常判定を predict_anomaly() に集約し、再利用可能なパイプラインとして整理。②FastAPI による POST /predict エンドポイントの構築：10サイクル分の21センサー値を JSON で受け取り、異常スコア・rolling_error・severity・上位エラーセンサー・latency_ms などの運用メトリクスを返す。Pydantic により入力値の型バリデーションを実装し、不正入力時は 500 ではなく 422 Validation Error を返す。③severity の3段階設計：単発の threshold 超えを warning、連続 alert を critical とし、数値スコアを業務判断に使える形に変換。④推論ログの二重保存：JSONL（入出力をそのまま保存、デバッグ・トレース用）と SQLite（alert 数・severity 比率・latency の SQL 集計用）の両方に記録し、Streamlit ダッシュボードへ連携。⑤Docker Compose 化：FastAPI・モデル・SQLite・JSONL を一括コンテナ化し、ログ保存先を volume として外出しすることでコンテナ再ビルド時もデータを永続化。

監査エージェント開発への示唆として、本構成は「センサーデータ → 異常スコア算出 → severity 判定 → ログ記録 → ダッシュボード監視」というパイプラインが明確に分離されており、監査ログ分析における異常取引検知への転用が考えられる。特に severity の段階設計（normal/warning/critical）と Pydantic による入力バリデーションは、監査エージェントの出力設計にそのまま応用できるパターンである。

## アイデア

- unit_number をまたがないウィンドウ分割の設計：時系列モデルで複数エンティティのデータを扱う際、エンティティ境界をまたいだウィンドウ化が学習を破壊するという問題は、監査ログや取引データの分析でも同様に発生する普遍的な課題
- severity の段階設計（単発 warning・連続 critical）：数値スコアを業務アクションに直結する判定ロジックとして整理する設計パターンは、LLM-as-judge やエージェントの出力設計にも応用可能
- JSONL と SQLite の役割分離：JSONL をデバッグ・トレース用のイミュータブルな記録として、SQLite を集計・監視用の構造化ストアとして使い分ける二重ログ設計は、MLOps における observability の実践的パターン

## 前提知識

- **LSTM** → /deep_97 AIトレーダー開発ログ #2: Paper Tradingで検証したQuant型アーキテクチャの有効性
- **AutoEncoder** (TODO: 読むべき)
- **reconstruction error** (TODO: 読むべき)
- **FastAPI** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **Docker Compose** (TODO: 読むべき)

## 関連記事

- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新
- /deep_280 敵対的ロバスト性を持つ多変量時系列異常検知：結合情報保持による手法（ARTA）
- /deep_1385 事前学習済み時系列モデルを活用したクロスマシン異常検知
- /deep_3946 【FastAPI新機能】SSEネイティブサポートでAIチャットのストリーミング処理が簡潔に書ける
- /deep_1915 MCP（Model Context Protocol）実践ガイド——PythonでAIエージェントにツールを接続する

## 原文リンク

[LSTM AutoEncoderによる異常検知モデルをMLOps化してみた](https://zenn.dev/parabolaml/articles/450d7586390d4e)
