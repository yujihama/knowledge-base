---
title: "HuggingFace Datasets に SQL コンソールを導入 — DuckDB WASM でブラウザ内クエリが可能に"
url: "https://huggingface.co/blog/sql-console"
date: 2026-04-08
tags: [DuckDB, DuckDB-WASM, Parquet, HuggingFace-Hub, データセット前処理, SQL]
category: "infra"
memo: "[HF Blog] Introducing the SQL Console on Datasets"
processed_at: "2026-04-08T21:35:48.059841"
---

## 要約

Hugging Face は 2024年9月、Hub 上のデータセットに対してブラウザから直接 SQL クエリを実行できる「SQL Console」を公開した。バックエンド不要で動作し、DuckDB WASM（WebAssembly）をエンジンとして採用することで、ユーザーのローカル環境（ブラウザ内）でクエリ処理を完結させる設計になっている。

技術的な仕組みとして、Hub 上のデータセットは多くが Parquet 形式で保存されており、SQL Console はこれらの Parquet ファイルを直接読み込んでビューを生成する。Parquet 以外の形式のデータセットについては、最初の 5GB が自動的に Parquet に変換される。DuckDB WASM はブラウザの WebAssembly ランタイム上で動作するインプロセス DB エンジンであり、サーバーや外部依存なしにフル SQL 構文（PostgreSQL に近い）、正規表現・リスト・JSON・Embedding 向けの組み込み関数を利用できる。

主な機能は4点：(1) 100% ローカル実行（DuckDB WASM）、(2) DuckDB のフル SQL 構文サポート、(3) クエリ結果の Parquet エクスポート、(4) パブリックデータセットのクエリ結果をリンクで共有可能。制約としてはメモリ上限が約 3GB であること、DuckDB WASM では `hf://` プロトコルによるデータセット参照が未サポートである点がある。

実用例として、1,260万行を持つ OpenCo7/UpVoteWeb データセットへのフィルタクエリが 3 秒未満で完了したことが示された。また、LLM ファインチューニング用データの前処理として一般的に Python スクリプトで行われる「Alpaca 形式 → 会話形式への変換」を、SQL Console 上で `struct_pack` 関数を使った SQL クエリのみで 30 秒以内に実現するデモが公開されている。他にも、関数呼び出しデータセットの正規表現フィルタリング、Embedding を用いた類似検索、open-llm-leaderboard からのベースモデル人気度集計など、多様なユースケースが「SQL Snippets」スペースにまとめられている。

## アイデア

- DuckDB WASM によりサーバーレス・依存ゼロでブラウザ内データ処理が完結する設計は、セキュリティ要件の厳しい環境（監査法人など）でのデータ探索ツールとして参考になるアーキテクチャパターン
- Embedding カラムへの類似検索クエリが SQL で書けるため、RAG パイプラインのデータセット評価・フィルタリングをノーコードで試せる点が興味深い
- SQL で LLM ファインチューニング用データのフォーマット変換（Alpaca → 会話形式）が完結するユースケースは、Python 前処理スクリプトの代替として再現性・共有性が高い
## 関連記事

- /deep_1355 DuckDB：Hugging Face Hub上の50,000以上のデータセットをSQLで分析する
- /deep_904 Hugging Face HubでオープンなMLデータセットを共有する方法
- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け
- /deep_521 ParquetのContent-Defined Chunking（CDC）によるHugging Face Hub上のデータ転送最適化

## 原文リンク

[HuggingFace Datasets に SQL コンソールを導入 — DuckDB WASM でブラウザ内クエリが可能に](https://huggingface.co/blog/sql-console)
