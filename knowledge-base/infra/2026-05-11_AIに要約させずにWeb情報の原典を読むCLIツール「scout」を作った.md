---
title: "AIに要約させずにWeb情報の原典を読むCLIツール「scout」を作った"
url: "https://zenn.dev/thkt/articles/eae521ee3f4016"
date: 2026-05-11
tags: [Claude Code, WebFetch, CLI, Rust, Readability, Gemini Grounding, SSRF対策, GitHub API, headless Chrome, コンテキストエンジニアリング]
category: "infra"
related: [1788, 94, 5163, 4907, 1145]
memo: "[Zenn LLM] AI に要約させずに Web 情報の原典を読む CLI を作った"
processed_at: "2026-05-11T12:15:30.411178"
---

## 要約

Claude CodeのWebFetchツールは、内部でHaikuモデルが取得したページを要約してからメインモデルに渡す仕組みになっており、原文が18,000文字あってもメインモデルには数百文字の要約しか届かない。この情報の欠落がコード実装精度に直結するという問題を解決するため、RustとCLIとして「scout」が開発された。scoutは要約を一切介さず、WebページをMarkdownに変換してそのままコンテキストに取り込める。主なコマンドは6種類：`scout fetch`（URL→cleanMarkdown変換）、`scout search`（Gemini Groundingによるグラウンドされた回答＋ソースURLリスト）、`scout research`（検索→上位N件fetch→全文レポート化）、`scout repo-tree`（GitHubリポのファイル一覧）、`scout repo-read`（GitHubファイルの範囲指定読み込み）、`scout repo-overview`（README＋Issue/PR/Releases一覧）。fetchはMozilla Reader View由来のReadabilityアルゴリズムで本文のみを抽出し、ナビ・広告・フッターを除去。SPAは自動検出してheadless Chrome（CDP）にフォールバックする。日本語クエリ対応として、ASCII技術用語（ライブラリ名・バージョン番号等）を自動抽出して英語クエリと併合検索する機能も持つ。セキュリティ面ではSSRF対策として4層の防御（URLバリデーション・DNS事前チェック・リダイレクト毎再チェック・最終接続先IP確認）を実装。出力はMarkdownとJSON（`--json`フラグ）に対応し、JSON出力では`retryable`・`degraded`フラグも含まれるためCI/CD連携やスクリプト化に適する。インストールはHomebrew経由（`brew install thkt/tap/scout`）。監査エージェント開発への示唆として、LangGraphベースのReActエージェントが外部ドキュメントや仕様書を参照する際、WebFetch経由の要約ではなくscout経由の原典取得に切り替えることで、コンテキスト精度を大幅に向上できる可能性がある。

## アイデア

- Claude CodeのWebFetchがHaikuによる要約をメインモデルに渡す内部構造は非公開だが、これを実測・検証してツールで回避した点が実践的
- 日本語クエリからASCII技術用語のみを抽出して英語クエリと併合する手法は、翻訳APIを使わずに多言語検索精度を上げる軽量なアプローチ
- AIエージェント経由でプロンプトインジェクションによりfetch URLが差し替えられるSSRFリスクを想定し、ローカルCLIにもかかわらず4層防御を実装している点がセキュリティ意識として参考になる

## 前提知識

- **Claude Code WebFetch** (TODO: 読むべき)
- **Readability アルゴリズム** (TODO: 読むべき)
- **Gemini Grounding** (TODO: 読むべき)
- **SSRF** (TODO: 読むべき)
- **headless Chrome CDP** (TODO: 読むべき)

## 関連記事

- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_5163 「できません」と言ったClaude Codeが、ドキュメントを渡したら動いた ── Kaggle NB自動提出を例に
- /deep_4907 Claude CodeのWebFetchは実際にはHaikuによる要約を返している：内部構造の解析
- /deep_1145 Clade v1.3.0 — CLI版推奨＋マイルストーンワークフロー

## 原文リンク

[AIに要約させずにWeb情報の原典を読むCLIツール「scout」を作った](https://zenn.dev/thkt/articles/eae521ee3f4016)
