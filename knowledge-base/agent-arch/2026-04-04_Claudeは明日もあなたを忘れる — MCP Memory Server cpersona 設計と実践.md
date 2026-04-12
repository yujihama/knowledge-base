---
title: "Claudeは明日もあなたを忘れる — MCP Memory Server cpersona 設計と実践"
url: "https://zenn.dev/cloto/books/claude-memory-mcp-server"
date: 2026-04-04
tags: [MCP, Memory, SQLite, cpersona, エピソード記憶, Confidence Score, Cascading Recall, マルチエージェント, Anti-Contamination, LLM永続化]
category: "agent-arch"
memo: "[Zenn LLM] Claudeは明日もあなたを忘れる — MCP Memory Server cpersona 設計と実践"
processed_at: "2026-04-04T21:10:03.157479"
---

## 要約

本書はClaude等のLLMに永続的記憶を持たせるMCPサーバー「cpersona」の設計と実装を解説した技術書（約106,939字、1,000円）。2026年3月30日公開、4月2日更新。著者はClotoCore開発者のCloto-dev氏。

核心的な問題意識は「LLMはセッションをまたいでユーザーのことを忘れる」という課題で、これをMCP（Model Context Protocol）を介したSQLiteベースの外部記憶システムで解決する。アーキテクチャは3層ハイブリッド構造：(1)エピソード記憶（会話の要約・蓄積）、(2)プロファイル記憶（ユーザー理解の継続的更新）、(3)Cascading Recall（多段検索による想起）。

技術的特徴として以下が挙げられる。スキーマ設計では記憶を構造化データとしてSQLiteに格納し、Confidence Score（確からしさのスコア）を各記憶エントリに付与することで記憶の信頼性を定量管理する。Cascading Recallは検索を多段階で実行し、関連度の高い記憶を段階的に召喚する設計。Anti-Contaminationはマルチエージェント環境においてエージェント間の記憶が混濁しないよう記憶空間を論理的に分離する機構。埋め込みプロバイダの選択と検索精度改良についても章を設け、ベクトル検索の実装選択肢を解説している。

チャプター構成は全13章で、クイックスタートから全ツール解説、設計概要、各記憶層の実装、発展的トピックまでを網羅。MCPのツール呼び出しインターフェース経由でClaudeが自律的に記憶の読み書きを行えるよう設計されており、LLMエージェントの文脈保持問題に対する実装レベルの解法を提供する。

## アイデア

- Confidence Scoreによる記憶の確からしさの定量化：各記憶エントリにスコアを付与することで、古い・矛盾した記憶を自動的に降格・排除するメカニズムが実現可能
- Anti-Contamination（エージェント間記憶分離）：マルチエージェントシステムでエージェントAの記憶がエージェントBに干渉しないよう論理的に名前空間を分離する設計は、複数の監査サブエージェントを持つシステムに直接応用可能
- Cascading Recall（多段検索）：単純なベクトル類似検索ではなく、複数段階のフィルタリングと想起を組み合わせることで、関連記憶の精度と網羅性を両立させるアーキテクチャパターン

## Yujiの取り組みへの示唆

LangGraphで構築中の監査エージェントシステムにおいて、監査セッションをまたいでコンテキスト（過去の指摘事項・企業固有リスク・監査判断の根拠）を保持する記憶レイヤーの設計にcpersonaの3層ハイブリッド構造が直接参考になる。特にAnti-Contamination設計は、複数クライアント・複数監査領域を扱うマルチエージェント構成で記憶汚染を防ぐ実装パターンとして有用。Confidence Scoreによる記憶品質管理は、LLM-as-judgeアーキテクチャと組み合わせることで監査証跡の信頼性スコアリングにも応用可能。

## 原文リンク

[Claudeは明日もあなたを忘れる — MCP Memory Server cpersona 設計と実践](https://zenn.dev/cloto/books/claude-memory-mcp-server)
