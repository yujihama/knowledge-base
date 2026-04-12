---
title: "PyTorch FSDPを使ったLlama 2 70Bのファインチューニング"
url: "https://huggingface.co/blog/ram-efficient-pytorch-fsdp"
date: 2026-04-10
tags: [FSDP, Llama2, 分散学習, FlashAttention, Accelerate, PyTorch, A100, SLURM, gradient-checkpointing, bf16]
category: "infra"
memo: "[HF Blog] Fine-tuning Llama 2 70B using PyTorch FSDP"
related: [1532, 1620, 947, 1536, 404]
processed_at: "2026-04-10T09:00:34.928362"
---

## 要約

本記事は、Hugging Face の Transformers・Accelerate・TRL を活用し、PyTorch FSDP（Fully Sharded Data Parallelism）で Llama 2 70B をファインチューニングする手法を解説している。

FSDPは、オプティマイザの状態・勾配・パラメータをデバイス間でシャーディングするパラダイムで、フォワードパスでは all-gather 操作で完全な重みを取得し、計算後に他デバイスのシャードを破棄する。バックワードパスでは同様に all-gather でローカル勾配を計算し、reduce-scatter でデバイス間で平均・シャーディングして各デバイスが担当シャードのパラメータを更新する。

使用ハードウェアは2ノード構成で、各ノードにA100 80GB × 8枚（NVLink接続）、CPU RAM 1TB、96コアを搭載。ノード間は Elastic Fabric Adapter で接続している。

主な技術的課題と解決策は以下の3点。

【課題1: CPU RAMの枯渇】全ランクが70Bモデルをロードすると 70×4×8 GB ≈ 2TB のRAMが必要になり、OOMが発生する。解決策として、全ランクをmetaデバイス上で重みなしで初期化し、rank 0のみが state dict をロードする方式を採用（transformers#25107・accelerate#1777 で実装）。rank 0のCPUピークメモリは32,744 MB、rank 1はわずか1,506 MB に抑制される。`sync_module_states=True` を設定することで、FSDPがトレーニング開始前に全ランクへブロードキャストする。

【課題2: チェックポイント保存の遅延とNCCLタイムアウト】`FULL_STATE_DICT` による中間チェックポイント保存はrank 0がCPU上にモデル全体を収集するため時間がかかり、NCCLタイムアウトを引き起こす。中間保存には `SHARDED_STATE_DICT`（GPU毎にシャードを個別保存）を使用し、最終チェックポイントのみ `FULL_STATE_DICT` に切り替えて保存する2段階方式で解決。

【課題3: 速度とVRAMの最適化】FlashAttention V2（IO-Aware Exact Attention）とgradient checkpointingを組み合わせて高速化とVRAM削減を実現。FlashAttentionはメモリ階層を活用し、従来のアテンション計算よりも高速かつメモリ効率的に正確なアテンションを計算する。

FSDPコンフィグでは、シャーディング戦略に `FULL_SHARD`、自動ラップポリシーに `TRANSFORMER_BASED_WRAP`（`_no_split_module` でTransformerブロック名を検出）、混合精度に `bf16` を使用。SLURMクラスタとの統合も解説されており、マルチノード分散学習の実践的なセットアップが提供されている。

## アイデア

- rank 0のみが重みをロードしてFSDPがブロードキャストする方式は、CPUメモリを1/N以下に抑える実践的なパターンで、大規模モデルのマルチGPU展開設計に直結する
- 中間チェックポイントにSHARDED_STATE_DICTを使い、最終保存時のみFULL_STATE_DICTに切り替える2段階戦略は、NCCLタイムアウト回避と標準形式保存の両立として汎用的に使える
- FlashAttention V2 + gradient checkpointing の組み合わせはVRAMと速度のトレードオフを改善する定番構成であり、計算コスト削減の定量的根拠として論文実装を参照できる
## 関連記事

- /deep_1532 PyTorch DDPからAccelerateとTrainerへ：分散学習を段階的にマスターする
- /deep_1620 BLOOMトレーニングを支えた技術：Megatron-DeepSpeedによる176Bパラメータモデルの学習基盤
- /deep_947 Accelerate 1.0.0 リリース：マルチGPU・大規模モデル訓練フレームワークのメジャーバージョン公開
- /deep_1536 最適化の記録: BLOOM推論サーバーの高速化
- /deep_404 Ulyssesシーケンス並列化：100万トークンコンテキストでのLLM学習

## 原文リンク

[PyTorch FSDPを使ったLlama 2 70Bのファインチューニング](https://huggingface.co/blog/ram-efficient-pytorch-fsdp)
