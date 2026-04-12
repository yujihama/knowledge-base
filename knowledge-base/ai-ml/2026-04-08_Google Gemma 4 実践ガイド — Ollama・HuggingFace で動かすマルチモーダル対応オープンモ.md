---
title: "Google Gemma 4 実践ガイド — Ollama・HuggingFace で動かすマルチモーダル対応オープンモデル"
url: "https://zenn.dev/tkou15/articles/google-gemma-4"
date: 2026-04-08
tags: [Gemma4, Google, オープンウェイト, マルチモーダル, FunctionCalling, MoE, Ollama, HuggingFace, Apache2.0]
category: "ai-ml"
memo: "[Zenn LLM] Google Gemma 4 実践ガイド — Ollama・HuggingFace で動かすマルチモーダル対応オープンモデル"
processed_at: "2026-04-08T12:44:32.797992"
---

## 要約

2026年4月2日、GoogleはGemini 3の技術をベースとしたオープンウェイトモデル「Gemma 4」をリリースした。Apache 2.0ライセンスで公開されており、商用利用を含む制限がない。モデルは4サイズ展開：E2B（実効2.3B、128Kコンテキスト）、E4B（実効4.5B、128K）、26B MoE（アクティブ3.8B、256K）、31B Dense（256K）。全サイズにBase版とInstruction-tuned（IT）版がある。ベンチマーク性能はGemma 3 27Bから大幅改善され、26B MoEはAIME 2026で88.3%（Gemma 3は20.8%）、LiveCodeBenchで77.1%（同29.1%）を達成。31B DenseはArena AIリーダーボードでオープンモデル3位にランクイン。主要機能として、テキスト・画像・動画・音声（E2B/E4BはAudio対応）のマルチモーダル入力、ハイブリッドアテンション（ローカルスライディングウィンドウ＋グローバルフルアテンションの交互配置）、140言語以上での事前学習、`<think>`タグによるネイティブ推論モードを備える。ネイティブFunction Callingをサポートし、ツール定義をプロンプトに渡すとモデルがJSON形式でツール呼び出しを返す4ステップのエージェントループが構成できる。実行環境としてOllamaでは`ollama run gemma4`のワンコマンドで動作し、OpenAI互換APIサーバーとしても利用可能。HuggingFace Transformersではテキスト生成に`AutoModelForCausalLM`、マルチモーダル入力には`AutoModelForImageTextToText`と`AutoProcessor`を使用。VRAM要件はE4BでFP16約9GB・Q4量子化約4GB、26B MoEでQ4約16GB、31B DenseでQ4約20GB。旧カスタムGemmaライセンスからApache 2.0への移行により、QwenやMistralと同等の法的扱いとなり、プロダクション導入の障壁が低下した。

## アイデア

- 26B MoEモデルがアクティブパラメータ3.8Bのみで動作し、AIME 2026で88.3%を達成している点は、推論コストと性能のトレードオフ設計として注目に値する
- ネイティブFunction CallingをモデルレベルでサポートすることでLangChain等の外部フレームワークなしにエージェントループを構成できる設計が、デプロイ構成の単純化につながる
- Apache 2.0への移行はモデル配布・ファインチューニング・商用組み込みの法的ハードルを下げ、エンタープライズ向けローカルLLMの選択肢として実用性が増した

## Yujiの取り組みへの示唆

Gemma 4のネイティブFunction CallingはLangGraphのツールノード実装と直接対応しており、外部API呼び出しを含む監査エージェントのツールチェーン構築に活用できる。E4B（Q4量子化で約4GB VRAM）はRTX 3090（24GB）上でローカル実行可能であり、Yujiが構築中のローカルLLMインフラで監査ドメイン特化のファインチューニング基盤として適している。`<think>`タグによる推論モードはLLM-as-judgeのステップバイステップ評価プロセスにも応用できる。

## 原文リンク

[Google Gemma 4 実践ガイド — Ollama・HuggingFace で動かすマルチモーダル対応オープンモデル](https://zenn.dev/tkou15/articles/google-gemma-4)
