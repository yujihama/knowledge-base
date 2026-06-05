---
title: "【AIエージェント自作】tool_useを理解してツールを作る"
url: "https://zenn.dev/pekopugu/articles/agent01-a3-tool-use"
date: 2026-06-05
tags: [tool_use, LLMエージェント, Ollama, Claude API, ReAct, ディスパッチャ, OpenAI互換フォーマット, Python]
category: "agent-arch"
related: [7289, 7416, 4473, 5037, 2950]
memo: "[Zenn LLM] 【AIエージェント自作】tool_useを理解してツールを作る"
processed_at: "2026-06-05T09:15:11.567827"
---

## 要約

本記事はPythonでAIエージェントをスクラッチ実装するシリーズ（A3）の解説記事であり、LLMのtool_use機能の仕組みとその実装方法を具体的なコードで説明している。

tool_useとは、LLMが通常の回答生成ではなくツール呼び出しが必要と判断した際に`stop_reason="tool_use"`を返す仕組みである。エージェント側はこれを検知してツールを実行し、結果をmessagesに追加してLLMに再送する。LLMは最終的に`stop_reason="end_turn"`で回答を返す。このループ構造がエージェントの本質であり、LLMを複数回呼び出す`while True`ループで実装される。

ツール定義はOpenAI互換フォーマット（JSON Schema）で記述し、`name`と`description`の正確さがLLMのツール選択精度に直結する。実装されたツールは3本：(1)`read_file`―ファイル内容をUTF-8で読み込み、エラーを例外ではなく文字列で返すことでLLMが状況を自然言語で伝えられる設計、(2)`list_files`―ディレクトリ一覧取得、(3)`search_text`―正規表現検索でMAX_RESULTS=50件の上限制限を設けてコンテキストウィンドウ溢れを防止。

ディスパッチャ（`TOOL_REGISTRY`辞書＋`dispatch()`関数）により、新ツール追加時はレジストリへの1行追加のみで済む拡張設計を採用している。

躓きポイントとして、`qwen2.5-coder:7b`がtool_use非対応でJSONを平文返却する問題、`llama3.1:8b`でシステムプロンプトにカレントディレクトリを明示しないとパスをプレースホルダーで返す問題、Windows環境での日本語入力時のサロゲート文字化け（`sys.stdin.reconfigure(encoding="utf-8")`で解決）が報告されている。

監査エージェント開発への示唆として、tool_useのループ構造はLangGraphのノード遷移と概念的に対応しており、`TOOL_REGISTRY`のようなディスパッチャ設計はReActパターンのAction実行層として直接応用可能。エラーを文字列で返す設計はLLM-as-judgeパターンでエラー状況をLLMに伝える際にも有効な手法である。

## アイデア

- ツールのエラーを例外でなく文字列で返す設計により、LLMがエラー内容を自然言語で解釈・伝達できる——エラーハンドリングをLLMに委譲する発想の転換
- TOOL_REGISTRYによるディスパッチャ設計で、ツール追加コストをゼロに抑える拡張性——LangGraphのノード登録パターンと同型の設計思想
- MAX_RESULTS=50の上限制限でコンテキストウィンドウ溢れを能動的に防止する——ツール設計段階でLLMのトークン制約を意識した実装

## 前提知識

- **tool_use / function calling** (TODO: 読むべき)
- **OpenAI互換フォーマット** (TODO: 読むべき)
- **ReActパターン** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **LLMコンテキストウィンドウ** (TODO: 読むべき)

## 関連記事

- /deep_7289 【AIエージェント自作】AIエージェントとは何か・設計思想を整理する
- /deep_7416 【AIエージェント自作】ローカルLLM（Ollama）とClaude APIを切り替えるアーキテクチャ
- /deep_4473 WantedlyのPlaywright自動化で3回連続404——CDPセッション越しにフォームへ辿り着くまでの1時間
- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因

## 原文リンク

[【AIエージェント自作】tool_useを理解してツールを作る](https://zenn.dev/pekopugu/articles/agent01-a3-tool-use)
