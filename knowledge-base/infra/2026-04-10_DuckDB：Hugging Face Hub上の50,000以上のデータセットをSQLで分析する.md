---
title: "DuckDB：Hugging Face Hub上の50,000以上のデータセットをSQLで分析する"
url: "https://huggingface.co/blog/hub-duckdb"
date: 2026-04-10
tags: [DuckDB, Parquet, HuggingFace, データセット分析, httpfs, SQL, Dataset Viewer]
category: "infra"
memo: "[HF Blog] DuckDB: analyze 50,000+ datasets stored on the Hugging Face Hub"
processed_at: "2026-04-10T09:43:36.621834"
---

## 要約

Hugging Face HubがDuckDBとの統合機能を追加し、Hub上に公開されているすべてのデータセットに対してSQLクエリを直接実行できるようになった。2023年6月時点で50,000以上のデータセットが対象。

技術的な仕組みとして、HubのDataset Viewerがすべての公開データセットを自動的にParquetファイルに変換・公開している。Parquetは列指向フォーマットであり、大規模データの保存・読み込み・分析に効率的。大きなデータセットは500MBチャンク単位でシャーディングされる。

利用手順は以下の通り。①`https://datasets-server.huggingface.co/parquet?dataset=<dataset_name}`エンドポイントへHTTPリクエストを送り、ParquetファイルのURLリストを取得する。②DuckDBのPythonクライアントで接続を作成し、`httpfs`拡張をインストール・ロードすることでリモートファイルの読み書きを可能にする。③取得したURLを直接SQL文のFROM句に指定してクエリを実行する。追加のデータロード処理は不要で、リモートParquetファイルに対してオーバーヘッドなしにSQL解析が実行できる。

具体的なコード例として、`blog_authorship_corpus`データセットに対して星座（horoscope）別のブログ記事数と平均文字数を集計するSQLクエリが示されている。DuckDBは複数のParquetファイルへのクエリも対応しており、シャーディングされた大規模データセットも扱える。

この機能の背景として、LLM時代に大規模データセットが増加しており、Falcon・Dolly・MPT・StarCoderなどの学習データとして使われたデータセットの中身を把握することがモデル品質管理に直結する。SQLはStackOverflow 2022年調査で第3位の人気言語であり、幅広いユーザーがデータ探索できる環境を提供することが目的。

## アイデア

- リモートParquetファイルをダウンロードせずにSQL直接実行できる設計：httpfs拡張によりネットワーク越しにParquetを列指向で部分読み込みするため、数GBのデータセットでも必要カラムだけ取得でき、メモリ効率が高い
- 自動Parquet変換パイプライン：Hubがあらゆる形式のデータセットをParquetに統一変換・公開することで、利用者側のフォーマット変換コストをゼロにしつつ、分析ツールの互換性を最大化する設計思想
- 500MBシャーディング＋複数ファイルクエリのサポート：DuckDBが複数Parquetファイルへのユニオンクエリをネイティブサポートするため、大規模データセットを透過的に扱える点がバッチ分析基盤として実用的
## 関連記事

- /deep_945 HuggingFace Datasets に SQL コンソールを導入 — DuckDB WASM でブラウザ内クエリが可能に
- /deep_904 Hugging Face HubでオープンなMLデータセットを共有する方法
- /deep_521 ParquetのContent-Defined Chunking（CDC）によるHugging Face Hub上のデータ転送最適化
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング

## 原文リンク

[DuckDB：Hugging Face Hub上の50,000以上のデータセットをSQLで分析する](https://huggingface.co/blog/hub-duckdb)
