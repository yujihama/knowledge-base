---
title: "llm-wikiの発想を自分のObsidian vaultに持ち込んでみた"
url: "https://zenn.dev/sunyeul89/articles/bf48eb1a12ed81"
date: 2026-04-15
tags: [llm-wiki, Obsidian, 知識管理, AGENTS.md, ナレッジベース, ingest, Markdown]
category: "agent-arch"
related: [682, 8, 91]
memo: "[Zenn LLM] `llm-wiki` の発想を、自分の Obsidian vault に持ち込んでみた"
processed_at: "2026-04-15T12:40:17.358892"
---

## 要約

Andrej Karpathyが提唱したllm-wikiのパターンをObsidian vaultに適用した実践レポート。llm-wikiの核心は、LLMを「その場で質問に答えるチャットボット」から「wikiを継続的に保守する作業者」へと役割転換させる点にある。raw資料をそのまま都度LLMに渡す従来手法では回答は得られるが整理された知識は蓄積されない。llm-wikiはその間にwikiレイヤーを挟み、新しい資料投入のたびにsource noteを作成し、関連するtopic・entityページを更新させる。著者はこの構成をObsidian上でraw/・wiki/・system/の3層ディレクトリに翻訳した。raw/はsource of truthとして原本を保管し直接編集しない。wiki/はLLMが育てる知識レイヤーでsources・topics・entities・synthesesの4種類のページを持つ。system/はテンプレートや運用ルールを格納する。最も重要な要素としてAGENTS.mdを挙げており、ここにvault全体でLLMが取るべき振る舞い（raw編集禁止、質問時はwikiを先読み、構造変更の承認境界等）を定義することで、毎回プロンプトで細かく指示する手間を省き出力の再現性を高めた。運用フローはingest・query・lintの3フェーズに分離。ingestは新資料投入時にsource noteを作成して関連ページを更新、queryは毎回rawを読み直さずwikiを先に探索、lintは定期的にorphan pageやリンク不足・既存理解との矛盾を検出する。日々の入力は「次をingest: {url}」程度まで短縮可能。良かった点として、同じ資料を毎回ゼロから読ませる必要がなくなったこと、知識がMarkdownファイルとして手元に残りアプリ依存しないこと、整理の経緯が可視化されることを挙げる。課題はtaxonomyの粒度（何をtopicにして何をentityに切り出すか）の調整と、LLMが構造を広げすぎるリスクへの対処。長期的に同じ資料群を参照し再利用可能な知識ベースを育てたいユースケースに特に適している。監査エージェント開発への示唆として、AGENTS.mdによる役割固定とingest/query/lintの分離は、監査エージェントにおけるコンテキスト管理・ツール呼び出し戦略の設計パターンとして直接応用可能。

## アイデア

- LLMを「回答者」ではなく「wikiメンテナー」として役割固定することで、単発会話で消費される知識を再利用可能な構造化資産に変換できる
- AGENTS.mdに振る舞いルールを一元定義することで、毎回のプロンプトエンジニアリングコストを削減し、LLM出力の再現性を高める設計パターン
- ingest・query・lintの3フェーズ分離により、知識の投入・参照・品質維持をそれぞれ独立したオペレーションとして管理でき、エージェントの責務境界が明確になる

## 前提知識

- **llm-wiki** (TODO: 読むべき)
- **Obsidian vault** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **Markdown** → /deep_395 図形入りの PowerPoint を Markdown に変換する方法（GitHub Copilot + OpenXML SDK）

## 関連記事

- /deep_682 【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う
- /deep_8 LLMに「マジカルバナナ」式連想想起を実装したら会話が変わった
- /deep_91 Cortex Code CLI 実践カスタマイズガイド：Skills・SubAgents・Hooks・MCPによる拡張

## 原文リンク

[llm-wikiの発想を自分のObsidian vaultに持ち込んでみた](https://zenn.dev/sunyeul89/articles/bf48eb1a12ed81)
