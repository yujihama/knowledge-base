---
title: "Claude Codeを使い倒すための設定術：CLAUDE.md・自動メモリ・コンテキスト管理の3本柱"
url: "https://zenn.dev/tamai_hideyuki/articles/claude-code-config-best-practices"
date: 2026-05-25
tags: [Claude Code, CLAUDE.md, 自動メモリ, コンテキスト管理, 開発環境設定, LLM活用]
category: "infra"
related: [5029, 3506, 2249, 2055, 6416]
memo: "[Zenn LLM] Claude Codeを使い倒すための設定術：CLAUDE.md・自動メモリ・コンテキスト管理の3本柱"
processed_at: "2026-05-25T09:09:01.639542"
---

## 要約

Claude Codeを効率的に使うための3つの仕組みを体系的に解説した実践ガイド。

**CLAUDE.md**はリポジトリルートに置くMarkdownファイルで、セッション開始時に毎回自動読み込みされる。「コードを読んでもわからないこと」、具体的には「なぜReduxではなくZustandを使っているか」「このAPIエンドポイントはパートナー契約で変更禁止」といった暗黙の文脈を記載する。コードパターン・関数名・頻繁に変わる情報（チケット番号・担当者名）は書くべきでない。チームでgitにcommitして共有できる点が最大のメリット。ルールが増えたら`.claude/rules/`サブディレクトリに`articles.md`・`api.md`・`testing.md`のように分割管理することでCLAUDE.md本体をコンパクトに保てる。

**自動メモリ**は`~/.claude/projects/<プロジェクトパス>/memory/`以下にMarkdown形式で保存される。user（ユーザープロファイル）・feedback（指摘・修正の蓄積）・project（進行中の作業・目標）・reference（LinearやGrafanaなど外部システムの場所）の4種類がある。CLAUDE.mdがチーム共通の「プロジェクトの常識」であるのに対し、自動メモリは特定ユーザーとの作業を通じて積み上がる個人的な文脈。feedbackメモリは古い「それは違う」が固定化されるリスクがあるため定期的な監査が必要。コードパターンや関数名（リファクタリングで場所が変わると誤情報になる）は保存しない原則を守る。

**コンテキスト管理**では、`/compact`（会話を要約圧縮して作業継続）と`/clear`（完全リセット）を使い分ける。`/compact`は実装が一段落したなどキリのいい場所で使うことで品質劣化を抑える。`@ファイル指定`で今のタスクに必要なファイルだけをClaudeに渡す習慣もトークン節約に有効。CLAUDE.mdが長大なほど毎セッションで無用なトークンを消費するため、簡潔さはコスト効率の問題でもある。

3本柱の役割分担：CLAUDE.md（チーム共有・永続的なプロジェクト常識）→自動メモリ（ユーザー固有・永続的な個人文脈）→コンテキスト管理（セッション内・一時的な品質維持）の3層で「毎回同じ説明をしなくて済む」状態を実現する。

## アイデア

- CLAUDE.mdの「書くべきでないこと」の原則（コードパターン・関数名・頻繁に変わる情報）がコンテキストコスト削減と直結しており、品質と効率の両面から同じ結論に至る点
- 自動メモリの4分類（user/feedback/project/reference）がClaude Codeのシステムプロンプト設計として公開されており、エージェント設計のメモリ分類パターンとして転用できる点
- `.claude/rules/`による関心分離（articles.md・api.md・testing.md）はRAGのチャンク戦略に類似しており、LLMへの情報提供を「必要な時だけ必要な粒度で」設計するアーキテクチャ原則として一般化できる点

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **Markdown** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- **LLMセッション管理** (TODO: 読むべき)

## 関連記事

- /deep_5029 ハーネスエンジニアリング入門【概要 & 実践的TIPS】
- /deep_3506 なぜClaude Codeは「トークンを食いまくる」のか、そしてそれを止める6つの習慣
- /deep_2249 Claude Codeの設定はどこに書くべきか ― プロンプト・RULES・スキル・エージェントの使い分け
- /deep_2055 Claude Codeのトークン消費を半分にする——800時間の運用データから見つけた実践テクニック
- /deep_6416 Claude Code / MCPで学んだ、AIが迷わない知識設計とツール設計

## 原文リンク

[Claude Codeを使い倒すための設定術：CLAUDE.md・自動メモリ・コンテキスト管理の3本柱](https://zenn.dev/tamai_hideyuki/articles/claude-code-config-best-practices)
