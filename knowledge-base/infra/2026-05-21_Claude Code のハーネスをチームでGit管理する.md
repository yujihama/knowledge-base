---
title: "Claude Code のハーネスをチームでGit管理する"
url: "https://zenn.dev/forward/articles/be82a1bc3e2948"
date: 2026-05-21
tags: [Claude Code, ハーネスエンジニアリング, git管理, .gitignore, skills, agents, チーム開発, hooks]
category: "infra"
related: [5970, 94, 3377, 5498, 1788]
memo: "[Zenn LLM] Claude Code のハーネスをチームでGit管理する"
processed_at: "2026-05-21T09:06:25.470239"
---

## 要約

Claude Code で使うハーネス（agents・skills・hooks・commands など）をチームで共有・Git管理するための手法と、その実装リポジトリ「share-harness」の紹介記事。

【課題】Claude Code のプロジェクト横断設定は `~/.claude` ディレクトリに格納されるが、同ディレクトリには個人固有の agents や skills も混在する。チームで共有したいファイルだけをGit管理しようとすると、個人設定と衝突するという問題があった。

【解決策】`.gitignore` をホワイトリスト方式で活用することで衝突を回避した。具体的には、まず `*` ですべてのファイルを ignore し、その上で `-shared` というpostfixが付くファイル・ディレクトリのみを `!` で例外指定してGit追跡対象とする。例として `!agents/*-shared.md`、`!skills/*-shared/`、`!hooks/*-shared.py`、`!hooks/hooks-shared.json` などのパターンを `.gitignore` に記述する。

【運用方法】チームメンバーはリポジトリをクローンし、`.gitignore` だけを自分の `~/.claude` ディレクトリにコピーすれば、各自の個人設定を保持したまま `-shared` 命名のファイルだけをチームで共有・更新できる。個人ファイルはGitに追跡されないため、プッシュ時に誤って混入することもない。

【今後の展開】MCP・tools・context など、agents/skills 以外のハーネス構成要素についても別途共有の仕組みを検討中とのこと。

監査エージェント開発への示唆：コードレビューや設計レビュー用の skill/agent をチーム横断で統一管理する際に、この `.gitignore` ホワイトリスト方式は即座に応用できる。LangGraph ベースの監査エージェントのプロンプトテンプレートや ReAct ループ設定を `-shared` ファイルとして管理すれば、個人カスタマイズと組織標準の分離が実現できる。

## アイデア

- .gitignore をブラックリストではなくホワイトリストとして使い、命名規則（-shared postfix）と組み合わせることで、同一ディレクトリ内の個人ファイルとチーム共有ファイルを分離するアイデアは、他のツールの設定管理にも転用可能
- Claude Code のハーネス（agents/skills/hooks/commands）を「コード」と同等にバージョン管理することで、プロンプトエンジニアリングの成果物をチームの知識資産として蓄積できる
- MCP・tools・context など今後拡張予定の共有対象は、監査エージェントのコンテキスト設定やツール定義の標準化に直結するため、その仕組みの公開が待たれる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **~/.claude ディレクトリ構造** (TODO: 読むべき)
- **.gitignore ホワイトリスト** (TODO: 読むべき)
- **skills/agents/hooks** (TODO: 読むべき)
- **ハーネスエンジニアリング** → /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術

## 関連記事

- /deep_5970 ハーネスは書いて終わりじゃなかった ── 3か月運用して動的に壊れた5つの瞬間
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_3377 Claude Code 効き目順30 — ~/.claude/ で一番効く順に並べた実測レシピ集
- /deep_5498 日本語版 humanizer スキル（humanizer-ja）の設計と実装
- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素

## 原文リンク

[Claude Code のハーネスをチームでGit管理する](https://zenn.dev/forward/articles/be82a1bc3e2948)
