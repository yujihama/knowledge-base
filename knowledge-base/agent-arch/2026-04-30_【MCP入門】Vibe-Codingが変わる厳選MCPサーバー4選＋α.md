---
title: "【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α"
url: "https://zenn.dev/pfj_cs/articles/c121cca7a3f1de"
date: 2026-04-30
tags: [MCP, Model Context Protocol, Vibe-Coding, Claude Code, Filesystem MCP, SQLite MCP, GitHub MCP, Fetch MCP, AIエージェント, npx]
category: "agent-arch"
related: [51, 2059, 1738, 1245, 430]
memo: "[Zenn LLM] 【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α"
processed_at: "2026-04-30T12:05:40.868125"
---

## 要約

MCP（Model Context Protocol）はAnthropicが2024年11月に公開したオープンプロトコルで、AIエージェントが外部ツール・データソースと標準インターフェースで接続できるようにする仕組み。2025年時点で公式リポジトリには200以上のMCPサーバーが登録されている。

Vibe-Codingとは、Andrej Karpathyが提唱した「AIに意図（Vibe）を伝えて実装を任せる」コーディングスタイル。MCP導入前は、DBスキーマ確認・APIレスポンス取得・ファイル一覧把握など、あらゆる情報をユーザーが手動でコピペしてAIに渡す必要があり、6ステップ程度の反復作業が発生していた。MCP導入後は「usersテーブルに認証ログ機能を追加して」の一言でAIが自律的にスキーマ確認・ファイル探索・コード生成・動作確認まで実行できる。

設定はClaude Codeの場合~/.claude.jsonにJSON数行を追記するだけ。npxで即起動できるサーバーが多く、Windows環境ではnpx.cmdを指定する点に注意が必要。

推奨4サーバーは以下の通り：
1. Filesystem MCP（@modelcontextprotocol/server-filesystem）：ローカルファイルの読み書き・検索を許可するパスを指定して起動。最も導入が簡単で効果を実感しやすい。
2. SQLite/PostgreSQL MCP（@modelcontextprotocol/server-sqlite）：--db-pathでSQLiteファイルを指定。AIがスキーマを直接参照してクエリ生成・API実装まで自律実行。
3. Fetch MCP（@modelcontextprotocol/server-fetch）：URLを渡すだけでAIが外部ドキュメントを取得。外部ライブラリの最新仕様参照やTypeScript型定義自動生成に有効。
4. GitHub MCP（@modelcontextprotocol/server-github）：GITHUB_PERSONAL_ACCESS_TOKENを環境変数に設定して起動。IssueからPR作成まで一気通貫で自動化可能。

番外編としてYouCam MCPサーバーも紹介。ヘアスタイル生成・メイク試着・肌分析・背景除去など26種類の画像・動画編集機能をHTTP型MCPで提供しており、~/.claude.jsonにurl・Authorizationヘッダーを設定するだけで利用できる。

監査エージェント開発への示唆：LangGraphベースのエージェントにMCPを組み合わせることで、監査ドキュメントのDB参照・外部規制文書の自動取得・GitHubでの監査ログ管理など、情報収集フェーズの自動化が実現できる。特にFetch MCPによる規制文書・基準書の動的参照は、監査基準の最新化を手動管理なしで行う仕組みとして応用価値が高い。

## アイデア

- MCPはAIの行動範囲を「渡された情報」から「自律的に調べられる情報」へ拡張する構造的な転換点であり、エージェントの自律度を設定ファイル数行で制御できる点が実用上の強み
- Filesystem・DB・Web・GitHubという4種のMCPを組み合わせると、コード生成→DB検証→ドキュメント参照→PR作成までのソフトウェア開発サイクル全体をAIが自律実行できるパイプラインになる
- YouCam MCPのようなドメイン特化型HTTP MCPの存在は、MCPが汎用開発ツールに留まらず業界固有のAIエージェント基盤として機能しうることを示しており、監査・法務・医療など規制業界への応用可能性を示唆する

## 前提知識

- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **AIエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **npx/Node.js** (TODO: 読むべき)
- **Vibe-Coding** → /deep_14 Vibe Coding XR：XR BlocksとGeminiによるAI+XRプロトタイピングの高速化
- **REST API** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア

## 関連記事

- /deep_51 SaaSを個人開発して運営しているが、本当に「SaaS is Dead」を感じ始めている
- /deep_2059 LLMを使って開発するなら、可観測性を最初から考えておくべきだった
- /deep_1738 Claude Code の MCP サーバー活用術：外部ツール連携で開発効率を最大化する
- /deep_1245 AIエンジニアリング進化の系譜 — 第4の波「Authority Engineering」とは何か
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話

## 原文リンク

[【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α](https://zenn.dev/pfj_cs/articles/c121cca7a3f1de)
