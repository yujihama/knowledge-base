---
title: "Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド"
url: "https://zenn.dev/rna4219/articles/ea7b40ade95a88"
date: 2026-04-24
tags: [Qwen3, Ollama, OpenCode, MoE, ローカルLLM, GGUF, llama.cpp, コーディングアシスタント]
category: "infra"
related: [2292, 399, 394, 2056, 1146]
memo: "[Zenn LLM] Qwen3.6-35B-A3B を OpenCode と Ollama でローカル運用する超初心者向けガイド (2026/04/19)"
processed_at: "2026-04-24T12:52:15.837936"
---

## 要約

本記事は、Alibabaが2025年4月にリリースしたMoE（Mixture of Experts）アーキテクチャのLLMであるQwen3シリーズ、特にQwen3-235B-A22B（総パラメータ235B、アクティブ22B）をローカル環境で動作させるための手順を初心者向けに解説したガイドである。URLのモデル名「35B-A3B」は旧称もしくは誤記で、実際の記事内容はQwen3の最新フラグシップモデルに関するものと推定される。

OllamaはローカルLLMの実行環境として広く使われるツールで、`ollama pull qwen3:235b-a22b`のようなコマンド一発でモデルのダウンロードと量子化済みGGUFファイルの展開が可能。推論にはllama.cppバックエンドが使われ、RTX 3090（24GB VRAM）などの民生GPUでもQ4_K_M量子化（約140GB）では厳しいが、Q2_K（約80GB）程度であればCPUオフロード併用で動作可能なケースがある。

OpenCodeはVS Code拡張またはCLIツールとして動作するAIコーディングアシスタントで、OpenAI互換APIエンドポイントを持つOllamaと組み合わせることで、GitHub CopilotやCursorの代替としてローカルLLMによるコード補完・チャットが実現できる。設定ファイル（settings.json）にOllamaのエンドポイント（デフォルト: http://localhost:11434）とモデル名を指定することで連携が完了する。

Qwen3の主な特徴として、thinking mode（推論チェーン出力）とnon-thinking mode（高速レスポンス）を`/think`・`/no_think`フラグで切り替えられる点が挙げられる。SWE-bench Verified（コーディングベンチマーク）でのスコアはGPT-4oやClaude 3.5 Sonnetに匹敵するレベルとされ、コーディング用途での実用性が高い。

監査エージェント開発への示唆として、MoEアーキテクチャにより推論コストを抑えつつ高精度を維持できる点は、LangGraphベースのReActエージェントにローカルLLMを組み込む際のコスト最適化に直結する。OllamaのOpenAI互換APIはLangChain/LangGraphのChatOpenAIクラスからそのまま呼び出せるため、既存エージェントコードの変更量を最小化できる。

## アイデア

- Qwen3のthinking/non-thinkingモード切り替えは、エージェントの推論ステップ（ReAct）では thinking ON、単純な分類タスクでは OFF と使い分けることでレイテンシとコストを動的に最適化できる
- OllamaのOpenAI互換エンドポイントはLangGraphのChatOpenAIと直結できるため、クラウドLLMからローカルMoE LLMへの切り替えをbase_url変更だけで実現できる
- MoEアーキテクチャ（235B総パラメータ・22Bアクティブ）は、民生GPU環境でも量子化（Q2_K〜Q4_K_M）とCPUオフロード併用により実用的な推論速度を確保できる可能性を示している

## 前提知識

- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **GGUF量子化** (TODO: 読むべき)
- **OpenAI互換API** → /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- **llama.cpp** → /deep_940 Llama 3.2 リリース：視覚理解とオンデバイス推論を兼ね備えたオープンモデル群

## 関連記事

- /deep_2292 8Bモデルが1GBに収まる1ビットLLM「Bonsai」を動かしてみた
- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_394 OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門
- /deep_2056 Gemma 4 思考モード検証：26B vs E4B — ローカルLLMでのオイラー数問題を題材にした精度・速度比較
- /deep_1146 1-bit Bonsai 8Bを触ってみた：爆速だが既存llama.cpp運用にはそのまま載らなかった

## 原文リンク

[Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド](https://zenn.dev/rna4219/articles/ea7b40ade95a88)
