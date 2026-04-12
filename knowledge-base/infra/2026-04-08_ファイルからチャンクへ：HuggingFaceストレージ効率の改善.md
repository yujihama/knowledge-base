---
title: "ファイルからチャンクへ：HuggingFaceストレージ効率の改善"
url: "https://huggingface.co/blog/from-files-to-chunks"
date: 2026-04-08
tags: [Content-Defined Chunking, HuggingFace, Git LFS, ストレージ最適化, 重複排除, ローリングハッシュ, Xet]
category: "infra"
memo: "[HF Blog] From Files to Chunks: Improving HF Storage Efficiency"
related: [771, 713, 521, 402, 1572]
processed_at: "2026-04-08T21:10:53.126222"
---

## 要約

HuggingFace（HF）は2024年11月時点でモデル・データセット・Spacesを合わせて30PB超のデータをGit LFSリポジトリで管理している。Git LFSはファイル単位でバージョン管理するため、GGUFファイル（8GB超）やSafetensor（平均1GB）の一部変更でも全ファイルの再アップロードが必要となり、転送コストとストレージ膨張が課題だった。HFのXetチームはContent-Defined Chunking（CDC）という手法でこの問題に取り組む。CDCはファイルをバイト列として扱い、ローリングハッシュアルゴリズムでスライディングウィンドウ（例：4バイト幅）のハッシュを逐次計算し、「hash(data) % 2^12 == 0」のような条件を満たす境界でチャンク分割する。チャンクの内容はハッシュ化してContent-Addressed Store（CAS）に格納するため、同一チャンクは1回しか保存されない（重複排除）。ファイルに挿入・削除が発生しても、変化した部分のチャンクのみ新たに保存・転送するだけで済む。XetHubの旧実装でGit LFSと比較したベンチマークでは、COVID-19研究論文データセット「CORD-19」（50回の増分更新）において、平均ダウンロード時間51分→19分、平均アップロード時間47分→24分、ストレージ使用量8.9GB→3.52GBという結果を得た。HFHub上のopenai-community/gpt2のmodel.safetensorsファイル2バージョン（664MB＋548MB）に適用した試算では、合計ストレージをGit LFS比で1.2GB→645MBに53%削減できると推定。圧縮でさらに10%削減の余地もある。ファインチューニングモデルやモデルチェックポイントは変更範囲が限定的なため重複排除率30〜85%と高い効果が見込まれ、PyTorchチェックポイント約200TBに50%重複排除を適用すると即座に100TB、月次で7〜8TBの削減が期待できる。XetチームはPoCを進めており、2025年初頭にXetバックエンドのリポジトリ展開を計画していた（2025年2月に「From Chunks to Blocks」として続報あり）。

## アイデア

- ローリングハッシュによるデータ駆動の境界決定は、ファイル形式に依存せず汎用的に適用可能で、バイナリの大規模モデルファイルにも有効
- Content-Addressed Storeによるチャンク単位のアドレッシングは、ファインチューニング差分やチェックポイント間の変分を最小転送量で管理する仕組みとして応用範囲が広い
- CDC攻撃（意図的な境界操作によるデータ推測）への対策が未解決課題として残っており、セキュリティと効率のトレードオフが実運用上の論点になる

## 関連記事

- /deep_771 チャンクからブロックへ：Hugging Face Hubにおけるアップロード・ダウンロードの高速化
- /deep_713 XetストレージがHugging Face Hubに導入された：LFSからコンテンツ定義チャンキングへの移行
- /deep_521 ParquetのContent-Defined Chunking（CDC）によるHugging Face Hub上のデータ転送最適化
- /deep_402 Hugging Face Hub に Storage Buckets が登場 — S3ライクなミュータブルオブジェクトストレージ
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド

## 原文リンク

[ファイルからチャンクへ：HuggingFaceストレージ効率の改善](https://huggingface.co/blog/from-files-to-chunks)
