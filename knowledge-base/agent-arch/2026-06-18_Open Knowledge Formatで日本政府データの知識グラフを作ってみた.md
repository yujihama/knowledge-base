---
title: "Open Knowledge Formatで日本政府データの知識グラフを作ってみた"
url: "https://zenn.dev/michy/articles/b7c9e2a4f6d810"
date: 2026-06-18
tags: [OKF, 知識グラフ, MCP, LLM-Agent, RAG, オープンデータ, 国土数値情報, データカタログ]
category: "agent-arch"
related: [7286, 4520, 1784, 2404, 7417]
memo: "[Zenn LLM] Open Knowledge Formatで日本政府データの知識グラフを作ってみた"
processed_at: "2026-06-18T09:03:05.865888"
---

## 要約

Open Knowledge Format（OKF）はGoogleが公開した軽量フォーマットで、MarkdownファイルとYAML frontmatterで知識を表現し、知識グラフとして可視化できる。本記事は国土交通省「国土数値情報」（行政区域データ・駅別乗降客数・地価公示データ）をOKF化した実験ログである。

作成したbundle（japan_urban_knowledge）は、datasets/tables/metrics/concepts/areas/referencesの6層ディレクトリ構造を持ち、各Markdownファイルのfrontmatterに type・tags・timestamp 等を記述する。Markdownリンクがグラフのedgeになり、viz.htmlとしてグラフビューアが生成される。

設計上の重要な決定として3点挙げられる。①ノード種別の明示：Government Data Portal・Government Dataset・GIS Feature Table・Metric・Code Concept・Domain Concept・Area Instance・Referenceの8種に分類し、viewer側でtype別に色分けする。②親子関係の表現：Markdownリンクは参照方向（渋谷区→東京都）になるが、frontmatterのparentフィールドで逆向きの親子edge（東京都→渋谷区）を補完する。③join情報の管理：Column NodeやJoin Relationship Nodeによる完全グラフ化は小規模bundleでは過剰となるため、テーブル文書内の「結合」セクションにjoinキー・cardinality・推奨join種別を自然言語で記載する方式を採用。

Agent活用においては、OKF bundleを全文プロンプトに貼るより、MCP serverやライブラリ経由でtype検索・ノードトラバーサル・join情報取得をAPI化する方が安定する。「港区の駅周辺で地価が高いエリアを見たい」というクエリに対し、AgentはOKFをたどってmunicipality_codeによるleft join・駅との空間結合（st_dwithin 500m）・駅名単独集計の重複リスクを把握し、適切なSQLを生成できる。

OKFはBigQueryプロパティグラフとは異なり、クエリ実行エンジンではなく「SQLを書く前に読む文脈レイヤー」である。DDLだけでは伝わらない業務概念・粒度・join注意点を人間とLLM Agent双方が読める形で管理する用途に適する。実用化には組織ごとのfrontmatter運用ルール（category・parent・join_hints・grain・Agent Notesセクション）を事前に定義することが不可欠。

監査エージェント開発への示唆：内部監査においても複数のデータソース（ERP・GL・サブシステム）のjoin関係や業務概念（勘定科目体系・承認階層）をOKF化し、MCPツール経由でAgentに読ませることで、ハルシネーションを抑制しながら正確なデータ取得クエリを生成させる構成が有望。

## アイデア

- Markdownリンクをグラフedgeとして解釈するOKFの設計により、既存のMarkdownドキュメントを最小限の変更で知識グラフ化できる点
- frontmatterのparentフィールドで参照方向と親子方向を分離し、グラフの意味的一貫性を保つ拡張パターン
- OKFをMCP server化してAgentにtype検索・ノードトラバーサルAPIを提供することで、全文検索より安定した文脈取得が実現できる設計

## 前提知識

- **OKF（Open Knowledge Format）** (TODO: 読むべき)
- **YAML frontmatter** → /deep_3895 Claude Code Routineの設定をfrontmatterでConfig as Code管理する
- **知識グラフ** → /deep_2701 MCPThreatHive: Model Context Protocolエコシステム向け自動脅威インテリジェンスプラットフォーム
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **空間結合（st_dwithin）** (TODO: 読むべき)

## 関連記事

- /deep_7286 誰も教えてくれないベクトル検索RAGの真実
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_7417 ローカルLLMで「PoC止まり」にしない業務AIエージェント ― MCP＋RAG評価まで一気通貫

## 原文リンク

[Open Knowledge Formatで日本政府データの知識グラフを作ってみた](https://zenn.dev/michy/articles/b7c9e2a4f6d810)
