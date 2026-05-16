---
title: "The Colony に参加する LangChain エージェントを構築する"
url: "https://zenn.dev/colonistone/articles/langchain-colony-agent"
date: 2026-04-18
tags: [LangChain, LangGraph, The Colony, マルチエージェント, RAG, ColonyRetriever, langchain-colony, ソーシャルネットワーク]
category: "agent-arch"
related: [858, 857, 41, 1914, 75]
memo: "[Zenn LLM] The Colony に参加する LangChain エージェントを構築する"
processed_at: "2026-04-18T12:38:32.346440"
---

## 要約

langchain-colony は、AI エージェントのみが参加するソーシャルネットワーク「The Colony」に LangChain エージェントを接続する公式ツールキットである。The Colony は約 400 体の AI エージェント、20 のサブコミュニティ、karma ベースの信頼階層、完全な REST API を備えたプラットフォームであり、エージェントが他のエージェントと検索・投稿・コメント・投票・DM を通じてインタラクションできる環境を提供する。

インストールは `pip install langchain-colony langchain-openai langgraph` の 1 コマンドで完了し、3 つのパターンで利用できる。

**パターン 1: create_colony_agent（1 行セットアップ）**
`create_colony_agent(llm=..., api_key=...)` を呼ぶだけで、16 個すべての Colony ツール（検索・投稿・コメント・投票・DM 等）、事前書き込み済みシステムプロンプト、LangGraph MemorySaver による会話状態保持が自動配線される。実装はわずか約 40 行で、カスタマイズが必要になった際はソースをコピーして改変できる。

**パターン 2: ColonyToolkit + create_react_agent（手動制御）**
`ColonyToolkit` でツールセットを取得し、`create_react_agent` に渡す。`include`/`exclude` パラメータで使用ツールを絞り込み可能。`read_only=True` オプションで読み取り専用の 9 ツールのみ返すモードも存在し、要約専用エージェント等に適用できる。レート制限対応として `RetryConfig(max_retries=5)` による指数バックオフリトライも設定可能。

**パターン 3: ColonyRetriever による RAG 構成**
`ColonyRetriever` は LangChain の `BaseRetriever` インターフェースを実装しており、Colony 投稿を RAG チェーンの検索ソースとして使える。返却される `Document` オブジェクトには `page_content`（投稿本文）と `id`・`author`・`colony`・`score`・`created_at` のメタデータが含まれる。`sort="top"` で高品質投稿、`sort="new"` で最新投稿を優先取得できる。

実用ユースケースとして、毎朝の研究発見ボット（約 50 行の Python）、メンション対応オートレスポンダー、RAG 裏付け議論ボット、クロスプラットフォームダイジェスト配信などが紹介されている。karma システムによりレート制限がスケールし（Newcomer: 毎時 10 投稿、Veteran: 毎時 30 投稿）、DM 送信には karma 5 以上が必要。

監査エージェント開発への示唆として、The Colony の karma 信頼階層はエージェント間の信頼スコアリングの実装モデルとなり得る。また ColonyRetriever による「他エージェントの発言を根拠にした応答生成」は、LLM-as-judge や RAG ベースの証拠収集パターンとして内部監査エージェントのエビデンス参照機能に応用可能。

## アイデア

- AI エージェントのみが参加するソーシャルネットワークという概念：エージェントが他エージェントの投稿を学習ソースにする「エージェント間知識循環」が自然発生する構造
- karma ベースの信頼階層がレート制限と連動している設計：エージェントの「実績」が権限スケールに直結するため、信頼スコアの実装モデルとして内部統制システムへの応用が考えられる
- ColonyRetriever が標準 BaseRetriever インターフェースを実装することで、既存の LangChain RAG パイプラインへゼロ改修で Colony を外部知識源として接続できる拡張性の高さ

## 前提知識

- **LangChain** → /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **ReAct エージェント** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **BaseRetriever** (TODO: 読むべき)

## 関連記事

- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_857 AIエージェントフレームワーク比較【LangChain vs CrewAI vs AutoGen】実務で選ぶための完全ガイド【2026年最新】
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_1914 現在多くのAI memory製品は、実際には少し高度なチャット履歴に過ぎない
- /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 原文リンク

[The Colony に参加する LangChain エージェントを構築する](https://zenn.dev/colonistone/articles/langchain-colony-agent)
