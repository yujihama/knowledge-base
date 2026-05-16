---
title: "ZeROによるメモリ最適化：DeepSpeedとFairScaleで大規模モデルを効率的に学習する"
url: "https://huggingface.co/blog/zero-deepspeed-fairscale"
date: 2026-04-15
tags: [ZeRO, DeepSpeed, FairScale, sharded_ddp, GPU最適化, 分散学習, CPUオフロード, t5-large, t5-3b, HuggingFace Transformers]
category: "infra"
related: [429, 505, 589, 1620, 1762]
memo: "[HF Blog] Fit More and Train Faster With ZeRO via DeepSpeed and FairScale"
processed_at: "2026-04-15T12:24:33.958343"
---

## 要約

GPU メモリの増加速度が ML モデルの肥大化に追いつかない現状を解決するため、ZeRO（Zero Redundancy Optimizer）を実装した DeepSpeed と FairScale が Hugging Face Transformers v4.2.0 に統合された。ZeRO の核心は、従来の DDP（DistributedDataParallel）ではモデルウェイト・勾配・オプティマイザ状態の3つを全 GPU に複製していたのに対し、これらを GPU 間でシャーディング（分割保持）することでメモリ冗長性を排除する点にある。

マルチ GPU（2x 24GB Titan RTX）での t5-large の翻訳ファインチューニングベンチマークでは、ベースライン（DDP のみ、BS=16）と比較して以下の結果が得られた：FairScale の `--sharded_ddp` では BS=30 まで拡大し訓練時間を約 44% 短縮、DeepSpeed（CPU オフロードなし）では BS=40 で訓練時間を約 66% 短縮、DeepSpeed（CPU オフロードあり）では BS=50 まで拡大可能となった。FairScale は引数1つを追加するだけで導入できる手軽さが特徴で、DeepSpeed は設定ファイル（JSON）とランチャーの変更が必要だが、より高い最適化効果を発揮する。

シングル GPU（24GB RTX-3090）では、通常 BS=1 でも OOM となる t5-3b（約 3B パラメータ）を DeepSpeed の CPU オフロード機能により BS=20 で学習成功させることに成功した。CPU オフロードはオプティマイザ状態や勾配を CPU RAM に逃がすことで GPU メモリを節約する仕組みで、速度は低下するがモデル自体を GPU に載せることが可能になる。

ZeRO の最適化は3段階（Stage 1〜3）で構成され、Stage 1 はオプティマイザ状態のシャーディング、Stage 2 は勾配のシャーディング、Stage 3 はモデルパラメータ自体のシャーディングに対応する。これらを組み合わせることで、理論上は N GPU 使用時に N 倍のメモリ効率向上が見込める。

監査エージェント開発への示唆：ローカル GPU（RTX 3090 予定）で大規模モデルを扱う際、DeepSpeed の CPU オフロード機能は実用的な手段となる。シングル GPU 環境でも 3B 規模のモデルが動作することは、監査ドメイン特化ファインチューニングの選択肢を広げる。

## アイデア

- ZeROはモデルウェイト・勾配・オプティマイザ状態という3種類のメモリを段階的にシャーディングすることで、N GPU 使用時に理論上 N 倍のメモリ効率を実現する
- CPU オフロードにより GPU OOM を回避できるが、速度とのトレードオフがあり、シングル GPU でも 3B 規模モデルの学習が可能になるという実用上のブレークスルーを示している
- FairScale は引数1つ（`--sharded_ddp`）で導入でき、DeepSpeed より効果は小さいが導入障壁が低い──80:20 ルールに従って FairScale から試し、必要に応じて DeepSpeed に移行する戦略が合理的

## 前提知識

- **DDP（DistributedDataParallel）** (TODO: 読むべき)
- **混合精度学習（fp16）** (TODO: 読むべき)
- **オプティマイザ状態** (TODO: 読むべき)
- **勾配シャーディング** (TODO: 読むべき)
- **t5モデル** (TODO: 読むべき)

## 関連記事

- /deep_429 大規模AIシステムにおける戦略的レバーとしてのスループット最適化：データローダーとメモリプロファイリング革新からの証拠
- /deep_505 大規模AIシステムにおけるスループット最適化：データローダーとメモリプロファイリングの革新からの実証
- /deep_589 GPU を無駄にしない: TRL における Co-located vLLM による効率化
- /deep_1620 BLOOMトレーニングを支えた技術：Megatron-DeepSpeedによる176Bパラメータモデルの学習基盤
- /deep_1762 🤗 TransformersのWav2Vec2で大容量音声ファイルの自動音声認識を実現する方法

## 原文リンク

[ZeROによるメモリ最適化：DeepSpeedとFairScaleで大規模モデルを効率的に学習する](https://huggingface.co/blog/zero-deepspeed-fairscale)
