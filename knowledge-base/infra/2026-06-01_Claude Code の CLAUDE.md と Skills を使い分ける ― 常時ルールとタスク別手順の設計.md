---
title: "Claude Code の CLAUDE.md と Skills を使い分ける ― 常時ルールとタスク別手順の設計"
url: "https://zenn.dev/goki602/articles/2026-05-31-claude-code-claude-md-skills-guide"
date: 2026-06-01
tags: [Claude Code, CLAUDE.md, Skills, プロンプト設計, コンテキスト管理, LLM運用]
category: "infra"
related: [6416, 5498, 5029, 3506, 6915]
memo: "[Zenn LLM] Claude Code の CLAUDE.md と Skills を使い分ける ― 常時ルールとタスク別手順の設計"
processed_at: "2026-06-01T21:02:09.080810"
---

## 要約

Claude Code における設定の肥大化を防ぐため、CLAUDE.md と Skills（.claude/skills/ 配下の SKILL.md ファイル群）の役割を明確に分離する設計指針をまとめた記事。CLAUDE.md はセッション開始時に毎回自動で読み込まれる「常時適用の設計書」であり、ビルド・テストコマンド（npm run build、pytest -x 等）、コーディング規約、プロジェクト固有のアーキテクチャ概要を記載する場所として位置づけられる。サイズ上限の目安は 500 行で、これを超えるとコンテキスト消費が増加しモデルの注意が分散しやすくなる。初期ファイルは /init コマンドでコードベースを自動解析して生成できる。一方 Skills は、各 SKILL.md の YAML フロントマターに記述した description フィールドが合致したときのみ読み込まれる条件付き設定モジュールであり、コードレビュー・テスト・デプロイ等の特定タスクに特化した手順を格納する。description は 250 文字を超えると切り詰められるため、「何をするか」と「いつ使うべきか（トリガー条件）」を前半に凝縮する必要がある。v2.1.152 から disallowed-tools フィールドが追加され、スキル実行中に禁止するツール（Bash、WebFetch 等）をスキル単位で制御できるようになった。同バージョンから /reload-skills コマンドも利用可能となり、SKILL.md 編集後に再起動なしで変更を反映できる。配置場所は ~/.claude/skills/ がグローバル（全プロジェクト共通）、.claude/skills/ がリポジトリ固有（チーム向け）に使い分ける。使い分けの判断基準はシンプルで、全作業で必要なルールは CLAUDE.md、特定コマンドや場面でしか使わない手順は Skills に切り出す。CLAUDE.md が肥大化し始めたら「このルールは特定タスクにしか関係しないか？」を自問し、Yes なら Skills に移動するのが公式推奨の運用方法。監査エージェント開発への示唆としては、LangGraph や Pydantic を使ったエージェント開発においても同様のモジュール分離の思想が適用できる。頻繁に参照すべきグローバルな制約（監査ルール、出力フォーマット規約）は CLAUDE.md に、特定フェーズ（証跡収集、リスク評価、レポート生成）の手順は Skills に分離することで、コンテキスト効率を保ちながらエージェントの挙動を安定させる設計が可能になる。

## アイデア

- description フィールドが 250 文字で切り詰められるという制約が、スキルの自動発動精度を左右する設計上のボトルネックになっている点。トリガー条件を前半に凝縮するという対策は、プロンプトエンジニアリングの attention locality の問題と本質的に同じ
- disallowed-tools をスキル単位で制御できる仕組みは、エージェントの権限最小化原則（principle of least privilege）をツールレベルで実現するもので、監査エージェントのような高リスク操作を含むシステムの安全設計に直接応用できる
- CLAUDE.md（常時読み込み）と Skills（条件付き読み込み）の分離は、RAG における dense retrieval と sparse retrieval の役割分担に類似しており、LLMのコンテキストウィンドウを有限リソースとして最適配分するアーキテクチャパターンとして一般化できる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **YAML frontmatter** → /deep_3895 Claude Code Routineの設定をfrontmatterでConfig as Code管理する
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_6416 Claude Code / MCPで学んだ、AIが迷わない知識設計とツール設計
- /deep_5498 日本語版 humanizer スキル（humanizer-ja）の設計と実装
- /deep_5029 ハーネスエンジニアリング入門【概要 & 実践的TIPS】
- /deep_3506 なぜClaude Codeは「トークンを食いまくる」のか、そしてそれを止める6つの習慣
- /deep_6915 Claude Codeを使うなら知っておきたい「コンテキスト」の話

## 原文リンク

[Claude Code の CLAUDE.md と Skills を使い分ける ― 常時ルールとタスク別手順の設計](https://zenn.dev/goki602/articles/2026-05-31-claude-code-claude-md-skills-guide)
