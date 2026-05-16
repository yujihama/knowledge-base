---
title: "AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話"
url: "https://zenn.dev/biscuit/articles/llm-wiki-claude-code-personal-knowledge-base"
date: 2026-04-24
tags: [LLM Wiki, Claude Code, Claude Code Skills, Claude Code Routines, Obsidian, knowledge-base, RAG, hooks, 自動化, Markdown]
category: "agent-arch"
related: [2404, 94, 682, 1962, 9]
memo: "[Zenn LLM] AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話"
processed_at: "2026-04-24T12:29:35.873369"
---

## 要約

Andrej KarpathyとShann HolmbergのOSS「llm-wikid」が提唱する「LLM Wiki」パターンを、Claude Codeで実装した事例紹介。LLM WikiはLLMを司書として機能させ、自分の知識をMarkdownデータベースとして構造化し続けるステートフルなシステムで、従来のRAG（クエリのたびにゼロから検索・合成）とは異なり、一度コンパイルして蓄積しクエリするたびに成長する。Graphify社の計測でRAWファイル直接検索比約71.5倍のトークン削減が報告されており、約100記事超でRAGよりコンパイル済みアプローチが優位になるとされる。

システムは2層構造で設計されている。Layer 1（KBL）はLLMが自動生成・保守する動的層で、概念ページ・エンティティページ・ソースサマリーを格納。Layer 2（Brand Foundation）は自分の声・トーン・禁止表現を定義する静的層で人間が管理する。ディレクトリ構成はraw/（生ソース）・wiki/（LLM生成・保守）・brand-foundation/（人間のみ編集）の3区分。

Claude Code実装の要点は、CLAUDE.mdへのスキーマ・規約の完全記述と、hooksによるraw/ディレクトリ保護。hookスクリプトでWrite操作をexit 2でブロックし、既存ファイルへのEdit（ingested: true書き込み）のみ許可する。スキルとして/wiki-ingest（rawをwikiに変換・7ステップ）・/wiki-query・/wiki-lint・/wiki-explore・/wiki-to-zennを実装。旧来の.claude/commands/ではなく、動的コンテキスト注入・サブエージェント・ツール制限が使えるSkillsとして構築した。

自動化にはClaude Code Routines（2026年4月研究プレビュー公開）を活用し、6時間ごとに未処理raw/ファイルを自動ingest→専用ブランチにcommit & push→PR作成→squash mergeのパイプラインを構築。スマホのObsidian Web ClipperでクリップしたソースがGitHub経由でRoutinesに処理され、翌朝wikiが更新される運用を実現した。ingested: false/trueフラグで二重処理を防止し、explored: false→trueで人間レビューを管理する品質ゲートも設けている。AIが80%の整理・コンパイル・クロスリファレンスを担い、人間が20%のキュレーション・検証・洞察を担う分担が実際に機能しているとの報告。監査エージェント開発観点では、LLM Wikiの「コンパイル済み知識ベース」アーキテクチャは監査ルール・規制・過去事例の構造的蓄積に直接転用でき、hooksによるアクセス制御パターンはエージェントの権限設計（書き込み可能領域の明示的制限）として参考になる。

## アイデア

- hooksのexit 2によるディレクトリ保護パターン：raw/への新規Write操作をブロックしつつEditのみ許可することで、LLMの誤書き込みを構造的に防ぐアクセス制御の実装例
- RAGとの設計思想の違い：クエリのたびにゼロから検索するRAGに対し、LLM Wikiは事前コンパイル・蓄積型で約100記事超からトークン効率が逆転するという定量的ターニングポイントの存在
- ingested: false/trueフラグによる二重処理防止と、explored: false/trueによる人間レビューゲートの組み合わせで、AI生成コンテンツの品質管理ワークフローを実現している点

## 前提知識

- **RAG（Retrieval-Augmented Generation）** (TODO: 読むべき)
- **Claude Code Skills/hooks** (TODO: 読むべき)
- **Obsidian Web Clipper** (TODO: 読むべき)
- **Claude Code Routines** (TODO: 読むべき)
- **フロントマター（YAML）** (TODO: 読むべき)

## 関連記事

- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_682 【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う
- /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装

## 原文リンク

[AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話](https://zenn.dev/biscuit/articles/llm-wiki-claude-code-personal-knowledge-base)
