---
title: "OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門"
url: "https://zenn.dev/komlock_lab/articles/openclaw-local-llm"
date: 2026-03-29
tags: [Ollama, OpenClaw, Qwen3, ローカルLLM, ハイブリッドLLM, tool-calling, GGML]
category: "infra"
memo: "[Zenn LLM] OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門"
processed_at: "2026-03-29T22:06:25.600257"
---

## 要約

TypeScript製マルチチャネルAIアシスタントフレームワーク「OpenClaw」とGo製ローカルLLMランタイム「Ollama」を組み合わせ、MacBook 16GB環境で3コマンドによりローカルLLM環境を構築する手順を解説した記事。推奨モデルはQwen3:8B（4〜6GB、tool calling対応、日本語対応良好）。設定ファイル（openclaw.json）でローカル優先・クラウドフォールバックのハイブリッド構成が可能で、OpenAI/Anthropic APIへの自動切り替えを実現する。コンテキストウィンドウ・temperature・numCtx等のパラメータチューニングによりメモリと速度のトレードオフを制御できる。プライバシー保護・コストゼロ・低レイテンシ（100〜500ms）がローカル運用の主なメリット。

## 要点

- Ollama + OpenClawは3コマンドで構築可能。Qwen3:8BはTool Calling対応・日本語良好・16GB環境で快適動作
- openclaw.jsonのfallbacks設定でローカル優先→クラウドフォールバックのハイブリッド構成を宣言的に定義できる
- numCtxを8192に絞ることで16GB RAM環境での速度とメモリのバランスを最適化できる

## 監査エージェントへの示唆

監査エージェントで機密性の高い社内ドキュメントを処理する場合、ローカルLLMによりデータの外部送信を防ぎコンプライアンスリスクを回避できる。Qwen3:8BのネイティブTool Calling対応はReActベースの監査エージェント構築に直接活用可能。

## 原文リンク

[OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門](https://zenn.dev/komlock_lab/articles/openclaw-local-llm)
