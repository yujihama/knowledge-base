---
title: "ObsidianとClaude Codeで「育つ知識ベース」を作った話"
url: "https://zenn.dev/sochi/articles/1e851637841acc"
date: 2026-04-25
tags: [Claude Code, Obsidian, LLM-wiki, CLAUDE.md, knowledge-base, Markdown, カスタムコマンド, クロスリファレンス]
category: "agent-arch"
related: [2821, 1962, 2547, 2250, 2405]
memo: "[Zenn LLM] ObsidianとClaude Codeで「育つ知識ベース」を作った話"
processed_at: "2026-04-25T12:48:53.981962"
---

## 要約

Andrej KarpathyのLLM知識ベースパターンに基づき、ObsidianとClaude Codeを組み合わせて自己成長型のWikiシステムを構築した事例。従来のRAGがファイルをベクトル化して検索するのに対し、このアプローチではClaude CodeがMarkdownファイルを直接編集・更新し続けることで知識を段階的に積み上げる。セッションをまたいで文脈が失われる問題（生成AIの根本的制約）を、LLMをWikiメンテナーとして位置づけることで解決する。

ディレクトリ構成はVaultルートにCLAUDE.mdを置き、raw/（人間が管理するソース置き場）とwiki/（Claude Codeが自動管理）に分割。wiki/以下はindex.md（全ページ索引）、log.md（操作ログ）、summaries/（記事まとめ）、concepts/（用語・概念）、entities/（固有名詞）、queries/（回答保存）の6種類のディレクトリで構成される。

運用は3つのカスタムコマンドで行う。/wiki-ingest（raw/のMarkdownを読み込み、summaries・concepts・entitiesページを自動生成・更新）、/wiki-query（index.mdを起点に関連ページを参照して引用付き回答を生成し、queries/に保存）、/wiki-lint（矛盾・孤立ページ・リンク切れを検出）。1つのソースが5〜10のwikiページに影響することもある。

CLAUDE.mdに自然言語でオペレーション手順を記述するだけでClaude Codeがメンテナーとして動作する。.claude/commands/ディレクトリにMarkdownを置くことでスラッシュコマンドとして呼び出せる。

実運用では10本程度の記事をWiki化した段階で、複数記事をまたいだクロスリファレンスによって「自分では繋げていなかった情報が繋がる」体験が得られたと報告されている。注意点として、/wiki-ingestは処理に5〜10分かかること、数百ファイル規模での動作は未検証であることが明記されている。GitHubにテンプレート（sochi512/llm-wiki-template）が公開されており、クローン後にclaude起動で即使用可能。

監査エージェント開発への示唆：CLAUDE.mdによるLLMへの役割委譲パターンは、監査手続きドキュメントのメンテナンスやエビデンス収集ログの自動索引化に応用できる。index.md起点の参照構造は、大量の監査調書をRAGなしで文脈横断検索する軽量アーキテクチャとして参考になる。

## アイデア

- RAGのようにベクトルDBを使わず、LLMがMarkdownを直接編集し続けるという「編集型知識ベース」アーキテクチャは、インフラ不要で軽量かつセッション横断の文脈保持を実現する点が設計として興味深い
- CLAUDE.mdに自然言語でオペレーション手順を記述することでLLMに役割を委譲するパターンは、監査エージェントのシステムプロンプト設計やツール定義の記述方針として直接応用できる
- index.md を唯一の入口として全知識グラフをナビゲートする設計は、エージェントがコンテキストウィンドウを節約しながら大規模ドキュメントを探索するための「エントリポイント駆動型RAG代替」として評価できる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Obsidian** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- **Markdown** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説

## 関連記事

- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- /deep_2547 【Claude Code】コマンドは3つだけ！ハーネスエンジニアリング実践編：log → distill → promote
- /deep_2250 Karpathyが指摘したLLMコーディングの失敗パターンと、コミュニティが作ったCLAUDE.mdの全貌
- /deep_2405 Claudeトークン節約・完全保存版リファレンス2026｜9カテゴリ×全手法マップ

## 原文リンク

[ObsidianとClaude Codeで「育つ知識ベース」を作った話](https://zenn.dev/sochi/articles/1e851637841acc)
