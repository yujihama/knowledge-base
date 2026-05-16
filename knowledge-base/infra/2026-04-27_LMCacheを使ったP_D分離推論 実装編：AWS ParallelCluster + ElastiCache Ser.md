---
title: "LMCacheを使ったP/D分離推論 実装編：AWS ParallelCluster + ElastiCache Serverless構成"
url: "https://zenn.dev/tosshi/articles/787683d9455ec8"
date: 2026-04-27
tags: [vLLM, LMCache, P/D分離推論, AWS ParallelCluster, ElastiCache, Slurm, Llama-3.1-8B, FSx Lustre, EFA, Docker, KVキャッシュ, Redis]
category: "infra"
related: [2101, 2590, 524, 832, 419]
memo: "[Zenn LLM] P/D Disaggregated Inference with LMCache - 2"
processed_at: "2026-04-27T12:17:22.702970"
---

## 要約

本記事はP/D Disaggregated Inference（Prefill/Decode分離推論）の実装編として、AWS上でLMCacheとvLLMを組み合わせた実験環境の構築手順を詳細に解説する。インフラはAWS ParallelClusterを用いたHPCクラスター構成で、GPUインスタンスとしてg5.12xlarge（NVIDIA A10G x4搭載）を2ノード固定（MinCount=MaxCount=2）で確保し、EFA（Elastic Fabric Adapter）を有効化してノード間通信を高速化している。ヘッドノードはm5.16xlargeのCPU専用構成で、Slurmスケジューラーを使用してGPUジョブを投入する。

KVキャッシュのリモートストレージにはAWS ElastiCache Serverlessを採用し、Redisプロトコル（rediss://）でLMCacheからアクセスする設定を行う。デプロイスクリプトにより自動的にエンドポイントが払い出され、FSx for Lustreの共有ストレージ（/fsx）経由で各計算ノードに環境変数を配布する仕組みとなっている。

モデルはmeta-llama/Llama-3.1-8B-InstructをHugging Face Hubからスナップショットダウンロードし、FSx Lustre上に配置する。推論サーバーはDockerコンテナで動作し、PrefillサーバーとDecodeサーバーをそれぞれ別GPUに割り当てる構成（GPU 0=Prefill, GPU 1=Decode, TP=1）をsingle nodeで試す形から開始している。Slurmのsbatchでジョブを投入し、LMCache v0.4.3とrediss URLを使ったスクリプト（run_disagg_lmcache_0.4.3_rediss_url.sh）を実行する。

ストレージ構成はFSx for Lustre（モデル・ログ用）とFSx for OpenZFS（ホームディレクトリ用）の二層構成で、モデルファイルやジョブログを永続化している。CloudWatchログとGrafanaダッシュボードによる監視も有効化されており、本番移行時の観測可能性も考慮された設計となっている。今後はSageMaker Hyperpod EKS構成への移行を予定しており、マルチノードP/D分離推論の実験へ発展させる計画が示されている。監査エージェント観点では、LLM推論のインフラ分離・スケーリング手法として、大規模バッチ処理や長文コンテキスト処理の効率化に直接応用できるアーキテクチャパターンを提供している。

## アイデア

- ElastiCache ServerlessをRedisプロトコル（rediss://）でKVキャッシュのリモートストレージとして使うことで、PrefillノードとDecodeノード間のKVキャッシュ転送をマネージドサービスに委譲し、運用負荷を下げる設計は実用的
- MinCount=MaxCount=2でSlurmの自動スケールダウンを無効化し容量を常時確保する手法は、推論レイテンシを安定させるために重要で、コスト最適化と応答性のトレードオフを明示している点が示唆深い
- ヘッドノード（CPU）とGPUコンピュートノードを完全分離し、EFAによる高速ノード間通信とFSx Lustre共有ストレージを組み合わせることで、単一ノードから将来のマルチノードP/D分離へスムーズに拡張できるアーキテクチャ設計になっている

## 前提知識

- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル
- **P/D Disaggregated Inference** (TODO: 読むべき)
- **LMCache** → /deep_2101 LMCacheを使ったPrefill/Decode分離推論 on AWS - 構成解説編
- **AWS ParallelCluster** → /deep_2101 LMCacheを使ったPrefill/Decode分離推論 on AWS - 構成解説編
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義

## 関連記事

- /deep_2101 LMCacheを使ったPrefill/Decode分離推論 on AWS - 構成解説編
- /deep_2590 ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成
- /deep_524 NVIDIA NIMでHugging Face上の10万以上のLLMを高速デプロイ
- /deep_832 Bamba: 推論効率に優れたハイブリッドMamba2モデル
- /deep_419 連続バッチ処理（Continuous Batching）をゼロから理解する

## 原文リンク

[LMCacheを使ったP/D分離推論 実装編：AWS ParallelCluster + ElastiCache Serverless構成](https://zenn.dev/tosshi/articles/787683d9455ec8)
