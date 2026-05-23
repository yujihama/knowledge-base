---
title: "LLMの拡張標準「MCP (Model Context Protocol)」入門：Pythonでカスタムサーバーを構築する"
url: "https://zenn.dev/fsgesaiyo/articles/3581e5f4a92b6e"
date: 2026-05-23
tags: [MCP, Model Context Protocol, FastMCP, Claude Desktop, SQLite, Python, LLMツール連携]
category: "agent-arch"
related: [4742, 1915, 88, 1784, 3379]
memo: "[Zenn LLM] LLMの拡張標準「MCP (Model Context Protocol)」入門：Pythonでカスタムサーバーを構築する"
processed_at: "2026-05-23T09:05:56.532604"
---

## 要約

Model Context Protocol（MCP）は、LLMと外部データソースを標準化されたインターフェースで接続するためのオープン規格。従来はRAG構築や独自プラグイン開発が必要だったローカルDBや社内APIとの連携を、MCP経由で統一的に実現できる。

アーキテクチャはクライアント・サーバーモデルを採用。MCP Hostは Claude Desktop や対応IDEなどのLLM実行環境、MCP Serverはデータ・API へのアクセスを提供するPythonプロセス。サーバーが提供する機能は Resources（読み取り）、Tools（関数実行）、Prompts（テンプレート）の3種。本記事では実務頻度の高い Tools に焦点を当てる。

実装は公式Python SDK（pip install mcp）の FastMCP ラッパーを使用。FastAPI に類似したデコレータ記法で、@mcp.tool() を関数に付与するだけでツール登録が完了する。関数の docstring と型アノテーションが自動的にLLM側に公開され、LLMはそれを元に「いつ・どの引数で呼ぶか」を自律的に判断する。

実装例はSQLite（users.db）を対象としたDB検索ツール2本。get_user_by_id はID指定でユーザーをSELECT、search_users_by_department は部署名でフィルタリング。クエリ結果はJSON文字列でLLMに返される。サーバーは標準入出力（stdio）モードで起動（mcp.run()）。

Claude Desktop との接続は claude_desktop_config.json に mcpServers エントリを追加し、python コマンドと server.py の絶対パスを指定するだけ。再起動後、プロンプト入力欄のツールアイコンに「UserDB_Server」が表示されれば接続成功。「開発部のユーザー一覧を教えてください」と入力すると、Claudeが自動的に search_users_by_department(department="開発部") を呼び出し、日本語で回答を生成する。

監査エージェント開発への示唆：社内の監査ログDBや内部統制チェックリストをMCPサーバー経由で公開することで、Claude等のLLMが直接クエリを実行し、リスク分析や異常検知を自律的に行うエージェントを低コストで構築できる。JiraやGitHub APIとの連携例も言及されており、タスク管理・証跡収集を自動化するAI駆動監査ワークフローへの応用が現実的。

## アイデア

- FastMCPの@mcp.tool()デコレータがdocstringと型アノテーションを自動でLLMに公開する設計により、関数定義＝ツール仕様書になる点が開発体験として優れている
- stdioモードでサーバーを起動することで、ローカルプロセス間通信となりネットワーク露出なしにセキュアなデータ連携が実現できる点
- 社内DBや監査ログをMCPサーバー化することで、既存データ資産をエージェントから再利用可能にする『データアクセス層の標準化』としての活用可能性

## 前提知識

- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **LLM Tool Use** (TODO: 読むべき)
- **FastAPI デコレータ記法** (TODO: 読むべき)
- **SQLite** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **Claude Desktop** → /deep_4742 MCP（Model Context Protocol）実践入門──LLMを外部ツールとつなぐ標準規格を自分で実装する【2026】

## 関連記事

- /deep_4742 MCP（Model Context Protocol）実践入門──LLMを外部ツールとつなぐ標準規格を自分で実装する【2026】
- /deep_1915 MCP（Model Context Protocol）実践ガイド——PythonでAIエージェントにツールを接続する
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ
- /deep_3379 【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α

## 原文リンク

[LLMの拡張標準「MCP (Model Context Protocol)」入門：Pythonでカスタムサーバーを構築する](https://zenn.dev/fsgesaiyo/articles/3581e5f4a92b6e)
