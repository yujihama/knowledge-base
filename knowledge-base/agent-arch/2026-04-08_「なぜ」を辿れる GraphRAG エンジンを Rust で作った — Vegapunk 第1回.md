---
title: "「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回"
url: "https://zenn.dev/ryugo/articles/vegapunk-01-why-graphrag"
date: 2026-04-08
tags: [GraphRAG, Rust, traceable_pairs, ナレッジグラフ, RAG, gRPC, Node2Vec, ローカルLLM]
category: "agent-arch"
memo: "[Zenn LLM] 「なぜ」を辿れる GraphRAG エンジンを Rust で作った"
processed_at: "2026-04-08T21:51:22.064898"
---

## 要約

Vegapunk は Rust 製の根拠追跡型 GraphRAG エンジンで、全6回シリーズの第1回として「なぜ作ったか」を解説している。

【背景・課題】通常のベクトル検索 RAG は「意味的な近さ」には強いが、「論理的な関係性」の追跡が苦手。例えば「PostgreSQL をやめた理由は？」と聞いても、単に PostgreSQL に言及したテキストが返るだけで、「運用コストが想定の3倍だった」という根拠や「鈴木が調査し田中が判断した」という意思決定文脈は辿れない。Microsoft GraphRAG（2024年公開）はナレッジグラフ自動構築で俯瞰クエリに対応したが、①GPT-4必須でコスト高（1万ドキュメントで$50〜200）、②CLI バッチ処理前提でリアルタイム投入不可、③スキーマが汎用的すぎて「なぜ」の構造的追跡が保証されない、という3つの問題があった。

【中核概念: traceable_pairs】Vegapunk の核心は YAML スキーマで「主張（claim）」と「根拠（evidence）」の関係をエッジタイプとともに宣言する traceable_pairs。例えば Decision ノードと Rationale ノードを BECAUSE エッジで結ぶと、①LLM抽出プロンプトへの明示的指示が可能になり1.5Bパラメータの小型LLMでも実用精度が出る、②検索ヒット時に BECAUSE エッジを自動展開して根拠も返す、③traceability スコアで根拠追跡率を定量評価できる、という3つの効果が生まれる。

【検索の仕組み】ベクトル検索とグラフ走査を単一の Search RPC で提供。クエリをベクトル化→ベクトル検索でヒット→ヒットノードから traceable_pairs エッジを辿ってグラフ走査、という処理をクライアントに透過的に実施。

【5つの設計原則】①テキスト投入のみでクライアントはグラフ構築を意識しない、②デフォルトでローカルLLM/Embedding完結（完全オフライン動作）、③ベクトル検索+グラフ走査の一体操作、④保存・Embeddingは同期/LLM推論は非同期分離でリアルタイム投入を実現、⑤localhost バインド＋LAN公開時は認証強制。

【MS GraphRAG との比較】Vegapunk は常駐 gRPC サーバでリアルタイム投入が可能、ローカル実行でコスト実質ゼロ、根拠追跡性を定量評価、Node2Vec による構造検索対応、LLM不使用で低レイテンシ、完全オフライン動作、Rust シングルバイナリという点で MS GraphRAG v3.0.8 と差別化している。

## アイデア

- traceable_pairs という概念でスキーマレベルに「主張と根拠の関係」を定義することで、LLMの抽出プロンプト品質・検索時の自動展開・定量評価（traceabilityスコア）の3つを同時に解決している点が設計上秀逸
- 保存パス（同期: グラフ+ベクトルDB書き込み）とLLM推論パス（非同期: エンティティ抽出）を分離することで、バッチ前提だった GraphRAG をリアルタイム投入可能なアーキテクチャに転換している
- 1.5Bパラメータの小型LLMでも実用精度を出せるとしており、スキーマによる抽出対象の絞り込みがモデルサイズとコストのトレードオフを改善する手法として興味深い

## Yujiの取り組みへの示唆

監査エージェント開発において「なぜその判断をしたか」の根拠追跡は内部監査の文書化要件と直結する。traceable_pairs の概念（Decision→BECAUSE→Rationale）は LangGraph の状態遷移ログや Pydantic モデルで表現する監査証跡スキーマ設計に直接応用できる。また、Microsoft GraphRAG のコスト問題を回避しつつローカルLLMで動作する点は、機密性の高い監査データを扱うユースケースにおいてインフラ選定の参考になる。traceability スコアによる定量評価はLLM-as-judgeの評価軸設計にも示唆を与える。

## 原文リンク

[「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回](https://zenn.dev/ryugo/articles/vegapunk-01-why-graphrag)
