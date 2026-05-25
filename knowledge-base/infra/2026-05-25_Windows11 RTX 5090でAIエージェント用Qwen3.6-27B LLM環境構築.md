---
title: "Windows11 RTX 5090でAIエージェント用Qwen3.6-27B LLM環境構築"
url: "https://zenn.dev/supertaro/articles/14678514727616"
date: 2026-05-25
tags: [llama.cpp, Qwen3, GGUF, MTP, Docker, RTX5090, 量子化, KVキャッシュ, OpenAI互換API, speculative decoding]
category: "infra"
related: [6360, 4331, 5839, 3909, 409]
memo: "[Zenn LLM] Windows11 RTX 5090 で AI Agent 用 Qwen3.6-27B LLM 環境構築"
processed_at: "2026-05-25T09:02:02.779573"
---

## 要約

RTX 5090（GDDR 32GB）搭載のWindows 11環境において、Qwen3.6-27BモデルをAIエージェント（OpenCode等）向けに構築する手順を解説した記事。推論基盤にllama.cpp serverのCUDAビルドをDockerで動かし、unsloth/Qwen3.6-27B-MTP-GGUFのUD-Q4_K_XL量子化を使用する。コンテキスト長128K（CTX_SIZE=131072）を基本構成とし、Flash Attention（-fa on）・MTP（Multi-Token Prediction）speculative decoding（--spec-type draft-mtp / --spec-draft-n-max 2）・q8_0 KVキャッシュ量子化を組み合わせて速度とVRAM効率を両立させる。実装はWSL Ubuntu 24.04上で.envとdocker-compose.ymlの2ファイルのみで完結し、ghcr.io/ggml-org/llama.cpp:server-cudaイメージをそのまま使用できる。MTP使用時は-np > 1（PARALLEL=1固定）が必須制約であり、違反するとエラーになる。チューニング段階は4段階で設計されており、①安定確認（128K/q8_0 KV/MTP n=2）→②速度寄り（128K/q8_0 KV/MTP n=3）→③長文寄り（256K/q8_0 KV/MTP n=2）→④VRAM不足時（256K/q4_0 KV/MTP n=2）の順で調整する。RTX 3090での実測例として、MTP n=2で27 tok/sだった生成速度がn=3で50 tok/sに向上したという報告がある。RTX 5090では256Kコンテキストで65〜75 tok/sの報告もあるが個人検証値。既知の問題として、CUDA 13.2系でGGUF出力が文字化けする事例があり、CUDA 12.8への変更で解消したという報告がある。RTX 5090向けにllama.cppをソースビルドする場合はCUDA_DOCKER_ARCH=120またはCMAKE_CUDA_ARCHITECTURES=120が必要。OpenAI互換API（ポート8000）として提供されるため、既存のエージェントフレームワークからそのまま利用可能。監査エージェント開発においては、128K以上の長コンテキストが必要なマルチドキュメント分析やログ全文解析に本構成が直接適用できる。

## アイデア

- MTP（Multi-Token Prediction）speculative decodingにより、同一モデルのドラフトヘッドで先読みを行うことでRTX 3090でも27→50 tok/sの高速化が実現できる点は、ローカルLLM推論の実用性を大きく引き上げる
- q8_0 KVキャッシュ量子化により、128K〜256Kの長コンテキストでもVRAMを節約しながら品質を維持できる設計は、監査ログや長文ドキュメント処理に直接応用可能
- .envとdocker-compose.ymlだけで全パラメータ管理を完結させる構成は、本番環境の再現性確保やチューニング反復を容易にする実践的なインフラ設計パターン

## 前提知識

- **GGUF量子化** (TODO: 読むべき)
- **llama.cpp** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **speculative decoding** → /deep_6079 LLM / AIエージェント時代の安全設計：確率的推論と決定論的ガードレールの境界
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **Flash Attention** → /deep_831 BERTの後継モデル登場：ModernBERTの紹介

## 関連記事

- /deep_6360 【2026年最新】Qwen 3.6/3.7 ローカル運用完全ガイド ― 27B/35B-A3B 選定とMTP・TurboQuant攻略
- /deep_4331 RTX 4060 8GB でどこまで動く？ Qwen3 サイズ別 VRAM 境界線を探る
- /deep_5839 生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す
- /deep_3909 llama.cppの設定で8GBの性能が5倍変わる — 主要オプションの最適値を出した
- /deep_409 Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法

## 原文リンク

[Windows11 RTX 5090でAIエージェント用Qwen3.6-27B LLM環境構築](https://zenn.dev/supertaro/articles/14678514727616)
