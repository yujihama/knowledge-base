---
title: "Claude Code 基礎ガイド：AIの全体像からMCP活用まで"
url: "https://zenn.dev/gingakuwagata/books/claude-code-basics"
date: 2026-04-13
tags: [Claude Code, MCP, CLAUDE.md, ハーネスエンジニアリング, フック, スキル, パーミッションモデル, Anthropic]
category: "infra"
related: [1245, 430, 41, 94, 13]
memo: "[Zenn LLM] Claude Code 基礎ガイド：AIの全体像からMCP活用まで"
processed_at: "2026-04-13T12:52:39.537766"
---

## 要約

本書はiOS開発者であるぎんがくわがた氏が執筆した、Claude Codeの入門書（約43,246字、無料公開）。全10章構成で、AI全般の基礎知識からClaude Code固有の概念・運用ノウハウまでを体系的にカバーする。

第1〜2章ではAIの種類（生成AI・識別AI等）とAnthropicのClaudeの位置付けを整理。第3章ではClaude Codeのインターフェース種類（CLI、デスクトップアプリ、VS Code/JetBrains拡張、Web）の使い分けを解説する。第4章はセットアップと初期設定の手順。

第5章のパーミッションモデルでは、Claude Codeが実行するツール呼び出し（ファイル読み書き、Bashコマンド等）に対する承認フローと安全性設計を説明する。第6章はClaude Code固有の概念として、CLAUDE.md（プロジェクト・ユーザー単位の指示ファイル）、スキル（/コマンドで呼び出せる再利用可能プロンプト）、ルール（行動制約）、フック（ツール実行前後に発火するシェルコマンド）の4概念を解説する。

第7章のコンテキスト管理では、会話履歴の圧縮挙動や効果的なプロンプト設計を扱う。第8章「ハーネスエンジニアリング」はClaude Codeを自動化基盤として組み込む手法で、CLAUDE.md・スキル・フック・設定ファイルを組み合わせてAIの振る舞いを構造化設計する考え方を提示する。

第9〜10章はMCP（Model Context Protocol）の解説。MCPはAnthropicが策定したオープン規格で、LLMと外部ツール・データソース（GitHub、Linear、Gmail等）を標準化されたプロトコルで接続する仕組み。Claude.aiおよびClaude CodeへのMCPサーバー追加・設定方法を具体的に示す。

監査エージェント開発への示唆：ハーネスエンジニアリングの考え方（CLAUDE.md + フック + スキルの組み合わせ）は、LangGraphベースの監査エージェントにおけるプロンプト管理・ツール実行制御の設計パターンと直接対応する。MCPを用いた外部システム連携（Linear等のチケット管理、GmailなどのGRC関連コミュニケーション基盤）は、監査ワークフロー自動化の実装候補として検討価値が高い。

## アイデア

- ハーネスエンジニアリングという概念：CLAUDE.md・スキル・フック・設定ファイルを組み合わせてAIの振る舞いを構造化設計する手法は、AIをソフトウェアコンポーネントとして扱う新しいエンジニアリング規律を示唆する
- MCP（Model Context Protocol）によるツール接続の標準化：LLMと外部サービスの接続をオープン規格で統一することで、LSP（Language Server Protocol）がIDEとの接続を標準化したのと同様のエコシステム形成が起きている
- フック機構によるAI行動の観測・制御：ツール実行前後にシェルコマンドを発火させる仕組みは、AIエージェントの副作用を人間が監視・介入できる安全弁として機能し、エージェントの本番運用における信頼性設計の参考になる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **LLM** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **CLI** → /deep_4 DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する

## 関連記事

- /deep_1245 AIエンジニアリング進化の系譜 — 第4の波「Authority Engineering」とは何か
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装

## 原文リンク

[Claude Code 基礎ガイド：AIの全体像からMCP活用まで](https://zenn.dev/gingakuwagata/books/claude-code-basics)
