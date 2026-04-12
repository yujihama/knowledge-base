---
title: "限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う"
url: "https://zenn.dev/4br4si0n/articles/506c761b35d9a6"
date: 2026-04-12
tags: [Codex, OpenRouter, マルチエージェント, モデル階層化, コスト最適化, gpt-oss-120b, サブエージェント]
category: "agent-arch"
memo: "[Zenn LLM] 限界社会人のための Codex 節約活用術"
processed_at: "2026-04-12T09:00:34.035038"
---

## 要約

ChatGPT Plus（$20/月）のCodexプロモーションが終了し、利用制限が従来比約5倍のペースで消費されるようになったことを背景に、コストを抑えながらCodexを使い続ける方法を解説した記事。著者はClaude CodeのProプラン（$17）では5時間のRate Limitが厳しく、Maxプラン（$100）は過剰というニーズから、ChatGPT Plusを選択していた。しかし2025年にOpenAIが公式にPlusプランのCodex利用を「1日の長時間セッションより週全体で多くの短いセッション」にシフトする旨を発表し、実質的な制限強化が行われた。

対策の中心は、Codex CLIにOpenRouterをモデルプロバイダとして接続する構成。OpenRouterはOpenAI互換APIで複数LLMを統一インターフェースで呼び出せるプロキシ兼ルーターで、条件を満たすユーザーには無料モデルを1,000リクエスト/日まで無償提供している。利用可能な無料モデルは `openai/gpt-oss-120b:free`、`Qwen3 Coder 480B A35B (free)`、`NVIDIA Nemotron 3 Super (free)`、`Google Gemma 4 31B (free)` など。

設定は `~/.codex/config.toml` に `[profiles.openrouter]` と `[model_providers.openrouter]` セクションを追加し、`base_url` に `https://openrouter.ai/api/v1`、`env_key` に `OPENROUTER_API_KEY` を指定するだけ。`codex --profile openrouter` で起動すれば無料モデルが使用される。

さらに高度な使い方として、メインエージェントは `gpt-5.4`（有料・高精度）、サブエージェントは `gpt-oss-120b:free`（無料・低精度）という役割分担を実現。`.codex/agents/reviewer.toml` のようなサブエージェント定義ファイルで `model_provider = "openrouter"` と `model = "openai/gpt-oss-120b:free"` を指定することで、コードレビューや調査・影響範囲の洗い出し等の補助タスクを無料モデルに委譲できる。Planning等のコアタスクのみ高性能モデルを使う棲み分けにより、サブスク枠の消費を大幅に抑制できる。監査エージェント開発への示唆としては、LangGraphのサブグラフやReActエージェントのツール呼び出しにも同様のモデル階層化（タスク重要度に応じたモデル選択）が適用でき、コスト最適化と精度のトレードオフ管理に活用できる。

## アイデア

- メイン/サブエージェント間でモデルを使い分けるアーキテクチャパターン：タスクの重要度・複雑度に応じてモデルを動的に選択することで、精度とコストのトレードオフを制御できる
- OpenRouterのフェイルオーバー機能：特定プロバイダ障害時に自動で代替モデルに切り替えられるため、エージェントシステムの可用性向上にも活用できる
- Codex CLIのconfig.tomlによるプロファイル切り替え機構：開発・本番・節約モード等、用途別プロファイルを切り替える運用パターンはLangGraphのグラフ構成管理にも参考になる

## 前提知識

- **Codex CLI** → [DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する](../agent-arch/2026-03-29_DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する.md)
- **OpenRouter API** (TODO: 読むべき)
- **LLMエージェント** → [Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践](../agent-arch/2026-03-29_Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践.md)
- **マルチエージェント構成** (TODO: 読むべき)
- **OpenAI互換API** → [OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）](../infra/2026-03-29_OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）.md)

## 関連記事

- [COBOLバッチプログラムをClaude Codeでモダナイズできるかの検証](../agent-arch/2026-04-10_COBOLバッチプログラムをClaude Codeでモダナイズできるかの検証.md)
- [AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築](../agent-arch/2026-03-29_AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築.md)
- [長期実行アプリケーション開発のためのハーネス設計](../agent-arch/2026-03-29_長期実行アプリケーション開発のためのハーネス設計.md)
- [部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読](../agent-arch/2026-03-30_部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読.md)
- [自律走行ポートフォリオ：機関投資家向け資産運用のエージェントアーキテクチャ](../agent-arch/2026-04-08_自律走行ポートフォリオ：機関投資家向け資産運用のエージェントアーキテクチャ.md)

## 原文リンク

[限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う](https://zenn.dev/4br4si0n/articles/506c761b35d9a6)
