---
title: "AI AgentメモリーOSS「MemPalace」徹底解説 — 記憶の宮殿アーキテクチャとベンチマーク論争"
url: "https://zenn.dev/npcver/articles/61ad95d56c2aca"
date: 2026-04-09
tags: [MemPalace, AIメモリー, MCP, Knowledge Graph, ChromaDB, SQLite, AAAK圧縮, LongMemEval, ローカルLLM, RAG]
category: "agent-arch"
memo: "[Zenn LLM] バイオハザードのアリスが建てた「記憶の宮殿」— AI AgentメモリーOSS MemPalace 徹底解説"
related: [9, 1247, 971, 1475, 1423]
processed_at: "2026-04-09T21:38:05.991072"
---

## 要約

MemPalaceは、映画バイオハザードのMilla Jovovich氏とBen Sigman氏が共同開発したAIエージェント向けオープンソースメモリーシステム。公開後2日でGitHub Star 8,800超を獲得。既存のMem0やZepが「AIに何を覚えるかを判断させる（LLM要約・選別方式）」のに対し、MemPalaceは「Store everything, then make it findable（全保存 + 構造検索）」という逆転の設計思想を採用する。

アーキテクチャはMethod of Loci（記憶の宮殿）を模した階層構造で、Palace → Wing（人/プロジェクト単位） → Room（具体トピック） → Closet（圧縮サマリ）/ Drawer（原文保存）という4層で構成される。Wing内のRoom間はHall（廊下）でfacts/events/discoveries/preferences/adviceの5タイプにより接続され、異なるWing間の同名Roomは自動でTunnel（トンネル）が張られる。22,000件の実会話メモリーを用いた検証では、全Closet検索（Recall@10: 60.9%）に対し、Wing+Room絞り込みで94.8%（+34%）を達成している。

ストレージはChromaDB（ベクトル検索）+ SQLite（Knowledge Graph）のローカル完結構成でAPIキー・クラウド不要。年間コストは約$10（LLM要約方式の$507と比較）。MCPサーバーとして19ツールを提供し、Claude CodeやCursorから直接利用可能。また、AAAK（AI専用ロスレス圧縮方言）により同一情報を約8倍圧縮し、起動時はL0+L1の約170トークンのみをロードする4層メモリースタックを実現する。SQLiteベースのTemporal Entity-Relationship Graphにより、ファクトに有効期間を付与した時系列クエリと矛盾検出機能も備える。

ただしベンチマーク論争も注目される。公式のLongMemEval 96.6%（Raw）は検索リコール（ステップ1）のみの評価であり、生成・判定を含むend-to-endではない。LoCoMoではtop_k=50設定により全セッションが候補に入り実質的に無効なテストとなっている。AAAKの「ロスレス」主張に対しても、Raw（96.6%）→AAAK圧縮後（84.2%）で12.4ポイントの品質低下が計測されている。100%スコアはdev-setへの個別パッチを含む。一方でBENCHMARKS.mdには5,000語超の方法論ノートで制約を自己開示しており、構造による+34%の精度向上はPenfield Labsの批判記事でも否定されていない。

## アイデア

- 「全保存 + 構造検索」vs「LLM選別要約」という設計思想の対立: 要約で文脈を失う問題をフォルダ階層（Wing/Room）で解決し、構造自体がRecall精度を+34%向上させるという知見は、RAGシステム設計全般に応用可能
- Temporal Knowledge GraphをSQLiteで実装するアプローチ: Neo4jなど外部DBに依存せず、ファクトに有効期間（valid_from/ended）を付与してas_ofクエリや矛盾検出を実現する軽量設計
- AAAK（AI専用圧縮方言）の概念: 人間可読性を捨ててAIの読解速度に最適化した短縮表記で約8倍圧縮。モデル非依存で自動学習される設計は、コンテキスト効率化の新しいアプローチ
## 関連記事

- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_971 「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回
- /deep_1475 Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説
- /deep_1423 Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）

## 原文リンク

[AI AgentメモリーOSS「MemPalace」徹底解説 — 記憶の宮殿アーキテクチャとベンチマーク論争](https://zenn.dev/npcver/articles/61ad95d56c2aca)
