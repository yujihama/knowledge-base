---
title: "MCP（Model Context Protocol）実践入門──LLMを外部ツールとつなぐ標準規格を自分で実装する【2026】"
url: "https://zenn.dev/karaagedesu/articles/4eefd40f81817d"
date: 2026-05-09
tags: [MCP, Model Context Protocol, FastMCP, Claude Desktop, LLMツール統合, Python, GitHub Issues, ReAct]
category: "agent-arch"
related: [1915, 88, 1784, 1247, 3379]
memo: "[Zenn LLM] MCP（Model Context Protocol）実践入門──LLMを外部ツールとつなぐ標準規格を自分で実装する【2026】"
processed_at: "2026-05-09T12:47:19.196685"
---

## 要約

MCP（Model Context Protocol）はAnthropicが2024年11月に公開したオープンプロトコルで、LLMと外部ツール・データソースを接続する業界標準規格。2026年時点でOpenAI・Google・Microsoftも採用し、「AIのためのUSB-C」と称される。従来はClaude・ChatGPT・Cursorそれぞれに個別実装が必要だったが、MCPにより一度サーバーを作ればすべての対応クライアントから利用可能になる。MCPサーバーが提供できる機能は3種類：①Tools（LLMが能動的に呼び出す関数）、②Resources（ファイル・DB・APIレスポンスなどLLMが参照するデータ）、③Prompts（再利用可能なプロンプトテンプレート）。個人開発ではToolsのみで十分なケースが多い。実装にはFastMCPライブラリを推奨。`pip install mcp fastmcp`でセットアップし、`@mcp.tool()`デコレータを関数に付けるだけでToolが定義できる。記事ではローカルMarkdownノートの全文検索サーバーとGitHub Issues連携サーバーの2つの実装例を提示。Claude Desktopへの接続はconfig.jsonにcommandとargsを記述して再起動するだけ。つまずきポイントとして①仮想環境のフルパス指定、②docstringの充実（LLMはdocstringでツール選択を判断）、③try-exceptによるエラーハンドリング（例外が投げられるとLLM処理が停止）の3点を挙げる。監査エージェント開発への示唆として、社内システムや監査ツール（ERPのAPI、ワークフローシステム等）をMCPサーバーとして実装することで、LangGraphベースのReActエージェントから標準化されたインターフェースで呼び出せる構成が実現できる。ツールのdocstring品質がLLMのツール選択精度に直結するという知見は、監査エージェントのツール設計において重要な設計原則となる。

## アイデア

- ツールのdocstringがLLMのツール選択ロジックそのものとして機能する点──仕様書とランタイム動作が同一ソースに統合されており、LLM-as-judgeの観点から「説明可能なツール設計」の実践例として参照できる
- MCPのTools/Resources/Promptsの3層分離は責務の明確化であり、能動的処理（Tools）と受動的データ提供（Resources）を分けることでエージェントのアクション空間を構造化できる
- 一度作ったMCPサーバーがClaude Desktop・Cursor・Zedなど複数クライアントで再利用できる設計は、監査エージェントのツール資産を組織横断で共有するインフラとして活用できる可能性がある

## 前提知識

- **Function Calling** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編
- **ReAct Agent** (TODO: 読むべき)
- **FastMCP** → /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- **JSON-RPC** → /deep_1738 Claude Code の MCP サーバー活用術：外部ツール連携で開発効率を最大化する
- **LLMツール呼び出し** (TODO: 読むべき)

## 関連記事

- /deep_1915 MCP（Model Context Protocol）実践ガイド——PythonでAIエージェントにツールを接続する
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_3379 【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α

## 原文リンク

[MCP（Model Context Protocol）実践入門──LLMを外部ツールとつなぐ標準規格を自分で実装する【2026】](https://zenn.dev/karaagedesu/articles/4eefd40f81817d)
