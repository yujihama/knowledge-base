---
title: "llm-d on Amazon EKS で Prefill/Decode Disaggregation 検証環境を構築する"
url: "https://zenn.dev/aws_japan/articles/eks-llm-d-pd-disaggregation"
date: 2026-05-11
tags: [PD-Disaggregation, llm-d, Amazon EKS, KV-Cache, NIXL, EFA, vLLM, Kubernetes, GPU推論, Qwen2.5]
category: "infra"
related: [419, 3099, 1691, 1936, 1060]
memo: "[Zenn LLM] llm-d on Amazon EKS で Prefill/Decode Disaggregation 検証環境を構築する"
processed_at: "2026-05-11T12:15:00.515221"
---

## 要約

本記事は、Kubernetes ネイティブな LLM 推論基盤プロジェクト「llm-d」を用いて、Amazon EKS 上に Prefill/Decode Disaggregation（PD 分離）構成の検証環境を構築する手順を詳細に解説している。

LLM の推論処理は KV Cache の扱いによって Prefill フェーズ（入力プロンプト全体を一括処理し、最初のトークンと KV Cache を生成する。GPU の演算能力をフルに活用する計算集約型）と Decode フェーズ（KV Cache を参照しながらトークンを1つずつ生成する。GPU-メモリ間のデータ転送がボトルネックになりやすいメモリ帯域幅依存型）に分かれる。従来は1台の GPU が両フェーズを処理していたが、計算特性が大きく異なるため互いに干渉し、TTFT や TPOT が低下する問題があった。PD Disaggregation はこの2フェーズを別ワーカーに分離することで、それぞれのリソースを最適化し、スループットとレイテンシを改善するアーキテクチャである。

構成の核心は、Prefill ワーカーで生成した KV Cache を Decode ワーカーへ高速転送する仕組みにある。本記事では NIXL（LLM 推論向け高速・低遅延転送抽象化ライブラリ）と AWS EFA（Elastic Fabric Adapter、OS カーネルバイパスによる低レイテンシ・高帯域ノード間通信）を組み合わせて実現している。

具体的な構成は Amazon EKS（eksctl で構築）、g6e.8xlarge × 2台（NVIDIA L40S 48GB × 1 each）、モデルは Qwen/Qwen2.5-1.5B-Instruct、KV Cache 転送は NIXL + LIBFABRIC（EFA バックエンド）、Gateway は Standalone Mode（Envoy サイドカー + Gateway API Inference Extension v1.5.0）。

手順は①EKS クラスター作成（efaEnabled: true、Placement Group cluster 戦略で同一 AZ 内近接配置）、②HuggingFace トークンを Kubernetes Secret として登録、③Gateway API Inference Extension CRD のインストール、④llm-d Router を Helm でデプロイ、⑤Kustomize カスタムオーバーレイで Prefill/Decode それぞれの Deployment を設定（replicas:1、tensor-parallel-size:1、NixlConnector、EFA 環境変数 FI_EFA_USE_DEVICE_RDMA=1 等）、⑥推論テストとなる。

デフォルトの llm-d Well-Lit Paths は gpt-oss-120b を 8 Prefill + 2 Decode という大規模構成を前提としているため、本記事ではカスタムオーバーレイ（ghcr.io/llm-d/llm-d-aws:v0.6.0 に EFA 対応 vLLM イメージ差し替え含む）を作成してハンズオン規模に適合させている点が実用的である。監査エージェントの推論基盤をスケールさせる際、長いプロンプト（長文の被監査資料等）処理の TTFT 改善に PD Disaggregation は直接適用可能な技術である。

## アイデア

- Prefill と Decode の計算特性の違い（compute-bound vs memory-bandwidth-bound）を物理的に別ノードへ分離することで、それぞれの GPU を最適な動作点で使用できる点。長文プロンプトを多用する監査エージェントでは TTFT 改善効果が特に大きい
- NIXL が LIBFABRIC バックエンドとして EFA を利用することで、KV Cache のノード間転送を OS カーネルバイパス（RDMA）で行う設計。転送レイテンシが推論全体のボトルネックになりうるため、ネットワーク層の選択がアーキテクチャ品質を左右する
- llm-d の Well-Lit Paths（Kustomize ベースのリファレンスアーキテクチャ）が本番規模（120B モデル）向けデフォルトを持ちつつ、カスタムオーバーレイで小規模検証環境へ容易に転用できる設計思想。インフラコードの再利用性と検証コストの低減を両立している

## 前提知識

- **KV Cache** → /deep_1019 Intel Gaudi向けAssisted Generation（投機的サンプリング）の高速化サポート
- **Transformer Self-Attention** (TODO: 読むべき)
- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル
- **Kubernetes / Kustomize** (TODO: 読むべき)
- **RDMA / EFA** (TODO: 読むべき)

## 関連記事

- /deep_419 連続バッチ処理（Continuous Batching）をゼロから理解する
- /deep_3099 LMCacheを使ったP/D分離推論 実装編：AWS ParallelCluster + ElastiCache Serverless構成
- /deep_1691 Kaggle自然言語処理コンペ向けローカルLLM活用入門
- /deep_1936 🤗 APIユーザー向けTransformer推論を100倍高速化した方法
- /deep_1060 簡潔な方が良い：関数呼び出しエージェントにおけるChain-of-Thoughtの非単調な予算効果

## 原文リンク

[llm-d on Amazon EKS で Prefill/Decode Disaggregation 検証環境を構築する](https://zenn.dev/aws_japan/articles/eks-llm-d-pd-disaggregation)
