---
title: "ParquetのContent-Defined Chunking（CDC）によるHugging Face Hub上のデータ転送最適化"
url: "https://huggingface.co/blog/parquet-cdc"
date: 2026-04-07
tags: [Parquet, PyArrow, HuggingFace, CDC, Xet, データ重複排除, コンテンツ定義チャンキング, Pandas]
category: "infra"
memo: "[HF Blog] Parquet Content-Defined Chunking"
processed_at: "2026-04-07T12:17:56.694653"
---

## 要約

Hugging Face Hubは現在約21PBのデータセットをホストしており、そのうちParquetファイルだけで4PB以上を占める。この大規模ストレージを効率化するため、HuggingFaceは新ストレージ層「Xet」を導入し、コンテンツ定義チャンキング（CDC）によるデータ重複排除を実現した。さらにApache ArrowのPyArrow 21.0.0以降では、Parquetファイル書き込み時に`use_content_defined_chunking=True`を指定することで、Xetストレージとの連携を最適化できるParquet CDC機能が利用可能になった。

従来のParquetはカラム指向圧縮により、データに僅かな変更が加わるだけでバイト列表現が大きく変わるため、CDCによる重複排除効率が低下する問題があった。Parquet CDCはこの問題を解決するため、データページ（カラムチャンク）の書き出し方を制御し、変更のない部分のバイト列が可能な限り一致するよう最適化する。

具体的なユースケース別の効果として以下が示された：①同一データの再アップロードは転送量0（96.1MBが0転送）、②カラム追加・削除は変更カラム分のみ転送（追加列の8MBのみ）、③カラム型変更も変更カラム分のみ、④末尾への行追加は追加行相当のみ転送、⑤行の挿入・削除では変更行以降のチャンクが影響を受けるが大幅削減、⑥行グループサイズ変更では一定の影響あり、⑦ファイル分割パターン変更は転送量増加のリスクあり。重複排除はリポジトリを横断して機能するため、同一データを複数リポジトリで共有する際もデータ転送が発生しない。

Pandasからも`df.to_parquet(path, use_content_defined_chunking=True)`で同機能が利用可能。PyArrow 21.0.0からはHugging FaceのURIスキーム（`hf://`）を直接サポートしており、HubへのParquet読み書きがネイティブに行える。

## アイデア

- コンテンツ定義チャンキングはファイル単位ではなくバイト列の内容に基づいてチャンク境界を決定するため、部分更新が多いデータセットの差分転送に非常に効果的
- 重複排除がリポジトリ横断で機能する点は、監査データのような機密性の高い類似データセットを複数環境で管理する際のストレージコスト削減に直結する
- 行の挿入・削除はその後のチャンク境界にも影響するため、追記（append）パターンの設計がCDC効率最大化の鍵になる
## 関連記事

- /deep_771 チャンクからブロックへ：Hugging Face Hubにおけるアップロード・ダウンロードの高速化
- /deep_900 ファイルからチャンクへ：HuggingFaceストレージ効率の改善
- /deep_713 XetストレージがHugging Face Hubに導入された：LFSからコンテンツ定義チャンキングへの移行
- /deep_904 Hugging Face HubでオープンなMLデータセットを共有する方法
- /deep_402 Hugging Face Hub に Storage Buckets が登場 — S3ライクなミュータブルオブジェクトストレージ

## 原文リンク

[ParquetのContent-Defined Chunking（CDC）によるHugging Face Hub上のデータ転送最適化](https://huggingface.co/blog/parquet-cdc)
