---
title: "LMCacheを使ったPrefill/Decode分離推論 on AWS - 構成解説編"
url: "https://zenn.dev/tosshi/articles/b9fdb42d36bd82"
date: 2026-04-17
tags: [vLLM, LMCache, PD分離推論, KV Cache, ElastiCache, Valkey, AWS ParallelCluster, 分散推論, Prefill, Decode]
category: "infra"
related: [1120, 419, 1434, 902, 2067]
memo: "[Zenn LLM] P/D Disaggregated Inference with LMCache - 1"
processed_at: "2026-04-17T12:09:27.233628"
---

## 要約

本記事は、vLLM + LMCache + AWS ElastiCache Serverlessを組み合わせてPrefill/Decode分離推論（PD分離推論）を実現する構成の解説記事（第1部）。PD分離推論とは、LLM推論のPrefillフェーズ（入力トークンの一括処理・KV Cache生成）とDecodeフェーズ（トークンの逐次生成）を別々のサーバーに分離するアーキテクチャ。Prefillサーバーはコンピュート集約型処理に、Decodeサーバーはメモリ帯域集約型処理に特化させることで、スループットと低レイテンシを両立する。KV Cacheの共有にはLMCache（vLLM向けKV Cache外部永続化ライブラリ）を使用。L1がローカルCPUメモリ、L2がAWS ElastiCache Serverless（Valkey 8.1）という2層キャッシュ構造を採用。vLLMの`--kv-transfer-config`オプションで`kv_role: kv_producer`（Prefill側）と`kv_role: kv_consumer`（Decode側）を指定することで役割を分担する。検証環境はAWS ParallelCluster 3.14.2 + Slurmで構築したg6.12xlarge（NVIDIA L4 GPU×4）1台に、PrefillサーバーとDecodeサーバーを同居（GPU 0-1をポート8100、GPU 2-3をポート8200に割り当て）。モデルはmeta-llama/Llama-3.1-8B-InstructをTP=2で実行。ElastiCacheとの接続はrediss://スキームでTLS暗号化、VPC内接続で約10msのレイテンシ。LMCache設定ではPrefillとDecodeで`chunk_size: 256`と`hash_algorithm: sha256_cbor_64bit`を必ず一致させる必要がある。CacheGenによるKV Cache圧縮はバグ回避のため`remote_serde: naive`で無効化。実際の動作確認では、Prefillサーバーに9トークンのプロンプトを送信後、同プロンプトでDecodeサーバーにリクエストすると、Decodeサーバーがエンジン内でのPrefill計算を0トークンに抑制し、ElastiCacheからKV Cacheをヒットさせることを確認。LMCacheはv0.4.2→0.4.3でsave_decode_cacheバグ修正やRESP認証環境変数サポートが追加されたが、SSL/TLS改善は未含有のため接続設定に追加考慮が必要。監査エージェントへの示唆としては、長いコンテキスト（監査証跡・規程文書等）のPrefillを一度実施してKV Cacheを共有し、複数のDecodeサーバーが並列に異なるクエリへ回答するアーキテクチャが考えられる。

## アイデア

- PrefillとDecodeを別プロセス・別GPUに分離することで、各フェーズの計算特性（Compute-bound vs Memory-bound）に最適化したハードウェア割り当てが可能になる
- LMCacheのL1（CPU Memory）+ L2（ElastiCache）の2層キャッシュ構造により、同一サーバー内の高速アクセスとサーバー間共有を両立している
- chunk_sizeとhash_algorithmをPrefill/Decode間で厳密に一致させないとキャッシュ取得が失敗するという制約は、分散KV Cacheの一貫性管理の難しさを示している

## 前提知識

- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル
- **KV Cache** → /deep_1019 Intel Gaudi向けAssisted Generation（投機的サンプリング）の高速化サポート
- **Tensor Parallelism** → /deep_589 GPU を無駄にしない: TRL における Co-located vLLM による効率化
- **Redis/Valkey** (TODO: 読むべき)
- **AWS ParallelCluster** (TODO: 読むべき)

## 関連記事

- /deep_1120 Intel® Gaudi® 2 AIアクセラレータ上でのテキスト生成パイプライン
- /deep_419 連続バッチ処理（Continuous Batching）をゼロから理解する
- /deep_1434 生成AIワークロードの電力プロファイル計測：データセンター全体インフラ計画のための手法
- /deep_902 日本語LLMオープンリーダーボードの公開
- /deep_2067 医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較

## 原文リンク

[LMCacheを使ったPrefill/Decode分離推論 on AWS - 構成解説編](https://zenn.dev/tosshi/articles/b9fdb42d36bd82)
