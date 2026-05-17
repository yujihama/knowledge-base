---
title: "ObsidianのメモがAIで自動的に記事になる──第二の脳の発信パイプラインを構築した話"
url: "https://zenn.dev/okikusan/articles/a35ead64446c05"
date: 2026-05-17
tags: [Claude Code, LLM Wiki, Obsidian, Karpathy, Cloudflare Pages, 自動デプロイ, MOC, CLAUDE.md, HTML生成, 多言語化]
category: "agent-arch"
related: [4336, 2954, 2250, 4186, 3239]
memo: "[Zenn LLM] Obsidian のメモが、勝手に記事になる ── 第二の脳の発信パイプラインを AI で作った話"
processed_at: "2026-05-17T21:01:42.354635"
---

## 要約

ObsidianのDailyノートに殴り書きするだけで、AIが自動的にwiki整理・HTML記事生成・多言語化・デプロイまでを行うパイプラインの構築事例。人間が関与するのは「①殴り書き」と「②最終的に読む」の2工程のみで、中間3工程（Wiki整理、HTML生成、デプロイ）はすべてAIが担う。

アーキテクチャはAndrej Karpathyが提唱するLLM Wiki方式をベースに3層構造を採用。Raw層（daily/*.md）は人間が書きAIは触らない、Wiki層（knowledge/*.md）はAIが育てるMOC（Map of Content）、Schema層（CLAUDE.md）はAIの行動規範を記述するルールブックとなっている。AIのコア操作は「Ingest（新ノードをMOCに追記）」「Query（INDEX→MOC→実体ノートで引用付き回答）」「Lint（矛盾・孤立・欠落リンク検出）」の3種で、CLAUDE.mdにこれを記述することでClaude Codeが常時参照しながらwikiを自律的に育てる。

知識の矛盾や変化は統合・削除せず「日付別ノードとして並列保持」する方針を採用しており、複利的な蓄積を最重要視している点が特徴的。

出力フォーマットにMarkdownではなくHTMLを選択した理由は、Anthropic社のThariq Shihipar氏が指摘した「AI出力が1000行超になるとMarkdownの長文壁が深刻化し、100行超はほぼ読まれない」という問題への対処。HTMLではSVG/アニメーション/インタラクティブ図・段階表示・グラフ構造可視化・AIプレイグラウンド埋め込みなど表現力をフル活用する。Zenn/Qiitaを入口、自前HTMLを本体とする二段構えを採用。

多言語化は副産物として実現。同一MarkdownソースからAIに「英語圏向けにen.htmlを書け」と指示すると、機械翻訳ではなく英語として自然な構成・例示・たとえ話に再構成される。インフラはCloudflare Pagesを使用し、JA/EN×3ページ、4種OG画像（1200×630 PNG）、sitemap.xml、JSON-LD構造化データ（BlogPosting/WebSite/BreadcrumbList）を含む。デプロイはwrangler pages deployコマンド一発で、AIにnpm run deployを実行させるだけで本番反映される。

監査エージェント開発への示唆：CLAUDE.mdをSchema層として活用しAIの行動規範・操作ルールを宣言的に記述する手法は、エージェントの振る舞いを制御するシステムプロンプト設計に応用可能。「矛盾を消さず並列保持」する知識管理方針は、監査証跡の時系列管理や監査意見の変遷記録にも適用できる考え方。

## アイデア

- CLAUDE.mdをAIエージェントの行動規範（Schema層）として機能させ、Ingest/Query/Lintの3操作を宣言的に記述することでClaude Codeが自律的にwikiを育てる設計パターン
- 矛盾する知識を統合・削除せず日付別ノードとして並列保持する「複利的蓄積」パラダイムにより、知識の変遷そのものを資産化する手法
- AI出力の大規模化（1000行超）に対応するためMarkdownではなくHTMLを出力フォーマットに採用し、インタラクティブ表現・多言語化・デプロイ自動化を一体化したパイプライン設計

## 前提知識

- **LLM Wiki（Karpathy）** (TODO: 読むべき)
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **MOC（Map of Content）** (TODO: 読むべき)
- **Cloudflare Pages / wrangler** (TODO: 読むべき)
- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説

## 関連記事

- /deep_4336 markdownとClaude Codeだけでアプリを作る：Spec-as-Appという新しいアーキテクチャ
- /deep_2954 ObsidianとClaude Codeで「育つ知識ベース」を作った話
- /deep_2250 Karpathyが指摘したLLMコーディングの失敗パターンと、コミュニティが作ったCLAUDE.mdの全貌
- /deep_4186 Context Rotを防ぐ知識ベース設計：LLM Wikiが体現するContext Engineering技法群
- /deep_3239 Claude Code で LLM Wiki を育てる——第二の脳の作り方

## 原文リンク

[ObsidianのメモがAIで自動的に記事になる──第二の脳の発信パイプラインを構築した話](https://zenn.dev/okikusan/articles/a35ead64446c05)
