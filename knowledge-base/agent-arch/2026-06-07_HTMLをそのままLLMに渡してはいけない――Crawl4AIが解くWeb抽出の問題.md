---
title: "HTMLをそのままLLMに渡してはいけない――Crawl4AIが解くWeb抽出の問題"
url: "https://zenn.dev/aiwatch_jp/articles/crawl4ai-llm-ready-web-extraction"
date: 2026-06-07
tags: [Crawl4AI, RAG, Web抽出, Markdown変換, Playwright, LLMパイプライン, スクレイピング, self-host]
category: "agent-arch"
related: [856, 3372, 1116, 5769, 7177]
memo: "[Zenn LLM] HTMLをそのままLLMに渡してはいけない――Crawl4AIが解くWeb抽出の問題"
processed_at: "2026-06-07T09:02:53.111986"
---

## 要約

WebページをLLMやRAGパイプラインに活用する際、HTMLをそのまま渡すことは実用的でない。ネストしたタグ・広告・ナビゲーション・CSS・JavaScriptなどのノイズが多く、トークンを無駄消費し、本文抽出の精度も落ちる。Crawl4AIはこの「Web取得」と「LLM向け変換」という2つの問題を一体的に解くOSSである。

基本機能は、URLを渡すとPlaywright（Chromium）でヘッドレスブラウザ実行し、HTMLをMarkdownに変換して返すこと。`AsyncWebCrawler`を使った最小コードは10行程度で、`result.markdown`にMarkdown化されたコンテンツが格納される。JavaScriptで動的に読み込まれるコンテンツ（無限スクロール、SPA、クライアントサイドレンダリング）にも対応できる点が、単純なHTTPリクエストベースのスクレイパーとの差別化点である。

抽出戦略は3種類から選べる。①CSS Selectorによる固定構造サイト向け抽出（`CrawlerRunConfig(css_selector='.main-content')`）、②XPathによる抽出、③LLMベースの抽出（構造が可変なページ向け）。これらを組み合わせることで、固定サイトは軽量なCSS/XPath、複雑なページはMarkdown化後にLLM抽出という使い分けが可能。CLIも備えており、`crwl https://example.com`一行でMarkdown出力を確認できる。

競合ツールとの比較では、Firecrawl（API/SaaSとして手軽、商用サポートあり）やJina Reader（URLプレフィックスを変えるだけで使える）と異なり、Crawl4AIはOSSでself-hostが可能。業務利用での外部サービスへのURL送信リスク回避、社内ネットワーク内ページの処理、コスト予測可能性などの面で優位性を持つ。

監査エージェント開発への示唆としては、RAG構築時の前処理パイプラインとしての活用が直接的に使える。規制文書・監査基準・ガイドラインなどの外部Webコンテンツを自動収集してベクトルDB化する際、HTML→Markdown変換の品質がRAG検索精度に直結する。また、競合・技術調査や差分検出（更新された監査基準の変更点抽出等）にも応用可能。ただし、Playwright系の運用コストとして並列数・タイムアウト・メモリ設計が必要な点、Markdown化しても情報品質は保証されない点（表崩れ・リンク欠落等）に注意が必要。

## アイデア

- 「Web取得」と「LLM向け変換」を分離して考えるフレームワーク設計思想——単なるスクレイパーではなく中間変換層として位置づけることで、抽出戦略（CSS/XPath/LLM）を差し替え可能なアーキテクチャを実現している
- RAGにおける入力データ品質の重要性——モデル性能と同等かそれ以上に「何を渡すか」が回答品質を決定するという観点から、前処理パイプラインをファーストクラスの設計対象として扱う発想
- self-hostの戦略的意義——外部SaaS（Firecrawl/Jina Reader）との比較でコスト・セキュリティ・制御性のトレードオフを明示しており、業務用途での内製パイプライン設計判断の参考になる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Playwright** → /deep_17 AI vs. アンチボット：LLMが書き換えるウェブスクレイピングの全ルール
- **CSS Selector** (TODO: 読むべき)
- **ヘッドレスブラウザ** (TODO: 読むべき)
- **チャンキング** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた

## 関連記事

- /deep_856 Onyx 徹底調査：OSS AI プラットフォームの機能・仕様・導入・運用・API まで
- /deep_3372 AIを「会話ツール」から「知識コンパイラ」に変える：ワークフロー型AIという次のパラダイム
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_5769 長期LLMペルソナ一貫性のための異種時系列メモリガバナンスフレームワーク（ARPM）
- /deep_7177 長時間動くAIを成功させるカギ ― 3つのエージェントの緊張感

## 原文リンク

[HTMLをそのままLLMに渡してはいけない――Crawl4AIが解くWeb抽出の問題](https://zenn.dev/aiwatch_jp/articles/crawl4ai-llm-ready-web-extraction)
