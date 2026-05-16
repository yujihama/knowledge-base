---
title: "Claude Code の MCP サーバー活用術：外部ツール連携で開発効率を最大化する"
url: "https://zenn.dev/yunisuta/articles/claude-code-mcp-server-tips-968850"
date: 2026-04-13
tags: [MCP, Claude Code, Model Context Protocol, Playwright, Supabase, GitHub, Notion, JSON-RPC, エージェント自律実行, 開発効率化]
category: "agent-arch"
related: [430, 88, 13, 51, 12]
memo: "[Zenn LLM] Claude Code の MCP サーバー活用術：外部ツール連携で開発効率を最大化する"
processed_at: "2026-04-13T12:24:46.189833"
---

## 要約

Claude Code は単なるコード補完ツールではなく、MCP（Model Context Protocol）サーバーと組み合わせることで「コードベースとサービスを横断して自律的に動くエージェント」として機能する。MCPはAnthropicが策定したオープンな通信プロトコルで、AIモデルが外部ツール・データソース・サービスをJSON-RPCで呼び出すための標準インターフェースを定義する。設定は~/.claude/settings.json（グローバル）または.claude/settings.json（プロジェクト単位）のmcpServersキーに数行追加するだけで完了し、Claude Code起動時に子プロセスとして各サーバーが立ち上がる。環境変数は${VAR_NAME}形式で参照可能。実践的なユースケースとして4つが紹介されている。①GitHub MCPによるコードレビュー：PR差分・関連Issue・ローカルファイルを一度のプロンプトで横断参照し、レビューコメントを自動生成。②Playwright MCPによるブラウザデバッグ：browser_navigate→browser_snapshot→browser_fill_form→browser_clickの一連の操作をAIが自律実行し、DOMスナップショットとコンソールログを取得して再現困難なバグを調査。③Supabase MCPによるDB連携コード生成：list_tablesとexecute_sqlでスキーマを自律取得し、実際の型定義に基づいたServer Actionを生成することでハルシネーションによる存在しないカラム参照を防止。④Notion MCPによる仕様駆動開発：最新仕様書からTypeScript型定義を自動生成し、ドキュメントとコードの乖離を解消。運用上のハマりどころとして、①Edge Functions等でapikey・x-client-infoなどのカスタムヘッダーがAccess-Control-Allow-Headersに含まれないと403エラーになるCORS設定問題、②MCPサーバーの起動失敗がサイレントに失敗するため--debugオプションで起動ログをgrepする必要性、③複数サーバーで同名ツールが衝突した際は後から登録したものが優先される優先順位問題、④大量データを返すAPI呼び出しがコンテキストウィンドウを消費するためフィルタ条件を明示する必要性（「全Issue取得」は不可、「直近30日・open状態のバグ報告のみ」のように絞る）が挙げられている。繰り返し参照するスキーマや設計ドキュメントはCLAUDE.mdに事前記載することでMCP呼び出し回数自体を削減できる。監査エージェント開発への示唆として、MCPプロトコルを活用すれば監査ログDBや内部統制ドキュメント管理システム（Notion等）とLangGraphエージェントを接続し、証跡取得・スキーマ検証・レポート生成を自律化できる可能性がある。

## アイデア

- MCPサーバーの起動失敗がサイレントに発生し、ツールなしで動き続ける設計はデバッグを困難にするが、--debugフラグとgrepを組み合わせた診断パターンが実用的
- 繰り返しアクセスするデータをCLAUDE.mdに事前記載することでMCP呼び出し回数を削減できる設計パターンは、トークン節約と応答速度改善の両方に効く
- Supabase MCPによる「スキーマを実際に取得してからコード生成」というアプローチは、ハルシネーションの根本原因（知識の不確かさ）をグラウンディングで解決する手法として汎用性が高い

## 前提知識

- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **JSON-RPC** (TODO: 読むべき)
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **エージェントツール呼び出し** (TODO: 読むべき)

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装
- /deep_51 SaaSを個人開発して運営しているが、本当に「SaaS is Dead」を感じ始めている
- /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える

## 原文リンク

[Claude Code の MCP サーバー活用術：外部ツール連携で開発効率を最大化する](https://zenn.dev/yunisuta/articles/claude-code-mcp-server-tips-968850)
