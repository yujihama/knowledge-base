---
title: "CursorのAgentからRubyDexをMCP経由で使う：Railsモノリスのコード構造クエリを高速化する"
url: "https://zenn.dev/kota_koyama/articles/a0cd2f1d59ef72"
date: 2026-05-11
tags: [MCP, RubyDex, Cursor, AST解析, Ruby, LLM Agent, コードインデクサー, Shopify, Rust, Rails]
category: "agent-arch"
related: [1936, 430, 4912, 2550, 2688]
memo: "[Zenn LLM] Cursor の Agent から RubyDex を使う - MCP 経由でコード構造を直接クエリする"
processed_at: "2026-05-11T09:37:55.575860"
---

## 要約

RubyDexはShopifyが公開しているRust製のRubyコードインデクサーで、RubyKaigi 2026で発表された。プロジェクト全体をAST解析して事前インデックスを構築し、MCPサーバーとして構造的なクエリに答える。RubyLSPと比較して約10倍高速、メモリ消費は半分以下という性能を持ち、発表後のPR最適化でさらに解決時間50.2s→16.7s（約3倍）・インデックス構築63.2s→29.0s・メモリ使用量5531MB→3447MB（-38%）といった改善が入っている。

本記事では、CursorのAgentからRubyDexをMCP経由で利用するセットアップ手順と実測ベンチマークを報告している。セットアップはRustツールチェインでrubydex_mcpバイナリをビルドし、.cursor/mcp.jsonにMCPサーバーとして登録するだけで完了する。なお.mcp.json（ドット1つ）はClaude Code用でありCursorは読まないため、両ツールから使う場合は両方の設定ファイルに記述が必要。

RubyDexが提供するツールは、クラス・メソッド・定数のあいまい検索（search_declarations）、完全修飾名での詳細取得と継承ツリー表示（get_declaration）、定数の全参照抽出（find_constant_references）、ファイル単位の宣言一覧（get_file_declarations）、インデックス統計（codebase_stats）など。3050ファイル・13136宣言・メソッド参照52万件超のRailsモノリスで動作確認している。

実測ベンチマークでは、SomeModelの参照調査タスクにおいてRubyDexなしが210秒・9 tool callsに対し、RubyDexありは53秒・7 tool callsで約75%（4倍）高速化。RubyDexなしはgrepでテキストパターンマッチを繰り返し定義ファイル本体もヒットしてしまうのに対し、RubyDexはAST解析により外部参照のみを正確に抽出できる。タイミー技術ブログの検証では参照調査タスクで-56.9%、構成把握タスクで-44.0%のトークン削減も報告されている。

Ruby LSPとの棲み分けは明確で、エディタ上での人間操作（hover・定義ジャンプ・補完）はRuby LSP、Agent経由のコード構造調査はRubyDex（MCP）が担う。CursorのAgentからLSPのgoToDefinitionやfindReferencesを直接ツールとして呼ぶインターフェースは標準では提供されておらず、その役割をRubyDexが補完する形になる。監査エージェント開発への示唆としては、Railsモノリス的な大規模コードベースを対象とするエージェントがgrep+Readループを脱却してAST構造クエリを活用する設計パターンは、コードレビュー自動化や影響範囲分析を行う監査エージェントのツール設計にも直接応用できる。

## アイデア

- MCPサーバーとしてAST解析インデックスを公開することで、LLM Agentがgrepベースのテキストマッチを脱却し構造的なコードクエリを1クエリで実行できる設計パターン
- .cursor/mcp.jsonと.mcp.jsonを使い分けることでCursorとClaude Codeが同一RubyDexバイナリ（同一インデックス）を共有できる点：MCP起動時に毎回インデックス再構築するためズレが生じない
- 参照調査タスクで75%の時間短縮・56.9%のトークン削減という定量結果：AgentのツールにAST構造クエリを追加することのROIを実測で示した点

## 前提知識

- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **AST解析** (TODO: 読むべき)
- **Cursor Agent** (TODO: 読むべき)
- **Ruby LSP** (TODO: 読むべき)
- **Rustツールチェイン** (TODO: 読むべき)

## 関連記事

- /deep_1936 🤗 APIユーザー向けTransformer推論を100倍高速化した方法
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_4912 論文から再実装してわかったHNSW近傍探索の本当の難所 — pgvectorの中身を理解する
- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」

## 原文リンク

[CursorのAgentからRubyDexをMCP経由で使う：Railsモノリスのコード構造クエリを高速化する](https://zenn.dev/kota_koyama/articles/a0cd2f1d59ef72)
