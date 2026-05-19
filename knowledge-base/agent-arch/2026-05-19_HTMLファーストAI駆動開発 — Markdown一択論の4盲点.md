---
title: "HTMLファーストAI駆動開発 — Markdown一択論の4盲点"
url: "https://zenn.dev/miyan/articles/ai-driven-dev-html-first-pitfalls-2026"
date: 2026-05-19
tags: [RAG, HtmlRAG, Markdown, prompt-injection, Cloudflare, AI駆動開発, IPI, cloaking, tokenizer, Reader-LM]
category: "agent-arch"
related: [682, 3773, 2821, 1116, 5769]
memo: "[Zenn LLM] HTMLファーストAI駆動開発 — Markdown一択論の4盲点"
processed_at: "2026-05-19T09:03:13.829968"
---

## 要約

Cloudflareが2026年2月にリリースした「Markdown for Agents」を契機に、AI向けドキュメント配信は「Markdown一択」の空気が強まっている。本記事はその判断停止に対し、RAG層・Web配信層・セキュリティ層の3層に絞って4つの盲点を指摘する。

盲点①はHtmlRAG（arXiv 2411.02959, WWW 2025）の誤読。論文は「raw HTMLを渡せ」ではなく「block-tree pruningで圧縮したHTMLを渡す」ことを提案しており、HTML-Clean形式は元HTMLの5.93%まで圧縮しつつ、Llama-3.1-70BでASQA Hit@1=68.50と、Plain Text（59.75）やMarkdownを上回るretrieval精度を示した。rowspan/colspanを多用するテーブルをMarkdownに変換すると結合セルが分離し、RAGのembedding類似度が崩れる実害が報告されている。

盲点②はCloakingの工業化。CloudflareはAccept: text/markdownヘッダをoriginに転送する設計のため、origin側が人間とAIで別コンテンツを返すことが容易になり、David McSweeneyが「One Web原則の崩壊」と批判した（QueryBurst, 2026-02-13）。JSON-LD以外のmicrodata/RDFaは変換後に失われる点も重要。SEO重視のサイトでは同一性原則を担保できないなら有効化すべきでない。

盲点③はsilent failureとtokenizerずれ。Origin HTML 2MB超・Freeプラン・Acceptヘッダ未送信などの条件でMarkdown変換が無音でフォールバックしHTMLが返る。エージェント側でx-markdown-tokensヘッダとcontent-type: text/markdownの両方を確認しないと、HTMLタグごとembedされてトークン超過や類似度汚染が起きる。x-markdown-tokensはCloudflareの概算値であり、Claude/GPTの実トークンとずれるためCIのしきい値を過信してはならない。

盲点④はIndirect Prompt Injection（IPI）。「MarkdownはHTMLコメントが目立つから安全」という直感は崩れており、Google GTIG（2026-04-23）はMarkdownでもIPIが成立することを観測した。形式選択はIPI対策にならず、入力サニタイズとシステムプロンプトのハードニングが必要。監査AIのようにWebから文書を取得するシステムでは、コンテンツ取得時点でのIPI検出層を別途設計する必要がある。

## アイデア

- HtmlRAGのblock-tree pruningがHTML-CleanをMarkdownより小さく（5.93% vs 9.68%）かつ高精度に保てる点は、RAGパイプラインのフォーマット選択を「変換コスト vs 精度」のpareto問題として捉え直すフレームを与える
- Cloudflare Markdown for AgentsのAcceptヘッダ転送設計が意図せずcloaking工業化を招く構造は、インフラ層の設計決定がコンテンツ信頼モデルに波及する好例であり、監査エージェントがWebドキュメントを取得する際の二面性リスクとして直接参照できる
- IPIへの対策が「フォーマット選択」では解決できないという知見は、入力サニタイズをエージェントアーキテクチャのどのレイヤーに置くかの設計原則に影響し、LangGraphのノード境界でのサニタイズ実装指針として活用できる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Indirect Prompt Injection** (TODO: 読むべき)
- **HtmlRAG** (TODO: 読むべき)
- **Cloudflare Workers** → /deep_1785 CloudflareスタックだけでブラウザゲームのNaive RAGシステムを構築する
- **embedding類似度** (TODO: 読むべき)

## 関連記事

- /deep_682 【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う
- /deep_3773 Agentic AIはどう攻撃されるのか：EchoLeakをAAEF v0.2.0で解剖する
- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_5769 長期LLMペルソナ一貫性のための異種時系列メモリガバナンスフレームワーク（ARPM）

## 原文リンク

[HTMLファーストAI駆動開発 — Markdown一択論の4盲点](https://zenn.dev/miyan/articles/ai-driven-dev-html-first-pitfalls-2026)
