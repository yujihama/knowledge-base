---
title: "AIエージェント時代の「ファイルシステム終焉」論——Oracle AI Database 26ai"
url: "https://zenn.dev/tadkud/articles/2026-04-02_oracle-ai-db-26ai-multimodal-agent"
date: 2026-05-28
tags: [Oracle 26ai, RAG, VECTOR型, ハイブリッド検索, DBMS_VECTOR_CHAIN, MCP, Select AI, マルチモーダル, LangChain]
category: "agent-arch"
related: [4335, 5027, 2360, 4520, 1784]
memo: "[Zenn LLM] AIエージェント時代の「ファイルシステム終焉」論——Oracle AI Database 26ai"
processed_at: "2026-05-28T21:01:49.982953"
---

## 要約

Oracle AI Database 26aiは、Oracle Database 23aiの後継として2025〜2026年にリリースされたバージョンで、AI機能をファーストクラスとして扱う初めてのOracleメジャーバージョンである。主要機能は4点に整理できる。①VECTOR型＋ハイブリッド検索：23aiで導入されたVECTOR型を拡張し、Oracle Textによる全文検索とベクトル類似度検索をSQLのWHERE句で混在させるハイブリッド検索を実現。コサイン距離スコアと全文スコアを重み付け（ベクトル70%、全文30%等）して統合ランキングを生成でき、RAGパターンをSQL一本で完結させられる。②DBMS_VECTOR_CHAIN：埋め込み生成→類似チャンク検索→LLM呼び出し（GPT-4o等）→回答生成のRAGパイプライン全体をPL/SQL内部で定義できるパッケージ。PythonアプリからはLangChainやLlamaIndexのOracleコネクタ経由で同パイプラインを呼び出せる。③マルチモーダル対応：DBMS_VECTOR_CHAIN.UTL_TO_CHUNKSにより、PDFや画像をBLOBとしてDBに格納しながらAIチャンク化（単語数200、オーバーラップ20等のパラメータ指定）を自動実行。「S3→Lambda前処理→OpenSearch Serverless」という従来のパイプラインがDBへのINSERTで完結する。④AIエージェント連携：Select AI機能が拡張され、自然言語クエリをSQLに変換（action='narrate'で結果を自然言語返答、action='runsql'で生SQL返答）。さらに@oracle/mcp-server-oracleによるMCPサーバ公式実装により、Claude CodeやCursorなどのAIエージェントから直接DB操作が可能。LangChainのOracleVSを使うと、接続エンドポイントがOracleDB一つに集約され、トランザクション管理・RBAC・監査ログを既存DB運用ノウハウで一元管理できる。「ファイルシステム終焉」の現実解は棲み分けであり、AI推論に使うデータ（RAG知識ベース、LLMコンテキスト）はOracle 26aiのVECTOR型に直接格納し、大容量バイナリ（動画、大規模CSV）はS3等のオブジェクトストレージ＋Oracle External Tablesで扱うという設計が推奨される。監査エージェント開発への示唆として、DB内RAGパイプライン＋MCPサーバの組み合わせは、監査証跡・アクセス制御・ベクトル検索を単一DBレイヤで完結させる構成として有力な選択肢となる。

## アイデア

- RAGパイプライン（埋め込み→検索→LLM呼び出し）をPL/SQL内部で完結させるDBMS_VECTOR_CHAINは、Pythonアプリ側のオーケストレーション層を薄くしつつ、DBのトランザクション保証・監査ログを自動的に享受できる設計思想が興味深い
- MCPサーバ公式実装により、Claude CodeなどのAIエージェントがDB関数をToolとして直接呼び出せる構成は、エージェントのツール定義とデータアクセス層を統合する新しいアーキテクチャパターンを示している
- ハイブリッド検索でコサイン距離スコアと全文検索スコアを重み付け合算する手法は、キーワード的な一致精度と意味的類似度を同時に最適化でき、監査文書検索のような専門用語が重要なユースケースで特に有効

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **ベクトル検索** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **LangChain** → /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- **PL/SQL** (TODO: 読むべき)

## 関連記事

- /deep_4335 RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法
- /deep_5027 Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】
- /deep_2360 NLP2026 参加報告：言語処理学会第32回年次大会レポート
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ

## 原文リンク

[AIエージェント時代の「ファイルシステム終焉」論——Oracle AI Database 26ai](https://zenn.dev/tadkud/articles/2026-04-02_oracle-ai-db-26ai-multimodal-agent)
