---
title: "分散AIプラットフォームChutesとBittensorで始めるDePIN推論基盤"
url: "https://zenn.dev/taumu/articles/6d84f856d818b8"
date: 2026-04-13
tags: [DePIN, Bittensor, Chutes, 分散推論, TEE, Proof-of-Intelligence, TAO, サーバーレス, GPU分散, Sovereign AI]
category: "infra"
related: [251, 484, 1173, 1120, 408]
memo: "[Zenn LLM] はじめよう分散AIプラットフォーム with Chutes"
processed_at: "2026-04-13T12:23:11.838103"
---

## 要約

生成AIの推論基盤がAWS・Azure・GCPなどハイパースケーラに集中する現状に対し、第三の選択肢として「DePIN（Decentralized Physical Infrastructure Networks）」が台頭している。本記事ではBittensorネットワーク上の分散型サーバーレスAI推論プラットフォーム「Chutes」を通じてその実態を解説する。

ChutesはRayon Labsが運営し、1日約1,000億トークン・月間約3兆トークンを処理する。これはGoogleの前年NLPスループットの約3分の1に相当する規模であり、世界2,100以上のノード（NVIDIA H100/A100搭載）が支えている。コスト面ではAWS比約85%削減を実現しており、余剰GPUリソースを市場原理で動員する構造的優位性による。

基盤となるBittensorはPolkadotのSubstrateフレームワーク上に構築されたブロックチェーン（Subtensor）を中核とし、Proof-of-Stake（PoS）とProof-of-Intelligence（PoI）を組み合わせたハイブリッドコンセンサスを採用。ネイティブトークンTAO（τ）をマイナー（計算リソース提供者）とバリデーター（品質評価者）に自動配布する。ネットワーク内には特定AIタスクに特化した「サブネット」が多数存在し、Chutesはサブネット64として位置づけられる。

Rayon LabsはChutesに留まらず垂直統合的なエコシステムを構築しており、Gradients（SN56：RLHF等の重い学習タスク）、Nineteen（SN19：画像生成等の低遅延推論）を組み合わせ、AI開発の全ライフサイクルをカバーする。

Chutesの収益モデルは、多くのサブネットがネットワーク排出（Emissions）のみに依存する中、実サービス利用料に基づく外部収益を確立している点が特徴的で、投機でなく実需に根ざした持続可能性を志向する。

データ主権面では、Trusted Execution Environments（TEE）を導入し、ハードウェアレベルでの計算隔離・暗号化を実現。Qwen3・DeepSeek V3・MiniMaxなどの主要モデルでTEE対応版を提供し、機密データを分散ネットワーク上で安全処理できる。また許可不要のオープンプロトコルにより、政治的判断や法規制による検閲耐性（Sovereign AI）も実現している。監査AI観点では、TEEによる計算の完全性保証と、ブロックチェーン上への貢献記録は、AI推論ログの改ざん防止・監査証跡として応用可能な仕組みである。

## アイデア

- Proof-of-Intelligence（PoI）によるインセンティブ設計：マイナーとバリデーターが品質競争することでネットワーク全体の推論品質が自律的に向上するメカニズムは、中央管理なしのSLA維持手法として監査エージェントの分散デプロイに応用できる
- TEEによる分散環境でのデータ主権確保：サーバー所有者でさえ実行中データを覗けないハードウェア隔離は、監査AI（内部統制データ処理）を外部クラウドで安全稼働させるための重要なプリミティブになりえる
- 実需ベースの外部収益モデル：ネットワーク排出（インフレ補助金）ではなくAPI利用料収益でマイナーを動機づける設計は、DePINの持続可能性課題に対する一つの解答であり、エンタープライズ向け分散インフラ設計の参考になる

## 前提知識

- **Bittensor / TAO** (TODO: 読むべき)
- **DePIN** (TODO: 読むべき)
- **Trusted Execution Environment (TEE)** (TODO: 読むべき)
- **Proof-of-Stake** (TODO: 読むべき)
- **サーバーレス推論API** (TODO: 読むべき)

## 関連記事

- /deep_251 証明可能なプライバシーを保証するAI利用インサイト取得システム（Google Research）
- /deep_484 フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装
- /deep_1173 エッジにおける分散生成AI推論のためのトラスト対応ルーティング（G-TRAC）
- /deep_1120 Intel® Gaudi® 2 AIアクセラレータ上でのテキスト生成パイプライン
- /deep_408 Google Cloud の GPU 付き Cloud Run で Ollama + ローカル LLM を動かす

## 原文リンク

[分散AIプラットフォームChutesとBittensorで始めるDePIN推論基盤](https://zenn.dev/taumu/articles/6d84f856d818b8)
