---
title: "Claude Code の組込 WebFetch は生 Markdown を返さない — markitdown に乗り換えた話"
url: "https://zenn.dev/kanagen/articles/claude-code-webfetch-vs-mcp-server-fetch"
date: 2026-05-28
tags: [Claude Code, markitdown, MCP, WebFetch, mcp-server-fetch, uvx, SPA対応]
category: "infra"
related: [430, 2688, 4520, 6126, 1784]
memo: "[Zenn LLM] Claude Code の組込 WebFetch は生 Markdown を返さない。markitdown に乗り換えた話"
processed_at: "2026-05-28T21:00:53.549174"
---

## 要約

Claude Code に組み込まれた WebFetch ツールは、URL を取得する際に Claude Haiku が副次会話を起動して内容を解釈・要約する仕組みになっている。そのため、生の Markdown をそのまま取得したい用途には不向きであり、1回あたり約 $0.033 の追加トークンコストが発生する。代替手段として mcp-server-fetch と markitdown の2つが候補になる。mcp-server-fetch は httpx で HTTP 取得して Markdown に変換するだけで AI は介在せず、追加コストもゼロ。markitdown は Microsoft 製のオープンソースライブラリで、`markitdown <url>` コマンド一発で mcp-server-fetch と同等の生 Markdown を返す。さらに PDF・Word・Excel などのローカルファイル変換にも対応している点が差別化要因。mcp-server-fetch には初回タイムアウト問題が存在し、Claude Code 起動時に `uvx mcp-server-fetch` を実行すると lxml（5MB）を含む 45 パッケージのダウンロードが発生し、MCP 接続タイムアウトの 30 秒を超えてしまう。2回目以降は uvx のキャッシュが効いて即時起動するため、事前に手動実行するかDevContainerの postCreateCommand に追加することで回避できる。なお、mcp-server-fetch と markitdown はいずれも素の HTTP リクエストで動作するため、JavaScript でレンダリングする SPA には対応していない。Google の antigravity ドキュメントサイトで検証したところ HTTP 200 を返しても本文が空になることが確認されており、そのようなケースでは firecrawl scrape を使うのが現実的な回避策となる。著者の結論は、MCP はできる限り使わない方針と初回タイムアウト問題を理由に、現時点では markitdown がウェブページ取得のベスト選択肢というものだ。

## アイデア

- Claude Code の組込 WebFetch が Haiku を副次起動して要約する設計は、ユーザーの意図（生テキスト取得）と実装の乖離を生む典型例であり、ツール選定時に内部実装を確認することの重要性を示している
- uvx による初回パッケージダウンロードが MCP の 30 秒タイムアウトを超えるという問題は、MCP サーバーの起動コストが接続管理と相性が悪い構造的課題を示しており、DevContainer の postCreateCommand でキャッシュを事前に温める回避策が実用的
- markitdown は URL 取得だけでなく PDF・Word・Excel のローカルファイル変換にも対応しており、監査エージェントが様々なフォーマットの文書を統一的に Markdown 化して処理するパイプラインに組み込める汎用性がある

## 前提知識

- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **Claude Haiku** → /deep_5262 【Reincarnation Engineering】忘却のAI工学 ― Part1.実践編
- **uvx / uv** (TODO: 読むべき)
- **markitdown** → /deep_6552 mdx MaaSのAPIでLLM-jp-4を使う 第2回：文章の要約と情報の抽出
- **SPA / CSR** (TODO: 読むべき)

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ

## 原文リンク

[Claude Code の組込 WebFetch は生 Markdown を返さない — markitdown に乗り換えた話](https://zenn.dev/kanagen/articles/claude-code-webfetch-vs-mcp-server-fetch)
