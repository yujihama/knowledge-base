---
title: "StatefulMCPサーバーで社内データ分析エージェントを構築する"
url: "https://zenn.dev/0h_n0/articles/d759354462a484"
date: 2026-06-12
tags: [MCP, FastMCP, SQLite, チェックポイント, Stateful, 非同期タスク管理, LangGraph, aiosqlite, WAL]
category: "agent-arch"
related: [7417, 6357, 4177, 6412, 2365]
memo: "[Zenn LLM] Stateful MCPサーバーで社内データ分析エージェントを構築する"
processed_at: "2026-06-12T09:03:44.638719"
---

## 要約

本記事は、MCP（Model Context Protocol）のセッション管理とTasks拡張を活用し、社内データ分析エージェント向けのStatefulサーバーをPython + FastMCPで実装する手法を解説する。

StatelessなMCPサーバーでは、「先月の売上を部門別に集計」のような複数ステップ処理（SQLクエリ生成・実行・集計・可視化）の途中でネットワーク断やサーバー再起動が発生した場合、全処理をやり直す必要がある。これを解決するためにStateful設計が必要となる。

【MCPセッション管理の進化】
- 2025-03-26仕様: Mcp-Session-IdヘッダーによるStreamable HTTPセッション識別
- 2025-11-25仕様: Tasks拡張（実験的）で非同期タスク管理・5状態ステートマシン（working/input_required/completed/failed/cancelled）
- 2026-07-28 RC: プロトコルレベルのセッション廃止、Statelessコアへ移行し、ツールからハンドルを発行してモデルが引数として渡す設計へ

【3層状態管理アーキテクチャ】
- L1（インメモリdict）: アクティブなツール実行の一時状態、TTLはリクエスト中
- L2（SQLite）: タスクチェックポイント、TTL 24時間、ACID準拠、単一インスタンス向け
- L3（Redis、オプション）: 分散セッション情報、水平スケール時のセッション共有

【実装の要点】
FastMCPのlifespan APIでDB接続をサーバー起動時に初期化・シャットダウン時に解放し、各ツールはContextオブジェクト経由でアクセスする。CheckpointStoreクラスはaiosqliteを用い、PRAGMA journal_mode=WALを有効化して読み書き競合（database is lockedエラー）を回避する。WALファイル肥大化防止のため定期的なPRAGMA wal_checkpoint(TRUNCATE)実行を推奨。SQLクエリ実行ツール（run_analysis_query）はtask_idを引数に受け取り、既存チェックポイントがあればCompletedステータスを確認して結果を即時返却し、途中経過（step単位）をSQLiteに保存しながら処理を進める。

【報告されている効果】
- 長時間実行エージェント（4時間超）のタスク失敗リスクが状態永続化なし比で90%低減（Indium Tech, 2026）
- チェックポイントベース状態管理により全履歴注入比でトークン使用量最大90%削減（Fastio, 2026）
- temporal reasoning精度47%・未知状況でのタスク完了率38%改善（同上）

監査エージェント開発への示唆：LangGraphベースの監査エージェントで長時間バッチ処理（大量仕訳のリスク評価など）を行う際、同様の3層チェックポイント設計を適用することで、処理中断時のリカバリコストを大幅に削減できる。また、2026-07-28 RC仕様のStatelessコア移行を見越したハンドルベース設計への移行準備も重要。

## アイデア

- MCPのTasks拡張における5状態ステートマシン（working/input_required/completed/failed/cancelled）は、監査エージェントのワークフロー状態管理に直接応用可能な設計パターン
- 2026-07-28 RC仕様でプロトコルレベルのセッションを廃止しStatelessコアに移行する方針は、セッション管理の責任をサーバーからツール（ハンドル発行）とモデル（引数として渡す）に分散する設計思想の転換点
- L1（インメモリ）/L2（SQLite）/L3（Redis）の3層分離により、単一インスタンスから水平スケールまでを段階的に対応できる設計は、本番運用での段階的拡張に実用的

## 前提知識

- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **FastMCP** → /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- **asyncio/async-await** (TODO: 読むべき)
- **SQLite WAL** (TODO: 読むべき)
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_7417 ローカルLLMで「PoC止まり」にしない業務AIエージェント ― MCP＋RAG評価まで一気通貫
- /deep_6357 LLMの拡張標準「MCP (Model Context Protocol)」入門：Pythonでカスタムサーバーを構築する
- /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- /deep_6412 コンテキストエンジニアリングは7要素の組み合わせ ── 構成図で見る全体像
- /deep_2365 kintoneのAPIドキュメントは1ページ53,600トークン — AIエージェントのトークン浪費を実測した

## 原文リンク

[StatefulMCPサーバーで社内データ分析エージェントを構築する](https://zenn.dev/0h_n0/articles/d759354462a484)
