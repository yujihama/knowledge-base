---
title: "Agentのおつかいの現在地：Agentic Commerceの3系統と決済レール争い"
url: "https://zenn.dev/moimoi/articles/agentic-commerce-current-state"
date: 2026-06-06
tags: [agentic-commerce, MCP, x402, HTTP402, ACP, USDC, M2M決済, LLMエージェント, 決済プロトコル, OpenAI, Stripe, Shopify]
category: "agent-arch"
related: [1475, 6885, 3000, 12, 5398]
memo: "[Zenn LLM] Agentのおつかいの現在地"
processed_at: "2026-06-06T09:04:38.434800"
---

## 要約

Agentic Commerce（エージェントによる自律購買）の現状を、決済インフラの視点から整理した記事。「おつかい」には予算上限・購買対象・決済手段の委任構造が伴い、その実現方式は現在3系統に分岐している。

①プロトコル系：正規APIをエージェントに使わせる方式。OpenAI×StripeのACP（ChatGPT Instant Checkout）、Google×ShopifyのUCP、Google主導でPayPal・Mastercardらが参加するAP2、Microsoft Copilot Checkoutなどが乱立。ACPはShopify加盟店がOpenAIに4%のチャネル手数料を払う構造で、カード手数料2.9%と合計すると約7%。Amazon紹介料（8〜15%）より低いが、関所を握った者が料率を後から変更できるリスクがある。さらに「何を選ばせるか」という選択順位自体が広告枠として機能しうる点も指摘（Amazonは2024年に広告収益約562億ドル）。

②力技系（UI自動化）：ブラウザを操作して人間用チェックアウト画面から購買するOSS「OpenClaw」等。店側の協力不要だがbot検知層（HUMAN Security/DataDome/Cloudflare等）との攻防が不可避。生のカード番号を単一エージェントに預ける構成は、決済業界が20年かけて排除してきたカード情報ベタ持ちを復活させるリスクがある。企業ユースではリスク審査を通過しにくい。

③M2M（機械間決済）：HTTP 402ステータスコードをpay-per-callに転用するx402プロトコルを活用。ツールが402を返す→エージェントが数セント支払う→ペイロード取得、という自律的な課金フロー。過去1年で約7,300万ドル／1.76億件の取引実績があり、そのうち98.6%がUSDC（Circle依存）。ERC-8004というオンチェーン評判によるエージェント信頼証明の仕組みも進行中。人間向けのretailが認証・関所で足踏みしている間、実際に金が動いているのはこのM2Mレーンのみ。

現状はAIショッピング採用率39%・AIトラフィック前年比805%増という需要がある一方、コンバージョン率はアフィリエイト比86%低い。2026〜27年が分岐点で、店の協力前提のプロトコル型が勝つか、computer-useの高度化によりプロトコル不要の力技型が主流になるかで、手数料構造が根本から変わる。日本では楽天がマーケットと決済レール両方を持つ希少プレイヤーだが、国際標準争いでは存在感が薄く、円建てステーブルコイン（JPYC）実証がM2M領域でポツポツ見られる程度。

## アイデア

- HTTP 402（Payment Required）という長年未使用だったステータスコードをエージェントのpay-per-call課金に転用するx402プロトコルは、既存インフラを再利用する巧妙な設計であり、監査エージェントが外部ツール利用ごとに自律的にマイクロペイメントを行う仕組みへの応用可能性がある
- MCPがデファクト標準になった理由（決済レールでなくツール接続の配管だから金の取り合いが起きにくい）と、決済プロトコルが乱立する理由（関所を握れば全取引から通行料を取れる）の非対称性は、エージェント間通信の標準化戦略を考える上で本質的な視点
- 「エージェントが何を選ぶか」という選択順位自体が広告枠として機能しうるという構造は、監査エージェントが外部情報源やツールを選択する際のバイアス・利益相反リスクとして内部統制設計に直接応用できる論点

## 前提知識

- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **HTTP 402 / x402** (TODO: 読むべき)
- **USDC / ステーブルコイン** (TODO: 読むべき)
- **computer-use（ブラウザ自動操作）** (TODO: 読むべき)
- **ERC-8004** (TODO: 読むべき)

## 関連記事

- /deep_1475 Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説
- /deep_6885 Tool Forge: ガバナンス付きエージェント実行のためのバリデーション内包型ツールチェーン
- /deep_3000 OpenClaw vs Hermes Agent：2つのオープンソースAIエージェントの設計思想を徹底比較
- /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- /deep_5398 LLMエージェント時代の上場企業データインフラ設計 — 4つの原則

## 原文リンク

[Agentのおつかいの現在地：Agentic Commerceの3系統と決済レール争い](https://zenn.dev/moimoi/articles/agentic-commerce-current-state)
