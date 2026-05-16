---
title: "「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド"
url: "https://zenn.dev/shintaroamaike/articles/c7e7e6b27509cc"
date: 2026-05-12
tags: [Claude Code, LM Studio, Qwen3-Coder, ローカルLLM, GGUF, Ollama, ANTHROPIC_BASE_URL, MoE, SWE-bench, VS Code拡張]
category: "infra"
related: [2862, 3088, 2950, 2404, 1423]
memo: "[Zenn LLM] 「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド"
processed_at: "2026-05-12T09:19:24.965958"
---

## 要約

Claude Codeはエージェント型コーディングツールとして高い完成度を持つが、ソースコードがAnthropicのサーバーに送信される構造上、業務利用では機密コードを扱えないという制約がある。本記事はその制約を回避するため、Claude CodeをローカルLLMで完結させるセットアップ手順を詳述している。

アーキテクチャの核心は「Claude CodeはAnthropic Messages APIを内部で叩く」という点にある。LM StudioのCLIツール（lms）がlocalhost:1234でMessages API互換エンドポイントを提供し、Claude Code側の環境変数ANTHROPIC_BASE_URLを差し替えることで、通信先をAnthropicではなくローカルサーバーに向ける構成になる。モデルはQwen3-Coder-30B-A3B-Instruct（MoEアーキテクチャ、活性化パラメータ3B）のGGUF量子化版（Q5_K_XL）を採用。SWE-bench Verifiedのスコアは約51.6%で、Claude Sonnet 4.6の79.6%、Claude Opus 4.6の80.8%と比べ約30ポイント差があるが、「コードを外部に出さない」制約下ではローカルモデルのトップ候補となる。

セットアップはlms daemon up → lms server start → GGUFダウンロード → lms importの順で進め、lms loadでコンテキスト長65536・GPU最大利用でモデルをロードする。Claude Code側は~/.bashrcにラッパー関数claude-localを定義し、ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN / ANTHROPIC_API_KEYを設定して--modelに識別子を渡すだけで切り替えが完結する。

VS Code拡張機能（anthropic.claude-code）経由で使う場合はOllamaが最短ルートで、settings.jsonのclaudeCode.environmentVariablesにBASE_URLとトークンを設定する。さらにANTHROPIC_DEFAULT_OPUS_MODEL / SONNET_MODEL / HAIKU_MODELをそれぞれ別のOllamaモデルにマッピングすることで、タスク重みに応じたモデル切り替えも可能。なおCVE-2026-7482（Ollamaの脆弱性）への対応が必須とされている点も言及されている。

実用評価として、単発の関数実装・テストコード生成・シェルスクリプト作成程度であれば実用範囲内とされる一方、長コンテキスト・複数ファイルにまたがるリファクタリングでは品質差が顕在化する。MoEアーキテクチャによりVRAM効率が高く、RTX 5090（32GB VRAM）環境ではQ5_K_XL量子化でエージェント的な往復に耐える速度感が得られるとのこと。監査エージェント開発の観点では、社外秘の監査ロジックや未公開のGRC関連コードをローカルで安全にエージェント支援できる構成として直接応用可能。

## アイデア

- ANTHROPIC_BASE_URLの差し替えだけでClaude CodeのAPIターゲットをローカルに切り替えられる設計は、Claude Code自体がAPI互換レイヤーを抽象化していることを示しており、同様の手法でLLMゲートウェイや社内プロキシにも転用できる
- MoEアーキテクチャ（30B総パラメータ・3B活性化）により、フルパラメータ30Bモデルより大幅に低いVRAM消費でコーディング性能を維持する設計思想は、ローカル推論の実用化において重要なトレードオフ点を示している
- VS Code拡張のANTHROPIC_DEFAULT_OPUS/SONNET/HAIKUモデルへの個別マッピング機能は、タスク複雑度に応じてモデルを動的に切り替えるマルチモデルルーティングをUIレベルで実現しており、エージェントシステムのコスト最適化と同様の発想を個人開発環境に持ち込んでいる

## 前提知識

- **GGUF量子化** (TODO: 読むべき)
- **MoEアーキテクチャ** → /deep_196 MoEアーキテクチャ最適化のための包括的スケーリング則
- **Anthropic Messages API** (TODO: 読むべき)
- **SWE-bench** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **LM Studio / Ollama** (TODO: 読むべき)

## 関連記事

- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録
- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_1423 Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）

## 原文リンク

[「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド](https://zenn.dev/shintaroamaike/articles/c7e7e6b27509cc)
