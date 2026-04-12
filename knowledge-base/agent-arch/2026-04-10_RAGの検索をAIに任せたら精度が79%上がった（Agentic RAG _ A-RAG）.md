---
title: "RAGの検索をAIに任せたら精度が79%上がった（Agentic RAG / A-RAG）"
url: "https://zenn.dev/plasmon/articles/20260408-unknown-bcd7c6"
date: 2026-04-10
tags: [Agentic-RAG, RAG, multi-hop-QA, tool-use, ChromaDB, LangGraph, retrieval-strategy]
category: "agent-arch"
memo: "[Zenn LLM] RAGの検索をAIに任せたら精度が79%上がった"
processed_at: "2026-04-10T09:34:53.802423"
---

## 要約

arXiv:2602.03442が提案するA-RAG（Agentic RAG）は、従来の固定パイプライン型RAG（クエリ→ベクトル検索→Top-K取得→LLM）をエージェントによる自律的な検索に置き換えるアーキテクチャ。従来RAGの3つの構造的限界——①マルチホップ質問への弱さ（1回の検索で答えが得られない）、②検索粒度の固定（Top-K=5のように質問の複雑度に関係なく均一取得）、③検索戦略の固定（ベクトル検索のみ等）——を、エージェントが自律判断することで解消する。A-RAGはエージェントに3つのツールを提供する：keyword_search（固有名詞・型番向け）、semantic_search（概念的類似性向け）、chunk_read（特定チャンクの精読）。エージェントはこれらをどの順序で何回呼ぶかを質問に応じて動的に決定し、十分な情報が集まった時点で検索を停止する。ベンチマーク結果では、GPT-5-miniバックエンドでNaive RAGと比較して、2WikiMultiHopQAで50.2%→89.7%（+79%）、MuSiQueで52.8%→74.1%（+40%）、HotpotQAで81.2%→94.5%（+16%）を達成。さらにHotpotQAの取得トークン数はNaive RAGの5,358から2,737へ-49%削減され、精度向上とコスト削減が同時に実現された。これはエージェントが必要最小限の情報だけを選択的に取得することでLLMへのノイズが減るためと説明される。モデルが強いほど改善効果が大きく（GPT-4o-miniでの平均+21% vs GPT-5-miniでの平均+45%）、エージェントのplanning・reflection能力がモデル性能に依存することが示された。GraphRAGはGPT-4o-miniではHotpotQA 33.2%（Naive RAGの半分以下）に落ち込む一方、GPT-5-miniでは82.5%を記録し、弱いモデルでの使用リスクも明示された。ローカルLLMではQwen2.5-32B Q4_K_Mで単純なAgentic RAGは動作可能だが、マルチホップの複雑な推論は困難で、改善率はGPT-5-miniの1/3程度（+15〜25%）と推定される。Agentic RAGが有効なのはマルチホップ質問が多い・知識ベースが大規模・精度最優先のユースケースで、FAQ・小規模・低レイテンシ優先のケースはNaive RAGで十分とも整理されている。

## アイデア

- 検索粒度と検索戦略をエージェントが動的決定することで、固定Top-Kの過剰取得・過少取得を同時に解消できる設計思想
- 精度向上と検索トークン削減が同時に達成される逆説的な結果——これはノイズ削減によるLLMの集中度向上として説明される
- GraphRAGは弱いモデルで崩壊するが、A-RAGはモデルが弱くても最低限機能するという堅牢性の差

## Yujiの取り組みへの示唆

監査エージェント開発では「ある勘定科目の異常を発見した人物の承認フロー上位者を特定する」のようなマルチホップ質問が頻出するため、A-RAGの検索エージェント設計はLangGraphのノード構成に直接応用できる。keyword_search / semantic_search / chunk_readの3ツール構成はLangGraphのToolNodeとして実装可能で、エージェントが検索ステップ数を動的決定するパターンはReActループの具体的な実装例として参考になる。また、取得トークン-49%・精度+79%というトレードオフ特性は、監査レポート生成のAPIコスト最適化を議論する際に定量根拠として使える。

## 原文リンク

[RAGの検索をAIに任せたら精度が79%上がった（Agentic RAG / A-RAG）](https://zenn.dev/plasmon/articles/20260408-unknown-bcd7c6)
