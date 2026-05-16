---
title: "Claude Code Routineの設定をfrontmatterでConfig as Code管理する"
url: "https://zenn.dev/biscuit/articles/claude-routines-config-as-code"
date: 2026-05-06
tags: [Claude Code, Claude Code Routine, RemoteTrigger API, Config as Code, YAML frontmatter, cron, LLM automation]
category: "agent-arch"
related: [1429, 2953, 430, 2688, 1335]
memo: "[Zenn LLM] Claude Code Routineの設定をfrontmatterでConfig as Code管理する"
processed_at: "2026-05-06T12:19:13.227970"
---

## 要約

Claude Code Routineを複数運用する中で、プロンプト本文は`.claude/routines/*.md`としてGit管理できるが、`cron_expression`・`environment`・`model`・`repositories`・`mcp_connections`・`allow_unrestricted_branch_pushes`といった付帯設定はクラウド側内部状態にしか残らず、リポジトリを再クローンしたり数週間後に設定を確認したりする際にWeb UIをポチポチ確認する必要があるという問題を解決するパターンを紹介している。解決策はシンプルで、各Routineの`.md`ファイル冒頭にYAML frontmatterで設定を宣言するConfig as Code化である。設計の核心は、Claude Codeの`/schedule`コマンドが内部的にRemoteTrigger APIのラッパーになっており、`name`・`cron_expression`・`mcp_connections`・`allow_unrestricted_branch_pushes`・`enabled`はAPIのトップレベルbodyフィールドと完全に同名、`environment`/`model`/`repositories`は`job_config.ccr.*`配下のパスへのshort-hand表記として設計できる点にある。これにより、frontmatterは「ただのメモ」ではなく「APIへの入力宣言」として一貫した意味を持つ。`cron_expression`はUTC固定のため、JSTコメントを併記する運用を推奨している。また、Config as Codeの古典的課題であるdrift（宣言と実態の乖離）に対処するため、`last_synced_at`フィールドをISO 8601 UTC形式で記録し、「いつ実態を確認・反映したか」を可視化する。`/schedule`で設定変更した際は対応`.md`のfrontmatterと`last_synced_at`を必ず更新するルールを`.claude/rules/routines.md`に1行記載することで運用を担保する。`enabled: false`による一時停止状態の可視化、複数Routineを並べた際の実行時刻重複確認など、Git diffで設定変更を追跡できることのメリットも大きい。監査エージェント開発への示唆として、定期実行するLLMエージェントの設定をコードとして管理することで、「どのモデルバージョンが本番で動いているか」「どのRoutineが無制限branch push権限を持つか」といったガバナンス上重要な情報をGitで追跡可能になる点が有益である。

## アイデア

- /scheduleコマンドがRemoteTrigger APIのラッパーである事実を利用し、frontmatterフィールドをAPIフィールドと1対1対応させることで、ドキュメントと実装仕様を完全に一致させる設計パターン
- last_synced_atフィールドによるdrift可視化：完全自動同期なしでも「乖離の古さ」をISO 8601タイムスタンプで記録し、宣言と実態の乖離リスクを人間が判断できる最低限の情報を残す手法
- allow_unrestricted_branch_pushesをfrontmatterに明示することで、任意ブランチへのpush権限を持つRoutineをGit diffで追跡可能にするセキュリティガバナンスの実践

## 前提知識

- **Claude Code Routine** → /deep_3089 LLM WikiとClaude Code Routinesで「毎朝Slackに届く自分専用Digest」を作った
- **RemoteTrigger API** (TODO: 読むべき)
- **YAML frontmatter** (TODO: 読むべき)
- **cron式（UTC）** (TODO: 読むべき)
- **Config as Code** (TODO: 読むべき)

## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した

## 原文リンク

[Claude Code Routineの設定をfrontmatterでConfig as Code管理する](https://zenn.dev/biscuit/articles/claude-routines-config-as-code)
