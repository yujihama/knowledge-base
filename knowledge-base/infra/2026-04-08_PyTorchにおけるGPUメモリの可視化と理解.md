---
title: "PyTorchにおけるGPUメモリの可視化と理解"
url: "https://huggingface.co/blog/train_memory"
date: 2026-04-08
tags: [PyTorch, GPU, CUDA, メモリプロファイリング, gradient_checkpointing, 混合精度訓練, BF16, Qwen2.5, bitsandbytes, TRL]
category: "infra"
memo: "[HF Blog] Visualize and understand GPU memory in PyTorch"
processed_at: "2026-04-08T12:26:44.950468"
---

## 要約

本記事はHugging Faceブログに掲載されたPyTorchのGPUメモリ管理チュートリアルで、`torch.cuda.memory._record_memory_history()`と`_dump_snapshot()`を用いてGPUメモリ使用履歴をpklファイルに記録し、pytorch.org/memory_vizで可視化する手法を解説している。

単純な線形層（nn.Linear(10_000, 50_000)）の例では、モデル生成で2GB、入力テンソル(5,000×10,000 float32)で200MB、出力テンソル(5,000×50,000 float32)で1GBが消費されることを数値で示し、勾配計算のためにactivationが保持されるタイミングを図解する。

実際のLLM（Qwen/Qwen2.5-1.5B）を用いた訓練ループの可視化では、メモリの内訳を①モデルパラメータ（青）②アクティベーション（橙、forward passで蓄積しbackward passで解放）③勾配（黄）④オプティマイザ状態（緑・赤）に色分けして説明。3ステップのループで3つのメモリスパイクが生じ、ピークはforward pass時に発生する。

メモリ推定において重要な落とし穴として「予約メモリ（reserved memory）」の概念を指摘。PyTorchはCUDA mallocのオーバーヘッドを避けるためメモリをキャッシュするため、実際に割り当てられた(allocated)メモリより多くが予約済みとなる。この予約分を無視すると必要メモリを過小評価する。

メモリ最適化手法として以下を提示：①`torch.no_grad()`によるアクティベーション保存の抑制（推論時）②混合精度訓練（BF16/FP16でパラメータ・アクティベーションを半減）③gradient checkpointing（アクティベーションを再計算して保存量を削減、計算コストとのトレードオフ）④gradient accumulation（バッチを分割してアクティベーションのピークを下げる）⑤8-bit/4-bit量子化オプティマイザ（bitsandbytes等）によるオプティマイザ状態の削減。

また、TRLライブラリがこれらの最適化を実装済みであることを示し、実際の訓練スクリプト例も紹介している。

## アイデア

- torch.cuda.memory._record_memory_history()によるメモリ履歴の記録とpytorch.org/memory_vizでの可視化により、OOMエラーの原因をアクティベーション・勾配・オプティマイザ状態のどの成分か特定できる
- gradient checkpointingはアクティベーションをforward pass時に破棄し、backward pass時に再計算することでメモリをO(√n)に削減できるが、約33%の計算オーバーヘッドが発生するというトレードオフが定量的に示されている
- 予約メモリ（reserved）と割り当てメモリ（allocated）の差分を考慮しないとGPU要件を過小評価するという実践的な落とし穴は、モデルデプロイ計画時に見落としやすい重要な知見

## Yujiの取り組みへの示唆

LangGraphベースの監査エージェントシステムをローカルLLMインフラ（RTX 3090予定）で動かす際、LLMのfine-tuning（GRPO/RLAIF等）に直接役立つ。特にGPU 24GBのRTX 3090でQwen等のモデルを訓練する際、gradient checkpointingや混合精度訓練の適切な組み合わせを選択するための定量的な判断基準が得られる。メモリプロファイリングツールを用いてfine-tuning前にメモリ要件を見積もることで、OOMエラーを予防しつつ最大バッチサイズを決定できる。

## 原文リンク

[PyTorchにおけるGPUメモリの可視化と理解](https://huggingface.co/blog/train_memory)
