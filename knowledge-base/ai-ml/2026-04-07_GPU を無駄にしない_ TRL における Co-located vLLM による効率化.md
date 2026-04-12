---
title: "GPU を無駄にしない: TRL における Co-located vLLM による効率化"
url: "https://huggingface.co/blog/vllm-colocate"
date: 2026-04-07
tags: [GRPO, vLLM, TRL, GPU最適化, 分散学習, Tensor Parallelism, SPMD, オンライン強化学習, H100]
category: "ai-ml"
memo: "[HF Blog] No GPU left behind: Unlocking Efficiency with Co-located vLLM in TRL"
processed_at: "2026-04-07T21:03:45.531441"
---

## 要約

TRL v0.18.0 以降で導入された「Co-located vLLM」は、GRPO などのオンライン強化学習において、推論（生成）と学習を同一 GPU 上で交互に実行する仕組みである。従来の「Server モード」では、vLLM を別プロセス・別 GPU 群で HTTP サーバとして起動し、学習スクリプトが REST API 経由でリクエストを送る構成だった。この場合、生成フェーズ中は学習用 GPU がアイドル状態になり、学習フェーズ中は vLLM 用 GPU がアイドル状態になるという「ピンポン問題」が発生し、GPU の実効利用率が大幅に低下していた。

Co-located モードでは、vLLM を `distributed_executor_backend="external_launcher"` オプションで同一 torch.distributed プロセスグループ内にインプロセス起動する。これにより、全 GPU が学習と推論を交互に担当し、HTTP 通信・別プロセス間通信のオーバーヘッドがゼロになる。Tensor Parallelism (TP) 対応として、`torch.distributed.new_subgroups_by_enumeration` で TP グループを動的に構築し、プロンプトの all_gather と出力の分配を PyTorch ネイティブ通信で処理する。torchrun との互換性も維持されており、マルチノード・マルチ GPU 構成への拡張が容易である。

ベンチマーク結果として、IBM Research のチームは 8×H100 環境での Llama-3.1-8B の GRPO 学習において、Server モード比でスループット（tokens/sec）が有意に向上することを確認している（具体的な数値は記事本文の図を参照）。また、専用推論 GPU を別途プロビジョニングする必要がなくなるため、クラウドコストの削減効果も大きい。実装は TRL の PR #3394 でマージ済みであり、`GRPOConfig` に `vllm_server_host` を指定せず `use_vllm=True` を設定するだけで Co-located モードが有効になる。SPMD（Single Program Multiple Data）実行モデルを採用しており、各 GPU が同期して自身の vLLM エンジンインスタンスを保持する設計のため、大規模分散学習でもスケールアウトが直線的に効く。

## アイデア

- 学習と推論を同一プロセスグループ内で交互実行する Co-location パターンは、GRPO に限らず PPO・REINFORCE など生成を伴うあらゆるオンライン RL に適用可能であり、今後の標準アーキテクチャになり得る
- external_launcher バックエンドによるインプロセス vLLM 起動は、HTTP サーバ管理の運用コストを完全に排除する設計思想であり、マイクロサービス分離 vs. モノリシック統合のトレードオフを GPU リソース効率の観点から再評価させる事例
- TP グループを torch.distributed のサブグループとして動的構築することで、既存の分散学習フレームワークのプロセスグループ管理と競合せずに推論エンジンを埋め込む手法は、他の推論ライブラリ（SGLang 等）への移植参考になる

## Yujiの取り組みへの示唆

Yuji が研究中の GRPO/RLAIF パイプラインにおいて、生成ボトルネックの解消は学習サイクルの高速化に直結する。RTX 3090 単体または少数 GPU 環境でも Co-located モードを使うことで、推論専用 GPU を別途確保せず GRPO 実験を回せるため、ローカル LLM インフラのコスト効率が改善する。また、監査エージェントの ReAct ループで自己評価（LLM-as-judge）を組み込む場合、生成と評価を同一 GPU で切り替える Co-location の設計思想がアーキテクチャ参考になる。TRL v0.18.0 以降で即座に利用可能な点も実用上の障壁が低い。

## 原文リンク

[GPU を無駄にしない: TRL における Co-located vLLM による効率化](https://huggingface.co/blog/vllm-colocate)
