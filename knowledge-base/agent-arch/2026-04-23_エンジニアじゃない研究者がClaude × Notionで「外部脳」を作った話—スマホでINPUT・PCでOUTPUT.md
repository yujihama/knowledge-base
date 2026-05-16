---
title: "エンジニアじゃない研究者がClaude × Notionで「外部脳」を作った話—スマホでINPUT・PCでOUTPUT"
url: "https://zenn.dev/kajungbang/articles/5c00f3bf7d7416"
date: 2026-04-23
tags: [Claude, Notion, MCP, 外部脳, ナレッジベース, CLAUDE.md, 非エンジニア, セッション管理]
category: "agent-arch"
related: [2102, 1422, 36, 2405, 436]
memo: "[Zenn LLM] エンジニアじゃない研究者がClaude × Notion で「外部脳」を作った話—スマホでINPUT・PCでOUTPUT"
processed_at: "2026-04-23T12:12:55.901612"
---

## 要約

社会科学系研究者（Marketing & Branding）が、Pythonもコードも書けない状態からClaude AppとNotion MCPを組み合わせて「AI外部脳」システムを構築した実践記録。出発点はClaude Codeのセッション忘却問題と、日々蓄積される論文・記事のキャッチアップ困難さ。Andrej KarpathyのCLLM Knowledge Bases投稿とhoeemの記事を参考に、ObsidianではなくNotionを選択（マルチデバイス対応・初心者向けという理由）。

システム構成は3層アーキテクチャ：Raw層（Notion Raw Sources DB＝原典保管、AIは書き換え禁止）・Wiki層（Notion Wiki DB＝AI生成サマリー・概念統合）・Schema層（SCHEMA.mdでAIの読み書きルール定義）。運用フローは「スマホのClaude Appから論文URLを投げる→Claude AppがNotion MCPで構造化保存（INGEST/COMPILE）→ローカルのPythonスクリプト`sync_notion_kb.py`でNotionから同期→Claude Codeがローカルのwikiフォルダを横断参照してクエリ応答（QUERY）」という分業体制。

設計上の重要な発見として、Claude CodeのNotion MCP連携にはOAuthトークンが約1時間で失効するバグ（GitHub issue #28256）があり、Claude Codeに全処理を担わせる当初設計が失敗。これを契機に「Claude App＝キュレーター（書く）」「Claude Code＝アナリスト（読む）」という役割分担が確立された。

~/.claude/CLAUDE.mdへの記載で、セッション起動時に`~/notion_kb/INDEX.md`の同期タイムスタンプを自動確認し、24時間以上古ければ同期スクリプトを自動実行する仕組みを実装。GitHubリポジトリ（Kajungbang/claude-notion-brain）でスクリプト・スキーマテンプレート・セットアップ手順を公開。非エンジニア向けにNotion DB作成（クリック操作）・JSON IDのコピペ・コマンド1つの3ステップに集約している。監査エージェント開発への示唆として、外部ナレッジベースとのセッション間連携設計（CLAUDE.mdへのルーチン注入・Raw/Wikiレイヤー分離・同期タイムスタンプ管理）は、LangGraphベースのエージェントに長期記憶を持たせる際のアーキテクチャパターンとして参考になる。

## アイデア

- Claude AppとClaude Codeの役割分担（書く vs 読む）によってMCP OAuth失効バグを設計上回避した逆転発想—制約が良いアーキテクチャを生む事例
- Raw/Wiki二層分離による原典保全とAI生成コンテンツの分離設計—AIが要約・解釈するのはWikiのみとすることでナレッジの信頼性を担保
- CLAUDE.mdへのルーチン注入（同期タイムスタンプ確認→条件付き自動同期）でAIがセッション開始時に自律的にコンテキストを取得しに行く設計

## 前提知識

- **Notion MCP** (TODO: 読むべき)
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **OAuth** (TODO: 読むべき)
- **外部脳アーキテクチャ** (TODO: 読むべき)

## 関連記事

- /deep_2102 Clade v1.14.5 ── Claude Code上のフレームワークを他の構成と正直に比べてみた
- /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- /deep_2405 Claudeトークン節約・完全保存版リファレンス2026｜9カテゴリ×全手法マップ
- /deep_436 Claudeと機械学習を頑張ることにした — Claude/Claude Codeをメンターとして活用する学習設計

## 原文リンク

[エンジニアじゃない研究者がClaude × Notionで「外部脳」を作った話—スマホでINPUT・PCでOUTPUT](https://zenn.dev/kajungbang/articles/5c00f3bf7d7416)
