---
title: "Stena Expenseの検知アーキテクチャ ── Go × Python × gRPCで不正検知を実現する仕組み"
url: "https://zenn.dev/chillstack/articles/2026-04-20-detection-architecture-stena-expense"
date: 2026-04-29
tags: [gRPC, Go, Python, Google Cloud Workflows, Cloud Run, 不正検知, マイクロサービス, pickle, コールバックパターン, pandas]
category: "infra"
related: [2698, 1784, 875, 2551, 1792]
memo: "[Zenn 機械学習] Stena Expenseの検知アーキテクチャ ── Go × Python × gRPCで不正検知を実現する仕組み"
processed_at: "2026-04-29T12:38:34.019669"
---

## 要約

ChillStackが提供するSaaS「Stena Expense」の不正経費検知システムのアーキテクチャを解説した記事。企業の経費データを受け取り、AIで不正・異常を検知するサービスで、毎月数万〜数十万件の経費明細を自動チェックする。

システム構成は、Next.js製のUI（Manager）、Go製のモノリシックバックエンド（Controller）、Python製の検知サービス（Predictor）の3層構造。Google Cloud WorkflowsとCloud Run Jobを使い、「データ取り込み→抽出→検知実行→集計」の4ステップからなるパイプラインを制御する。WorkflowのYAMLでtry/exceptによるエラーハンドリングを実装しており、いずれかのステップで失敗するとControllerにPATCHリクエストを送り、現在のステータスから失敗箇所を自動判定して適切な失敗状態に遷移させる設計が特徴的。

GoとPythonを分離した理由は言語特性の違いにある。Go側はAPIゲートウェイ・認証・権限管理・ワークフロー制御・データ永続化などビジネスロジック全般をモノリスとして担い、型安全性と堅牢性を担保。Python側はpandasを活用したデータ分析・前処理と検知ロジックの実装に特化し、Predictorは検知時のみ稼働するため独立したスケーリングも可能。

最も特徴的な技術的設計が双方向gRPCコールバックパターン。Cloud Run Job（Go）→Predictor方向はPredictServiceのBulkPredictで検知依頼を送信し、Predictor→Controller方向はPredictionHandlerのSaveAnomaly/FinishPrediction/FailPredictionでコールバックする2サービス定義構成。検知を依頼するCloud Run Jobは一時的なバッチプロセスであるため、通常のリクエスト→レスポンスでは結果をCloud Run Jobが中継する無駄が生じる。コールバック方式により、Predictorが検知結果を検知モデルごとに直接Controllerへバッチ送信でき、Cloud Run Jobによるデータ中継を排除。数千〜数万件に達する検知結果をモデルごとに逐次送信してメモリを解放できるため、Predictorのメモリ効率も向上する。コールバック部分にはtries=3・delay=1・backoff=2のリトライ処理を実装。

検知モデルはpreprocessor（前処理）とdetector（検知ロジック）に分離してpickle化し、GCSに保存。検知実行時にダウンロード・デシリアライズして使用後にメモリ破棄する動的ロード方式を採用することで、アプリケーションのデプロイなしに検知モデルを更新可能。データ形式変更時はpreprocessorのみ、検知アルゴリズム改良時はdetectorのみを更新すれば済む分離設計が、運用ライフサイクルの独立性を実現している。

監査エージェント開発への示唆として、このアーキテクチャはLangGraphベースの監査エージェントにおけるワークフロー管理・エラーハンドリング・モデルデプロイ分離の設計パターンとして参考になる。特に双方向コールバックパターンは、長時間実行の検知タスクと結果永続化を担うAPIサーバを分離する際の実装指針として活用できる。

## アイデア

- 双方向gRPCコールバックパターン：検知依頼側（Cloud Run Job）と結果受信側（Controller）を分離することで、バッチプロセスがデータ中継役を担う無駄を排除しつつ、数万件規模の検知結果のメモリ効率を改善する設計
- Workflowのステータスから失敗箇所を自動判定する設計：ControllerはWorkflowから「どのステップで失敗したか」を受け取らず、自身の現在のステータスから失敗箇所を特定する。これにより、Workflow側のエラー情報設計を簡素化できる
- preprocessor/detectorを分離したpickle動的ロード：アプリデプロイとモデル更新のライフサイクルを完全分離し、データ形式変更と検知アルゴリズム改良の影響範囲をそれぞれ独立して管理できる運用設計

## 前提知識

- **gRPC** → /deep_971 「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回
- **Google Cloud Workflows** (TODO: 読むべき)
- **Cloud Run Job** (TODO: 読むべき)
- **pickle直列化** (TODO: 読むべき)
- **ステートマシン** → /deep_2951 CodeRouterの内側 — Anthropic⇄OpenAI双方向翻訳とmid-streamセーフなフォールバック設計

## 関連記事

- /deep_2698 説明可能な金融不正検知のためのShapley値ガイド型適応アンサンブル学習と米国規制コンプライアンス検証
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ
- /deep_875 増分・分散グラフモデリングによる複雑なマネーロンダリングパターンの検出
- /deep_2551 因果推論の本質①：相関と因果 ─ なぜ区別が必要か
- /deep_1792 モンテカルロシミュレーションの数理とPython実装 -- 幾何ブラウン運動で株価の未来を確率的に予測する

## 原文リンク

[Stena Expenseの検知アーキテクチャ ── Go × Python × gRPCで不正検知を実現する仕組み](https://zenn.dev/chillstack/articles/2026-04-20-detection-architecture-stena-expense)
