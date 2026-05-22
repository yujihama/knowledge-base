---
title: "Vector DBを外したら、RAGではなくAgent Runtimeが残った"
url: "https://zenn.dev/mofuteq/articles/8a2193df98ac05"
date: 2026-05-22
tags: [RAG, RAR, LangGraph, 推論構造外部化, typed artifact, Agent Runtime, epistemic honesty, LangGraph state machine, 軽量LLM]
category: "agent-arch"
related: [858, 2255, 2877, 1337, 5264]
memo: "[Zenn LLM] Vector DBを外したら、RAGではなくAgent Runtimeが残った"
processed_at: "2026-05-22T09:03:15.515608"
---

## 要約

著者はfashion/stylingドメインのトレンド分析システムをRAGで構築しようとしたが、実装を進めるうちにVector DBと単純なretrieve→generateパイプラインでは不十分であることに気づいた。問題の核心は「推論構造がLLMの内部に閉じており、外から観測も制御もできない」点にあった。具体的には、矛盾するevidenceがLLMのprose生成に吸収されてconflictが消える、trashノイズとcanonical signalの区別ができない、recommendation driftが起きるといった問題が発生した。

これを解決するためにRAR（Retrieval Augmented Reasoning）という設計思想を構築した。RAGが「contextの量を増やしてより良い回答を生成する」のに対し、RARは「推論構造をruntime側へ外出しし、可視・制御・復旧可能にする」ことを目的とする。

具体的な実装として3つの設計判断を行った。①retrieval laneの分離：canonical_query（長期的baseline signal）とemerging_query（現在のnoise/drift）を分け、「何を見るために取得するか」を先に構造化してからretrieveする。②typed artifact：WebSource、Claim（claim_typeとしてobservation/interpretation/signal/normを持つ）、StructuredDraft、FinalAnswerRubricなどの中間表現をschema化し、LLMを「自律的reasoner」ではなく「schema埋めるtransformation component」として扱う。③conflicts/gapsの明示的保持：StructuredDraftの必須フィールドとしてconflictとgapを残し、epistemic honestyをruntime側で担保する。

システム構成はStreamlit UI→FastAPI boundary→LangGraph state machine→SQLite checkpoint→typed artifacts→SSE workflow statusとなり、UIはThinking...ではなくRetrieving evidence/Extracting claims/Structuring conflictsなどのworkflow stateを表示する。モデルはgemini 3.1 flash lite系の軽量モデルを使用し、コストを抑えつつ推論の脱線を防ぐ設計（runtime側が構造を保持）により品質を維持できた。

設計思想の根底には「frames, not verdicts」というthesisがある。AgentはRecommendationを返すのではなく、interpreted rule・reference frame・traceable evidence・conflict/gap・structured uncertaintyを返す。これはdisclaimerを増やす安全策ではなく、authority boundaryの設計であり「Agent designはモデルの中ではなく、モデルを囲む構造にある」という結論に至った。監査AIにおける判断根拠の透明性確保や、LLM-as-judgeの評価構造設計に直接応用できる考え方である。

## アイデア

- LLMを『自律的reasoner』ではなく『schema埋めるcontrolled transformation component』として扱うことで、軽量モデルでも推論品質を維持できるという逆説的アプローチ
- conflicts/gapsを消すのではなく構造化されたフィールドとして必須保持することで、epistemic honestyをruntime側の設計問題に落とし込む発想
- canonical_queryとemerging_queryの分離により、retrieval意図を先に構造化してからretrieveするという『reasoning-first retrieval』の順序逆転

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **State Machine** (TODO: 読むべき)
- **Typed Schema / Pydantic** (TODO: 読むべき)
- **principal-agent問題** (TODO: 読むべき)

## 関連記事

- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_2255 The Colony に参加する LangChain エージェントを構築する
- /deep_2877 SemiFA：半導体故障解析レポートを自律生成するエージェント型マルチモーダルフレームワーク
- /deep_1337 RAGの検索をAIに任せたら精度が79%上がった（Agentic RAG / A-RAG）
- /deep_5264 Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS

## 原文リンク

[Vector DBを外したら、RAGではなくAgent Runtimeが残った](https://zenn.dev/mofuteq/articles/8a2193df98ac05)
