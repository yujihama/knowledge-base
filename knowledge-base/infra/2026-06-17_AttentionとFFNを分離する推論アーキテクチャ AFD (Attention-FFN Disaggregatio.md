---
title: "AttentionとFFNを分離する推論アーキテクチャ AFD (Attention-FFN Disaggregation)"
url: "https://zenn.dev/tosshi/articles/8480f5be05871e"
date: 2026-06-17
tags: [AFD, MoE, vLLM, 推論最適化, Disaggregation, KVキャッシュ, ping-pong pipeline, MegaScale-Infer, Step-3, xDeepServe]
category: "infra"
related: [8244, 152, 6360, 7625, 7421]
memo: "[Zenn LLM] Attention と FFN を分離 ── AFD (Attention-FFN Disaggregation)"
processed_at: "2026-06-17T09:02:41.873790"
---

## 要約

大規模MoE（Mixture of Experts）モデルのデコード推論では、AttentionとFFN/Expertが全く異なるボトルネック特性を持つ。Attentionは1トークン生成のたびにKVキャッシュ全体をHBMから読み出すためメモリ帯域ボトルネックとなり、バッチサイズを増やしても演算強度（FLOP/byte）は改善しない。一方FFNは重み行列をバッチ全体で共有できるためバッチを大きくすれば演算バウンドにできるが、MoEの疎活性化（top-k Expert選択）により各Expertに届くトークンが薄くなりGEMMが小さいまま演算器が遊ぶ問題がある。たとえばMixtral 8×22B（top-2）をバッチ156で実行しても各Expertへは平均39トークンしか届かない。AFD（Attention-FFN Disaggregation）はこの問題を解決するため、AttentionとFFN/Expertを物理的に別GPUプールに分離するアーキテクチャである。Attentionプールは高HBM帯域・大容量特化のGPU（例：H20）を、FFNプールは高TFLOPS特化のGPU（例：L40S）を充てることで異種GPU構成も可能になる。通信オーバーヘッドはping-pong pipeline parallelismで隠蔽する。バッチを複数マイクロバッチに分割し、マイクロバッチ#0がFFNプールで処理中にAttentionプールは#1を処理する形で両プールが常に稼働する。ByteDanceのMegaScale-Infer（arXiv:2504.02263）は317B Scaled-MoEでTensorRT-LLM比1.90倍・vLLM比7.11倍のper-GPUスループットを達成し、専用M2N通信ライブラリでNCCL比P99レイテンシ92.9%削減を報告。StepFunのStep-3（arXiv:2507.19427）はAFDという命名を与えた論文で、321B/活性38B MoE型VLMにてH800・FP8・4Kコンテキスト・50ms TPOT SLA・32GPU（2A2F）構成で4,039 tokens/s/GPUを達成し、同条件のDeepSeek-V3（2,324 tokens/s/GPU）比+74%を実現。HuaweiのxDeepServe（arXiv:2508.02520）はAscend 910 / CloudMatrix384（384 NPU）上でTransformerless設計を採用し独自XCCL通信ライブラリを実装。vLLMではPR #29772でAFD基本実装が進行中で、`vllm fserver`コマンドでFFNプロセスを別起動し、AFDConnectorで隠れ状態テンソルの送受信を抽象化する構成。現状はeager mode・TP=1・Attention台数がFFN台数の整数倍という制約があり、CUDA Graph対応・PD分離統合はロードマップ段階。監査エージェント開発への直接示唆は薄いが、大規模推論インフラのコスト効率化手法として、エージェントの推論コスト最適化を検討する際の参考になる。

## アイデア

- AttentionとFFNの計算特性（メモリバウンドvs演算バウンド）の違いを活用して異種GPU（高HBM帯域のH20 vs 高TFLOPSのL40S）を役割別に使い分けることで、コスト正規化スループットを最大化できる点
- ping-pong pipeline parallelismによりノード間テンソル転送の通信レイテンシを計算時間の裏に完全に隠蔽できるという発想は、PD分離（Prefill-Decode分離）とは独立した別軸の最適化であり両者を組み合わせ可能である点
- vLLMがAFDConnectorを抽象化レイヤーとして設計し、将来的にstepmeshなど高性能バックエンドへの差し替えをプラグイン方式で可能にしている拡張性設計

## 前提知識

- **MoE (Mixture of Experts)** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **Roofline Model** (TODO: 読むべき)
- **Tensor Parallelism** → /deep_589 GPU を無駄にしない: TRL における Co-located vLLM による効率化
- **Expert Parallelism** (TODO: 読むべき)

## 関連記事

- /deep_8244 MiniPIC: 100行以下で実現する柔軟な位置非依存KVキャッシュ
- /deep_152 トークンを流し続けろ：16のオープンソースRLライブラリから学ぶ非同期学習アーキテクチャ
- /deep_6360 【2026年最新】Qwen 3.6/3.7 ローカル運用完全ガイド ― 27B/35B-A3B 選定とMTP・TurboQuant攻略
- /deep_7625 Tangram: マルチターンLLM推論における非一様KVキャッシュの実用化
- /deep_7421 RTX 4080（16GB VRAM）でローカルLLM 12モデルを実測：「15GBの壁」とOllama vs vLLMの比較

## 原文リンク

[AttentionとFFNを分離する推論アーキテクチャ AFD (Attention-FFN Disaggregation)](https://zenn.dev/tosshi/articles/8480f5be05871e)
