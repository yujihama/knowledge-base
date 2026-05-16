---
title: "Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】"
url: "https://zenn.dev/agdexai/articles/llm-observability-tools-2026"
date: 2026-04-23
tags: [LLM Observability, Langfuse, LangSmith, Helicone, トレース, プロンプト管理, コスト追跡, Eval, セルフホスト, LangChain]
category: "infra"
related: [41, 858, 381, 398, 2255]
memo: "[Zenn LLM] Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】"
processed_at: "2026-04-23T12:11:16.247840"
---

## 要約

LLMアプリを本番運用する際に直面する「プロンプト起因の異常出力」「レイテンシ悪化」「APIコスト集中」といった問題を解決するLLM Observabilityツールの2026年時点における3製品比較。従来のAPMツール（Datadog、New Relic）はLLM特有の課題——プロンプトバージョン管理、マルチステップエージェントのトレース、トークンコスト分析、出力品質のEval——に対応していないため、専用ツールが必要となっている。

**Langfuse**はMITライセンスのOSSで、セルフホスト（Docker対応）とCloud両対応。Pythonデコレータ（@observe）によるトレース自動記録、LangChain/LlamaIndex統合、Eval・プロンプト管理・コスト追跡をフル装備。無料枠は5万イベント/月、有料プランは$59/月〜。データ主権を重視するチームや、LangChain以外のフレームワーク（LangGraph、Pydantic AgentなどReActベース実装）を使う場合の定番選択肢。

**LangSmith**はLangChain公式のプロプライエタリなCloudサービス。環境変数2行（LANGCHAIN_TRACING_V2=true、LANGCHAIN_API_KEY）を設定するだけでLangChainの全処理が自動トレースされるゼロ設定統合が最大の強み。ヒューマンフィードバック収集、データセット管理、評価パイプラインも備える。無料枠は5,000トレース/月と他ツールより少なく、セルフホスト不可。LangGraph中心プロジェクトで最短経路の可観測性を求める場合に最適。

**Helicone**はApache 2.0ライセンスで、OpenAI APIのbase_urlをHeliconeのプロキシURLに変更するだけでトレースが開始される「プロキシ方式」を採用。コード変更が最小限で済む一方、Eval機能やプロンプト管理は基本的なもののみ。リアルタイムコストモニタリング、APIキャッシュ（コスト削減）、レート制限管理が得意。無料枠は最初の10万リクエストで他ツールより大きい。エージェントの複雑なトレース分析には不向き。

監査エージェント開発への示唆：LangGraph＋Pydanticで構築したReActエージェントの本番監視にはLangfuseのセルフホストが最も適する。データを社内に閉じられる点が内部監査用途のコンプライアンス要件と整合する。LangSmithはLangGraph統合がネイティブで開発中の動作確認に使いやすいが、本番データをCloudに送ることへのガバナンス上の懸念がある。Heliconeはプロキシ方式のためエージェントの多段ステップ追跡には限界がある。

## アイデア

- Heliconeのプロキシ方式はbase_urlを1行変えるだけでトレースが開始される最小侵襲アーキテクチャで、既存コードへの影響なくオブザーバビリティを後付けできる設計思想が興味深い
- LangSmithの環境変数2行による自動トレースは、LangChainがフレームワーク内部にインスツルメンテーションポイントを埋め込んでいることで実現しており、フレームワーク側がObservabilityを設計の一部として扱っている点が他OSS LLMフレームワークとの差別化になっている
- Langfuseのセルフホスト＋MIT licenseの組み合わせは、金融・医療・監査など規制産業でのLLMアプリ本番運用においてデータ主権とコスト最適化を両立できる唯一の選択肢となりつつある

## 前提知識

- **LLM API** → /deep_409 Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法
- **OpenTelemetry / APM** (TODO: 読むべき)
- **LangChain / LangGraph** (TODO: 読むべき)
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **トークンコスト** (TODO: 読むべき)

## 関連記事

- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_381 LLMコスト爆発から『品質ファースト』へ：2026年企業のコスト×品質管理戦略
- /deep_398 LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）
- /deep_2255 The Colony に参加する LangChain エージェントを構築する

## 原文リンク

[Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】](https://zenn.dev/agdexai/articles/llm-observability-tools-2026)
