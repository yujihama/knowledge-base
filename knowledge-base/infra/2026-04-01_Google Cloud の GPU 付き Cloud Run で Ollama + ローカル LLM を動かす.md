---
title: "Google Cloud の GPU 付き Cloud Run で Ollama + ローカル LLM を動かす"
url: "https://zenn.dev/massu_devix/articles/3a40000e8f3162"
date: 2026-04-01
tags: [Ollama, Cloud Run, NVIDIA L4, GPU, Google Cloud, qwen3-coder, コンテナ, サーバーレス]
category: "infra"
memo: "[Zenn LLM] Google Cloud の GPU 付き Cloud Run で Ollama + Local LLM を動かしてみた"
related: [396, 1450, 1581, 484, 404]
processed_at: "2026-04-01T21:07:52.412865"
---

## 要約

本記事は、Google Cloud の Cloud Run（NVIDIA L4 GPU 付き）に Ollama をデプロイし、30B クラスの LLM をクラウド上で動作させる手順を解説する。ローカル PC の GPU 制約を回避し、クラウド経由で大規模モデルを利用できる環境を構築することが目的。

構成は Cloud Build（Dockerfile からイメージビルド）→ Artifact Registry（イメージ保管）→ Cloud Run + L4 GPU（Ollama 起動）→ ローカル PC（localhost:9090 プロキシ経由）という流れ。Dockerfile では OLLAMA_HOST を 0.0.0.0:8080 に設定（Cloud Run のデフォルトポートに合わせる）、OLLAMA_KEEP_ALIVE=-1 でモデルをメモリ常駐させてコールドスタートを防止、ビルド時に `ollama serve & sleep 5 && ollama pull` でモデル（qwen3-coder:30b、約18GB）をイメージに含める設計となっている。

Cloud Run のデプロイパラメータとして、--gpu=1 --gpu-type=nvidia-l4 で VRAM 24GB の L4 を1基アタッチ、--cpu=8 --memory=32Gi（GPU 付き Cloud Run の最低要件）、--max-instances=1 --concurrency=1 で同時リクエストを1に制限、--timeout=600 で LLM 推論のタイムアウトを 600 秒に延長、--no-allow-unauthenticated でセキュリティを確保している。

アクセス方法は `gcloud run services proxy` でローカルにプロキシを立て、localhost:9090 経由で curl から Ollama API を呼び出す。課金管理として、プロキシ停止後にリクエストがなくなればインスタンスは自動スケールダウンし、`--min-instances=0` 設定で課金停止が可能。L4 の VRAM 制約（24GB）により 70B 超のモデルは動作不可で、その場合は GCE の A100/H100 インスタンスが推奨される。全手順を自動化する deploy.sh スクリプト（build/deploy/start/stop サブコマンド）も提供されており、日常運用の効率化に対応している。

## アイデア

- モデルをビルド時に Docker イメージへ同梱することで、起動時のモデルダウンロード待ちをゼロにする設計（コールドスタート対策とイメージサイズのトレードオフ）
- OLLAMA_KEEP_ALIVE=-1 によるモデル常駐とスケールダウン課金停止の組み合わせにより、コスト効率とレイテンシを両立する運用パターン
- Cloud Run のサーバーレス GPU という選択肢が、専用 GPU サーバーを持たない個人・小規模チームに 30B クラス LLM のオンデマンド利用を現実的にする
## 関連記事

- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け
- /deep_1450 ムスタファ・スレイマン：AI開発は近いうちに壁に当たらない——その理由
- /deep_1581 ムスタファ・スレイマン：AIの発展は近いうちに壁に当たらない――その理由
- /deep_484 フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装
- /deep_404 Ulyssesシーケンス並列化：100万トークンコンテキストでのLLM学習

## 原文リンク

[Google Cloud の GPU 付き Cloud Run で Ollama + ローカル LLM を動かす](https://zenn.dev/massu_devix/articles/3a40000e8f3162)
