---
title: "DGX Spark + Docker + SGLang + Qwen3.6-35B-A3B-FP8 環境構築手順"
url: "https://zenn.dev/supertaro/articles/571b74acb26724"
date: 2026-05-30
tags: [SGLang, Qwen3, DGX Spark, Docker, FP8, MoE, OpenAI-compatible API, 長コンテキスト, ローカルLLM]
category: "infra"
related: [5969, 2590, 4331, 2862, 6668]
memo: "[Zenn LLM] DGX Spark + Docker + SGLang + Qwen3.6-35B-A3B-FP8 環境構築"
processed_at: "2026-05-30T21:02:22.059531"
---

## 要約

NVIDIA DGX Spark 上で Docker を用いて SGLang の OpenAI-compatible API サーバーを構築し、Qwen/Qwen3.6-35B-A3B-FP8 を AI エージェント用途（OpenCode 等）で利用可能にする手順書。

Qwen3.6-35B-A3B-FP8 は Alibaba/Qwen 系の MoE モデルで、総パラメータ数 35B のうち実際に活性化されるのは 3B パラメータのみ。agentic coding・reasoning・tool calling・長コンテキスト処理を意図して設計されており、DGX Spark の Tensor コアに最適化された公式 FP8 量子化 checkpoint を使用する。本手順の優先事項は速度よりも 256K context（262,144 tokens）の安定稼働であり、FP8 採用による VRAM 節約が前提となっている。

構成の核心は docker-compose.yml と .env ファイルによる宣言的管理。主要パラメータとして CONTEXT_LENGTH=262144、MEM_FRACTION_STATIC=0.85、CHUNKED_PREFILL_SIZE=8192、MAX_RUNNING_REQUESTS=1（長コンテキスト KV cache の大きさに対応するため初期値は 1）、MAX_QUEUED_REQUESTS=8 を設定する。KV_CACHE_DTYPE=auto により SGLang に dtype 選択を委ねる安全寄りの設定とし、OOM 時は CONTEXT_LENGTH を 131072（128K）に下げる対処を案内している。

Qwen3.6 の MoE 構造に対応した固有パラメータとして、--mamba-scheduler-strategy=no_buffer（メモリ抑制優先）と --mamba-ssm-dtype=bfloat16（float32 比でメモリ削減）を指定。ipc: host 設定で PyTorch のマルチプロセス共有メモリを確保し、hf-cache ディレクトリをホスト側に bind mount することでコンテナ再作成時のモデル再ダウンロードを回避する。

APIサーバー起動後は curl で /v1/chat/completions への POST リクエストにより動作確認し、OpenCode 等のクライアントからは served-model-name（qwen36-35b-a3b-fp8）と PORT（30000）を指定して接続する。監査エージェント開発への示唆としては、256K の長コンテキストウィンドウにより複数の監査ドキュメントや長い会話履歴を一括処理できる点、および MoE アーキテクチャによる推論コスト削減（35B パラメータのうち実稼働 3B）がローカル LLM 運用のコスト構造改善に直結する点が挙げられる。

## アイデア

- 35B 総パラメータ・実稼働 3B の MoE 構造により、フルパラメータモデルと比較して推論時の VRAM 消費を大幅に抑えつつ大規模モデルの品質を保てる点
- FP8 量子化 + MEM_FRACTION_STATIC=0.85 + max_running_requests=1 という組み合わせで、速度を犠牲にして 256K context の安定稼働を最優先するトレードオフ設計の明示
- .env による設定の外部化により、CONTEXT_LENGTH・MEM_FRACTION_STATIC 等のチューニングパラメータをコード変更なしに切り替え可能にした運用設計

## 前提知識

- **MoE (Mixture of Experts)** (TODO: 読むべき)
- **FP8量子化** → /deep_426 ZeroGPU Spacesを事前コンパイル（AoT）で高速化する方法
- **SGLang** → /deep_5406 Irminsul: エージェント型LLMサービングのためのMLA-ネイティブ位置非依存キャッシュ
- **KV cache** → /deep_6079 LLM / AIエージェント時代の安全設計：確率的推論と決定論的ガードレールの境界
- **Docker Compose** (TODO: 読むべき)

## 関連記事

- /deep_5969 初めて作るオレオレAIデータセンター③：DGX SparkとRTX PRO 6000 Blackwell MAX-Qを比較する
- /deep_2590 ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成
- /deep_4331 RTX 4060 8GB でどこまで動く？ Qwen3 サイズ別 VRAM 境界線を探る
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_6668 M5 Max のローカル LLM ベンチ — MoE は GPU 性能、Dense はメモリ帯域幅がボトルネック、発熱の影響も調査

## 原文リンク

[DGX Spark + Docker + SGLang + Qwen3.6-35B-A3B-FP8 環境構築手順](https://zenn.dev/supertaro/articles/571b74acb26724)
