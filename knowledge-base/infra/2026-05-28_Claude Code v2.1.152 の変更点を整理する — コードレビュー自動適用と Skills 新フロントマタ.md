---
title: "Claude Code v2.1.152 の変更点を整理する — コードレビュー自動適用と Skills 新フロントマター"
url: "https://zenn.dev/goki602/articles/2026-05-27-claude-code-v2-1-152-what-changed"
date: 2026-05-28
tags: [ClaudeCode, Skills, code-review, frontmatter, disallowed-tools, 自動修正, 開発ツール]
category: "infra"
related: [5794, 5498, 1642, 1247, 4470]
memo: "[Zenn LLM] Claude Code v2.1.152 の変更点を整理する — コードレビュー自動適用と Skills 新フロントマター"
processed_at: "2026-05-28T21:04:35.089432"
---

## 要約

2026年5月27日リリースの Claude Code v2.1.152 は、主に4点の変更を含む。①`/code-review --fix`：従来の`/code-review`は問題点の列挙に留まっていたが、`--fix`フラグを追加することでレビュー結果を working tree に直接書き込む自動修正が可能になった。正確性・再利用性・簡略化・効率改善の4軸でレビューを行い、effort レベル（デフォルト: medium、high も指定可）と組み合わせることができる。`--comment`（GitHub PRインラインコメント投稿）との併用も可能。②`/simplify`のエイリアス化：従来独立コマンドだった`/simplify`が`/code-review --fix`を呼び出すエイリアスに変更された。これにより`/simplify`実行時に提案表示ではなく自動修正が走るようになり、実行前に`git status`で作業ツリーを確認する習慣が重要になった。チームで使用している場合はこの挙動変更の共有が必要。③Skills frontmatter の`disallowed-tools`対応：`.claude/skills/`配下のマークダウンで定義するカスタムコマンド（Skills）のフロントマターに`disallowed-tools`フィールドが追加された。従来の`allowed-tools`（許可リスト）に対して`disallowed-tools`は拒否リストとして機能し、ほぼ全ツールを使わせつつ一部のみ禁止したい場合に適する。ただし両方が指定された場合は`allowed-tools`が優先され`disallowed-tools`は無視される。実運用での強制力についてはコミュニティの検証待ちの面もある。④`/reload-skills`コマンド追加：スキル編集後にセッション再起動が不要になり、`/reload-skills`でセッションを維持したまま`.claude/skills/`を再スキャンできる。監査エージェント開発への示唆としては、`disallowed-tools`を用いて Edit/Write/Bash を禁止した読み取り専用の監査スキルを定義することで、スキル実行時の意図しないファイル変更を防ぐ安全な設計パターンが実現可能になった点が挙げられる。

## アイデア

- disallowed-tools により「全ツール許可 + 一部禁止」という設計が可能になり、監査スキルのような読み取り専用エージェントを宣言的に定義できる
- /code-review --fix が effort レベルと組み合わせ可能な点は、CI/CD パイプラインでの自動品質改善ステップへの組み込みを示唆する
- /simplify のエイリアス化は「コマンドのセマンティクス変更」という破壊的変更であり、共有環境でのツール挙動管理の難しさを示す事例

## 前提知識

- **Claude Code Skills** → /deep_1473 Claude Code Skillsは作って終わりじゃない — 事後ログで改善サイクルを回す
- **allowed-tools / disallowed-tools** (TODO: 読むべき)
- **git working tree** (TODO: 読むべき)
- **/code-review** (TODO: 読むべき)
- **frontmatter** → /deep_3895 Claude Code Routineの設定をfrontmatterでConfig as Code管理する

## 関連記事

- /deep_5794 社内独自LLMでもClaude Codeみたいなエージェント開発をしたい — Continue + AGENTS.md という解
- /deep_5498 日本語版 humanizer スキル（humanizer-ja）の設計と実装
- /deep_1642 バイブコーディングで失敗しない — 5つの罠と実践フレームワーク
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_4470 SPReAD 研究計画調書作成を伴走支援する Skill を作ってみた

## 原文リンク

[Claude Code v2.1.152 の変更点を整理する — コードレビュー自動適用と Skills 新フロントマター](https://zenn.dev/goki602/articles/2026-05-27-claude-code-v2-1-152-what-changed)
