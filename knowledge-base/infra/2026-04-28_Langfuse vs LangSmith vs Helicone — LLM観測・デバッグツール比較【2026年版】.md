---
title: "Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】"
url: "https://zenn.dev/agdex_ai/articles/8c0982b51e930d"
date: 2026-04-28
tags: [LLM Observability, Langfuse, LangSmith, Helicone, トレース, プロンプト管理, Eval, コスト追跡, LangChain, セルフホスト]
category: "infra"
related: [41, 858, 381, 398, 3096]
memo: "[Zenn LLM] Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】"
processed_at: "2026-04-28T12:34:06.279815"
---

## 要約

LLMアプリを本番運用する際に直面する「プロンプト品質の劣化」「レイテンシ悪化」「APIコスト集中」といった課題を解決するLLM Observabilityツール3種を比較した記事。従来のAPMツール（Datadog、New Relic）はプロンプトバージョン管理・マルチステップトレース・トークンコスト分析・出力品質評価といったLLM固有の要件に対応できないため、専用ツールが必要となる。

**Langfuse**はMITライセンスのOSSで、Dockerによるセルフホストが可能。トレース・プロンプト管理・Eval・コスト追跡をフルカバーし、Python/TypeScript SDKに加えLangChain・LlamaIndex統合を提供。`@observe`デコレータを付与するだけで関数実行が自動トレースされる。無料枠は月5万イベント、Cloud Proは月$59〜。

**LangSmith**はLangChain公式のプロプライエタリ製品で、環境変数2つ設定するだけでLangChainの全処理を自動トレースできる「ゼロ設定統合」が最大の強み。ヒューマンフィードバック収集・データセット管理・評価パイプラインを備える。現時点ではCloudのみでセルフホスト不可。無料枠は月5,000トレース、Plusは月$39。

**Helicone**はApache 2.0ライセンスで、OpenAI APIのBaseURLを`https://oai.helicone.ai/v1`に変更するだけでトレースが始まる「プロキシ方式」が特徴。リアルタイムコストモニタリング・キャッシュ機能（コスト削減）・レート制限管理を提供するが、詳細なプロンプト管理やEvalは限定的。無料枠は最初の10万リクエスト、Growthプランは月$20〜。

選定指針として、セルフホスト必須またはフルOSSならLangfuse、LangGraph中心プロジェクトならLangSmith、素早い立ち上げやコスト管理重視ならHeliconeが推奨される。監査エージェント開発（LangGraph + ReAct構成）においては、LangSmithのネイティブLangGraph統合とEvalパイプラインが有力候補。ただしデータの外部送信が監査上の懸念となる場合はLangfuseのセルフホスト構成が適切。

## アイデア

- Heliconeのプロキシ方式はコード変更ゼロ（BaseURL変更のみ）でトレース開始できる点が特異的で、既存コードへの侵襲性を最小化したい場合の設計パターンとして参考になる
- LangfuseのMITライセンス＋Dockerセルフホストの組み合わせは、データ主権が重要な監査・金融・医療領域でのLLM本番運用における観測基盤として実用的な選択肢を提供する
- LangSmithの「環境変数2つでLangChain全処理を自動トレース」という設計は、フレームワーク側がobservability hookを標準装備することでSDK利用者の計装コストをゼロにするアーキテクチャアプローチの具体例

## 前提知識

- **LLM Observability** → /deep_398 LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）
- **OpenTelemetry / APM** (TODO: 読むべき)
- **LangChain / LangGraph** (TODO: 読むべき)
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **トークンコスト管理** (TODO: 読むべき)

## 関連記事

- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_381 LLMコスト爆発から『品質ファースト』へ：2026年企業のコスト×品質管理戦略
- /deep_398 LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）
- /deep_3096 そのAIアプリはテストされているか：LLMアプリの自動テスト実践論

## 原文リンク

[Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】](https://zenn.dev/agdex_ai/articles/8c0982b51e930d)
