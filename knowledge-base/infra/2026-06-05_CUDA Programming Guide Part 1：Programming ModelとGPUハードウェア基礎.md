---
title: "CUDA Programming Guide Part 1：Programming ModelとGPUハードウェア基礎"
url: "https://zenn.dev/kaz20/articles/1e622ef249d133"
date: 2026-06-05
tags: [CUDA, GPU Programming, Streaming Multiprocessor, Warp, SIMT, Thread Block, Shared Memory, FlashAttention, NVIDIA]
category: "infra"
related: [1536, 2815, 2820, 580, 2643]
memo: "[Zenn 機械学習] CUDA Programming Guide Part 1"
processed_at: "2026-06-05T09:23:21.511420"
---

## 要約

東京科学大学博士課程の著者によるCUDA C++シリーズ第1回。最終目標はFlashAttention 3の自作。本記事ではCUDA Programming Modelの概念的理解を中心に解説する。

【Heterogeneous Systems】CUDAはCPU（host）とGPU（device）が共存するHeterogeneous System上を前提とする。LLM学習環境では複数CPU・複数GPUが並列稼働する構成が標準的。

【GPU Hardware Model】GPUはStreaming Multiprocessors（SM）の集合体であり、H100やB200では数百基のSMを搭載。複数SMをまとめた単位がGPC（Graphics Processing Cluster）。各SMはLocal Register File・Unified Data Cache（L1 Cache／Shared Memory兼用の物理リソース）・数値タイプ別演算ユニットを持つ。FlashAttentionで頻出する「Shared Memory」はこのUnified Data Cacheを指す。

【Thread/Thread Block/Grid】GPUは数千〜数万スレッドの並列実行で高スループットを実現。スレッドをまとめた単位がThread Block、Thread Blockをまとめた単位がGrid。同一Thread Block内のスレッドは必ず同一SM上で実行され、Shared Memory経由の効率的なcommunication・synchronizationが可能。Grid内のThread Block間の実行順序は保証されない。

【Thread Block Cluster（Compute Capability 9.0以降）】複数Thread BlockをClusterとしてグループ化し、単一GPC内でスケジューリング。Cooperative Groupsを用いてCluster内の異なるThread Block間でもcommunicate・synchronizeが可能。Distributed Shared Memoryにアクセスできる。

【Warp・SIMT】32スレッドからなるグループをwarpと呼び、SIMT（Single-Instruction Multiple-Threads）パラダイムで実行。warp内全スレッドが同一命令を実行し、制御分岐（if分岐等）でwarp lane単位のmask off処理が発生（Warp Divergence）。Part 2で解説するGlobal Memory CoalescingやShared Memory Bank Access PatternはWarpの理解が前提。

【Tile Programming Model】SIMTとは別のプログラミングモデル。プログラマはThread BlockレベルでTile（多次元データ集合）への演算を記述し、BlockからThreadへのマッピングはコンパイラが担当。Warp Divergenceが発生しない一方、Block単位で単一の制御フローに従う制約がある。

【GPU Memory階層】FlashAttentionはGPU Memoryの階層性（DRAM/HBM vs Shared Memory）に着目してAttention計算を効率化した技術。メモリ帯域幅の理解はGPUカーネル最適化の核心であり、Part 2以降で詳述予定。

監査エージェント開発への直接的な示唆は薄いが、LLMの推論・ファインチューニングコストの定量的把握に必要な基礎知識であり、ローカルLLMインフラ（RTX 3090）活用時のパフォーマンスチューニングに直結する。

## アイデア

- Warp（32スレッド）という粒度がGlobal Memory CoalescingとShared Memory Bank Conflictの両方に直結しており、この数字を意識するだけでカーネルのメモリ効率が大きく変わる
- Tile Programming ModelはWarp Divergenceを排除しコンパイラにThread割り当てを委ねる設計で、SIMTモデルとの使い分けがFlashAttentionのような高性能カーネル実装の鍵になる
- Thread Block ClusterとDistributed Shared Memory（Compute Capability 9.0以降）はH100世代の新機能であり、GPC単位でのデータ共有が可能になることでFlashAttention 3の実装に直接関わる階層構造

## 前提知識

- **GPU並列計算の基礎** (TODO: 読むべき)
- **SIMD / SIMT** (TODO: 読むべき)
- **メモリ階層（Cache/DRAM）** (TODO: 読むべき)
- **C++** → /deep_5797 MCPサーバーをRustではなく400行の純粋なC++20で書いた理由 〜巨大コード解析における密結合美学〜
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_1536 最適化の記録: BLOOM推論サーバーの高速化
- /deep_2815 Ubuntu Server に Docker と GPU ドライバをインストールする
- /deep_2820 PodmanのコンテナLinuxでNVIDIA GPU(Geforce RTX)を使ったローカルLLM環境を構築してみた
- /deep_580 Hugging Face Kernel Hub：5分で始める最適化カーネルの活用
- /deep_2643 ムスタファ・スレイマン：AIの進化は壁に当たらない——その理由

## 原文リンク

[CUDA Programming Guide Part 1：Programming ModelとGPUハードウェア基礎](https://zenn.dev/kaz20/articles/1e622ef249d133)
