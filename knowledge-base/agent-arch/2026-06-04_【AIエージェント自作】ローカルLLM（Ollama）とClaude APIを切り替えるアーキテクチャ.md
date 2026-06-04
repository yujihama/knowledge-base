---
title: "【AIエージェント自作】ローカルLLM（Ollama）とClaude APIを切り替えるアーキテクチャ"
url: "https://zenn.dev/pekopugu/articles/agent01-a2-llm-client"
date: 2026-06-04
tags: [Ollama, Claude API, 抽象化レイヤー, OpenAI互換, REPL, ファクトリパターン, tool_use, qwen2.5-coder]
category: "agent-arch"
related: [7289, 2950, 6269, 5037, 4911]
memo: "[Zenn LLM] 【AIエージェント自作】ローカルLLM（Ollama）とClaude APIを切り替えるアーキテクチャ"
processed_at: "2026-06-04T09:19:39.837776"
---

## 要約

本記事はAIエージェント自作シリーズの第2回で、Phase A（土台）のStep 01〜03として、LLMクライアント抽象化レイヤー・システムプロンプト・ターミナルREPLループの3要素を実装する手順を解説している。

コアとなる設計は抽象基底クラス`LLMClientBase`（`src/llm/base.py`）で、`chat(messages, tools, system)`メソッドのみを持ち、戻り値を`{content, tool_calls, stop_reason}`の統一フォーマットに固定している。`stop_reason`は`end_turn`か`tool_use`の2値で、エージェントループ側がLLMの種類を意識せずに動作できる設計になっている。

Ollama接続（`OllamaClient`）はOpenAI互換エンドポイント`http://localhost:11434/v1`を利用し、`openai`ライブラリの`base_url`を書き換えるだけで実現。デフォルトモデルは`qwen2.5-coder:7b`。`api_key="ollama"`は認証不要なOllamaに対してopenaiライブラリが空文字を拒否する仕様を回避するための任意文字列。

Claude API接続（`ClaudeClient`）は`anthropic`ライブラリを使用し、デフォルトモデルは`claude-sonnet-4-20250514`、`max_tokens=4096`。`ANTHROPIC_API_KEY`は`.env`ファイルから読み込む。`tool_use`判定はレスポンスの`stop_reason`と`content`内ブロックの`type`で行い、`tool_use`ブロックのみを抽出して返す。

切り替えはファクトリ関数`create_client(llm, model)`に集約し、`--llm ollama`または`--llm claude`の起動引数で選択する。

REPLループ（`src/repl.py`）は`messages`リストに`{role, content}`を追記し続け、LLMに毎回全履歴を渡すことで文脈保持を実現する。

実装上の落とし穴として、Windows環境のcp932エンコーディング問題（`sys.stdout.reconfigure(encoding="utf-8")`で解決）とPowerShellのBOM付きパイプ問題が記録されている。

監査エージェント開発への示唆：この抽象化パターンはローカルLLM（コスト0・低レイテンシ）でロジック開発・デバッグを行い、本番評価時のみClaude API（高精度）に切り替えるという開発ワークフローに直結する。LangGraphベースのエージェントにも同様の抽象化レイヤーを挟むことで、モデル依存性を排除したテストが可能になる。

## アイデア

- OllamaのOpenAI互換エンドポイントを活用することで、`openai`ライブラリの`base_url`変更のみでローカルLLMとクラウドAPIを同一インターフェースで扱える点は、マルチプロバイダー対応エージェントの最小実装として参考になる
- `stop_reason`による分岐（`end_turn` vs `tool_use`）を抽象化レイヤー内で統一することで、エージェントループ側がAnthropicとOpenAIの異なるレスポンス構造を意識せずに済む設計は、LLM非依存なエージェントループ構築の基本パターンとなる
- ローカルLLMをデフォルトにして開発コスト0でイテレーションし、品質確認時のみAPIに切り替えるワークフローは、ファインチューニング・プロンプト評価を含むLLMシステム開発全般に応用できる

## 前提知識

- **抽象基底クラス（ABC）** (TODO: 読むべき)
- **OpenAI Chat Completions API** (TODO: 読むべき)
- **Anthropic Messages API** (TODO: 読むべき)
- **tool_use / function calling** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境

## 関連記事

- /deep_7289 【AIエージェント自作】AIエージェントとは何か・設計思想を整理する
- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_6269 開発しながらLoRAデータが自動で貯まる仕組み「M2LoRA」を作った
- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_4911 社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）

## 原文リンク

[【AIエージェント自作】ローカルLLM（Ollama）とClaude APIを切り替えるアーキテクチャ](https://zenn.dev/pekopugu/articles/agent01-a2-llm-client)
