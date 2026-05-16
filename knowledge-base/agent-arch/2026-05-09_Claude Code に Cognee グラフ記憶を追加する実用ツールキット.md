---
title: "Claude Code に Cognee グラフ記憶を追加する実用ツールキット"
url: "https://zenn.dev/japannomu/articles/20260502_cognee-graph-memory-toolkit"
date: 2026-05-09
tags: [Claude Code, Cognee, MCP, KuzuDB, LanceDB, グラフ記憶, Ollama, qwen2.5, RAG, セッション永続化]
category: "agent-arch"
related: [2404, 4520, 9, 2405, 4177]
memo: "[Zenn LLM] Claude Code に Cognee グラフ記憶を追加する実用ツールキットを公開しました"
processed_at: "2026-05-09T09:31:53.972118"
---

## 要約

Claude Code のセッション横断的な記憶保持を実現するため、Cognee（AI Memory Engine）と Claude Code を橋渡しする実用ツールキットを MIT ライセンスで公開した。Cognee はエンティティ抽出・グラフ構築（KuzuDB）・ベクトル化（LanceDB / FastEmbed）をハイブリッド検索で提供するOSSだが、Claude Code から直接利用するには①会話ログの自動投入機構の欠如、②MCP サーバー起動時の環境変数（LLM_API_KEY、SYSTEM_ROOT_DIRECTORY）継承失敗による LLMAPIKeyNotSetError (Status 422)、③大量ナレッジの初期投入時のリトライ管理欠如という3つのギャップがある。本ツールキットはこれらを以下のコンポーネントで解決する。(1) start_cognee_mcp.py：config/.env を os.environ に読み込んだ上で execv で cognee-mcp を起動し、子プロセスへの環境変数継承を保証。依存ライブラリは Python 標準ライブラリのみ。(2) import_to_graph.py：~/.claude/rules/ 等のディレクトリや Markdown ファイルを Cognee グラフに投入。Ollama 起動確認・LLM_MODEL 存在チェックを起動時に実施。(3) split_knowledge.py + import_knowledge.py：H2 見出し単位でファイルを分割してチャンク化し、最大3回リトライ付きで順次投入。--dry-run オプションによる事前確認も可能。(4) harness/ ディレクトリ：Claude Code のフック（PostToolUse 等）経由でユーザー発言と AI 応答をグラフに自動蓄積するオプション機能。推奨 LLM はクラウド API（Claude / OpenAI）で動作安定性ほぼ100%。ローカル LLM では qwen2.5:14b（num_ctx=8192）が唯一全機能（remember / search(CHUNKS) / search(GRAPH_COMPLETION) / recall）の動作を確認済み。llama3.1:8b・llama3.2:3b・gemma4:e4b は structured output で JSON Schema 違反が頻発し recall が失敗。セットアップは5ステップ（venv作成・.env編集・MCP登録・サンプル投入・本番投入）で再現可能なドキュメントを提供。監査エージェント開発への示唆として、本ツールキットのフック自動蓄積パターンは LangGraph ベースのエージェントにも応用可能で、エージェントの判断根拠・設計決定をグラフ形式で永続化することで説明可能性（Explainability）の確保に活用できる。

## アイデア

- execv による環境変数継承という低レベルなOS機構を使って、MCP サーバー起動時の環境変数問題を Python 標準ライブラリのみで解決している点—追加 pip install ゼロという設計制約が実装選択を規定している
- RAG（答えだけ）vs グラフ記憶（経緯ごと）という対比が明示されており、設計決定・障害記録・ルールのような「なぜ」を保持したい用途にはグラフ構造が本質的に適している
- split_knowledge.py が H2 見出し単位でチャンク化する設計は、ローカル LLM の structured output 不安定性に起因する cognify 失敗を予防的に回避するための工夫で、コンテキスト長制約とモデル品質の両方に対処している

## 前提知識

- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **Cognee** → /deep_3943 AIエージェントのメモリ管理完全ガイド 2026 — Mem0 vs Zep vs Letta vs Cognee
- **KuzuDB** (TODO: 読むべき)
- **Claude Code hooks** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境

## 関連記事

- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_2405 Claudeトークン節約・完全保存版リファレンス2026｜9カテゴリ×全手法マップ
- /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選

## 原文リンク

[Claude Code に Cognee グラフ記憶を追加する実用ツールキット](https://zenn.dev/japannomu/articles/20260502_cognee-graph-memory-toolkit)
