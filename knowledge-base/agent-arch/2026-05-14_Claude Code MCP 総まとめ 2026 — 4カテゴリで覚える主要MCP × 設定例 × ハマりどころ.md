---
title: "Claude Code MCP 総まとめ 2026 — 4カテゴリで覚える主要MCP × 設定例 × ハマりどころ"
url: "https://zenn.dev/trailfusionai/articles/ai-news-20260427191318-ee52d5"
date: 2026-05-14
tags: [MCP, Claude Code, Model Context Protocol, Context7, Playwright, GitHub MCP, エージェント設定, ツール統合]
category: "agent-arch"
related: [3379, 1738, 430, 2688, 4520]
memo: "[Zenn LLM] Claude Code MCP 総まとめ 2026 — 4カテゴリで覚える主要MCP × 設定例 × ハマりどころ"
processed_at: "2026-05-14T09:03:04.121227"
---

## 要約

2026年4月時点でClaude Codeに接続可能なMCP（Model Context Protocol）サーバーを4カテゴリに体系整理した実践ガイド。MCPの普及によりClaude・Cursor・Codex間でツール接続プロトコルが統一され、エージェントごとに独自実装を書く必要がなくなった点が最大の構造変化として示される。

4カテゴリの内訳は①プロジェクト連携（GitHub / Linear / Playwright / Sentry）、②データ・情報・AI支援（Brave / YouTube / Firecrawl / Context7 / Memory / PostgreSQL）、③検証・テスト自動化（Playwright / Puppeteer）、④外部エコシステム連携（AWS / Figma / Slack / Firebase / Google Drive / Notion）。

まず入れるべき最小5MCPとして GitHub・Context7・Playwright・Filesystem・Supabase が挙げられ、~/.claude/settings.json への具体的なJSON設定例も提示される。各MCPはnpxで起動し、APIキーはenv フィールドで渡す構成。

実装シナリオとして3例が紹介される。①Context7 MCPでNext.js 15の最新app router仕様を学習データ外からリアルタイム取得してコード生成、②GitHub MCPで先週のコミット履歴を取得しmarkdown整形→PR作成を会話内で完結、③Playwright MCPでブラウザ起動・DOM取得→E2Eテスト自動生成・実行・自動修正のループを実現。

MCPの有効性評価では、公式docs参照・GitHub操作・業務DB検索が◎、ブラウザ操作が○（起動が重いため）、大規模リファクタが△（素のコード直読の方が安定）、ローカルLLM推論には×（MCPはAPI側ツール接続用）と場面別に整理されている。

設定スコープは4階層（Managed / User / Project / Local）で管理され、チーム共通設定はrepo/.claude/settings.jsonにコミット、個人作業上書きはsettings.local.jsonに分離する設計が推奨される。

ハマりどころとして①GitHub PATをrepo:fullで渡すとgit push --forceが可能になるため最小権限原則の徹底、②環境変数不足による沈黙バグはclaude --debugで診断、③Playwright初回実行時にChromiumが約200MBダウンロードされるため事前にnpx playwright install chromiumを実行、④MCP数は5〜7個に絞らないとプロンプトが肥大化する点が明示される。

監査エージェント開発への示唆として、LangGraphベースのReActエージェントにLinear MCP（タスク管理）とPostgreSQL MCP（監査ログDB参照）を組み合わせることで、監査手続きの進捗管理とエビデンスDB検索を会話完結で実装できる可能性がある。また設定スコープの4階層はGRC観点での権限分離設計と親和性が高い。

## アイデア

- MCPによりClaude・Cursor・Codex間でツール設定が共通化され、一度書いた settings.json が複数エージェントで再利用可能になった点は、エージェント間の設定標準化として実務上の工数削減効果が大きい
- MCP数を5〜7個に制限するコンテキスト管理の原則は、RAGシステムのチャンク数制限と同じ設計哲学であり、エージェントの認知負荷（コンテキスト圧迫）を定量的に考える必要性を示している
- 大規模リファクタでMCPより素のコードベース直読が安定するという評価は、外部ツール呼び出しのオーバーヘッドと精度トレードオフを示しており、エージェント設計でのツール選択基準として参照できる

## 前提知識

- **Model Context Protocol (MCP)** (TODO: 読むべき)
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **npx / Node.js** (TODO: 読むべき)
- **PAT（Personal Access Token）** (TODO: 読むべき)
- **E2Eテスト自動化** (TODO: 読むべき)

## 関連記事

- /deep_3379 【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α
- /deep_1738 Claude Code の MCP サーバー活用術：外部ツール連携で開発効率を最大化する
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）

## 原文リンク

[Claude Code MCP 総まとめ 2026 — 4カテゴリで覚える主要MCP × 設定例 × ハマりどころ](https://zenn.dev/trailfusionai/articles/ai-news-20260427191318-ee52d5)
