---
title: "Hugging Face HubでオープンなMLデータセットを共有する方法"
url: "https://huggingface.co/blog/researcher-dataset-sharing"
date: 2026-04-08
tags: [HuggingFace, データセット共有, DuckDB, Parquet, データストリーミング, オープンデータ, SQLコンソール]
category: "infra"
memo: "[HF Blog] Share your open ML datasets on Hugging Face Hub!"
related: [1355, 1213, 521, 945, 1572]
processed_at: "2026-04-08T21:12:59.314310"
---

## 要約

Hugging Face Hubは、機械学習研究者や開発者がデータセットを公開・共有するためのプラットフォームとして、Nvidia・Google・Stanford・NASA・Barcelona Supercomputing Centerなど主要な研究機関・企業に採用されている。本記事では、Hubが提供する主要機能を体系的に紹介している。

【ストレージと転送】テラバイト規模のデータセットに対応し、現行のファイルあたり上限50GBはXetチームの開発中バックエンド更新により500GBへ拡張予定。データセットのストリーミング機能により、全ファイルをダウンロードせずに大規模データセットを利用可能。

【データセットビューア】ブラウザ上でデータを直接探索できるUIを提供。音声・画像・動画などのモダリティとCSV・JSON・Parquetなどのフォーマットをサポート。全文検索やカラムヘッダーによるソート機能を内蔵。63,400行のarXiv論文を含むArxiverデータセットのような大規模データも効率的に検索可能。

【サードパーティライブラリ連携】Pandas（月間2億5,800万PyPiダウンロード）、Spark（2,900万）、🤗 Datasets（1,700万）、Dask（1,200万）、Polars（850万）、DuckDB（600万）など主要ライブラリと統合。`hf://datasets/`プレフィックスを使った1行のコードでデータ読み込みが可能。

【SQLコンソール】DuckDBの完全なSQL構文をブラウザ内で実行できるインタラクティブエディタ。正規表現・リスト・JSON・埋め込みベクトルなどの組み込み関数を利用可能。クエリ結果の共有・埋め込みもワンクリックで対応。

【セキュリティ】アクセス制御は「公開」「非公開」「ゲート付き（自動承認/手動承認）」の3段階。マルウェアスキャン・シークレットスキャン・Pickleファイルスキャン・ProtectAIによるGuardianセキュリティ技術を組み合わせた多層防御を実装。

【リーチと可視性】500万人以上のビルダーがアクティブに利用するプラットフォームで、データセットごとのディスカッションタブ・組織アカウント・リーダーボード機能によりコミュニティエンゲージメントを促進。

## アイデア

- DuckDB統合によりブラウザ上でSQL分析が完結する点は、データ前処理パイプラインの設計を大きく変える可能性がある（ローカル環境不要）
- ゲート付きデータセット機能により、規制産業（金融・監査等）での機密性の高いデータの制限付き共有が実現可能
- ストリーミング機能を活用すれば、テラバイト規模の訓練データを全量ダウンロードせずにサンプリング・プロトタイピングが可能
## 関連記事

- /deep_1355 DuckDB：Hugging Face Hub上の50,000以上のデータセットをSQLで分析する
- /deep_1213 Prodigy-HFの紹介：Hugging Faceとの直接統合
- /deep_521 ParquetのContent-Defined Chunking（CDC）によるHugging Face Hub上のデータ転送最適化
- /deep_945 HuggingFace Datasets に SQL コンソールを導入 — DuckDB WASM でブラウザ内クエリが可能に
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド

## 原文リンク

[Hugging Face HubでオープンなMLデータセットを共有する方法](https://huggingface.co/blog/researcher-dataset-sharing)
