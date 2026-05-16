---
title: "PersonalAI 2.0：知識グラフ traversal/retrieval と計画機構による個人化LLMエージェントの強化"
url: "https://tldr.takara.ai/p/2605.13481"
date: 2026-05-15
tags: [GraphRAG, 知識グラフ, BeamSearch, 多段階クエリ, LLM-as-a-Judge, 個人化AI, HotpotQA, RAG]
category: "agent-arch"
related: [1694, 971, 4715, 908, 4335]
memo: "[HF Daily Papers] PersonalAI 2.0: Enhancing knowledge graph traversal/retrieval with planning mechanism for Personalized LLM Agents"
processed_at: "2026-05-15T09:08:54.746353"
---

## 要約

PersonalAI 2.0（PAI-2）は、外部知識グラフ（KG）をLLMシステムに統合することで、既存のGraph RAG手法の限界を克服する新フレームワーク。既存のGraphRAG手法（LightRAG、RAPTOR、HippoRAG 2）が抱える静的・単段階クエリ処理の問題に対し、PAI-2は動的・多段階クエリパイプラインを導入する。

中核設計は「適応的・反復的情報探索」にある。具体的には、①抽出されたエンティティ、②グラフ上でマッチした頂点（vertex）、③生成されたclue-query（手がかりクエリ）の3要素に誘導されながら、KGをトラバースして情報を収集する。グラフ探索アルゴリズムとしてBeamSearchとWaterCirclesを採用し、標準的なflattenリトリーバーと比較して平均6%の精度向上を達成。さらに「サーチプラン強化機構」を有効化すると、無効化時と比較してLLM-as-a-Judge評価で18%のブーストを示す。

評価は6つのベンチマーク（Natural Questions、TriviaQA、HotpotQA、2WikiMultihopQA、MuSiQue、DiaASQ）で実施。比較手法に対してLLM-as-a-Judge指標で平均4%の精度向上を実現し、ハルシネーション率の低減と精度向上を定量的に示した。加えて、個人化情報保持能力を測るMINE-1ベンチマークではSOTA（89%のinformation-retention score）を達成。使用LLMは7B〜14Bパラメータ規模であり、大規模モデルに依存せず実用的なスケールで高性能を実現している点が特徴的。

監査エージェント開発への示唆：内部監査において、過去の監査調書・規制文書・リスク情報などを知識グラフとして構造化し、PAI-2型の多段階クエリ＋グラフ探索を組み合わせることで、単純ベクトルRAGよりも複雑な多ホップ推論（例：特定の内部統制が複数の規制要件にどう対応するかのトレース）が可能になる。BeamSearchベースのトラバーサルはLangGraph上のエージェントループと相性が良く、ReActパターンと組み合わせて実装できる可能性がある。

## アイデア

- clue-queryという概念：単なるクエリの書き換えではなく、グラフ上で発見したエンティティを基に次の探索方向を生成する仕組みが、ReActのThought-Action-Observationループと構造的に似ており、LangGraphのノード設計に直接転用できる
- WaterCirclesという独自グラフ探索アルゴリズム：BFSの波紋的拡散とBeamSearchの絞り込みを組み合わせた手法と思われ、知識グラフの局所的密度に適応できる可能性がある
- 7〜14Bモデルでの89% information-retention scoreはMINE-1 SOTA：大規模モデル（GPT-4等）なしで個人化知識の高精度保持が可能であることを示し、オンプレLLM（Ollama + RTX 3090環境）での実運用に有望

## 前提知識

- **GraphRAG** → /deep_762 HabitatAgent: 住宅相談のためのエンドツーエンド・マルチエージェントシステム
- **知識グラフ traversal** (TODO: 読むべき)
- **LLM-as-a-Judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **多ホップQA** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_1694 Plasma GraphRAG: ジャイロ運動論シミュレーション向け物理根拠に基づくパラメータ選択
- /deep_971 「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回
- /deep_4715 S2G-RAG：反復型RAG質問応答のための構造化十分性・ギャップ判定フレームワーク
- /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- /deep_4335 RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法

## 原文リンク

[PersonalAI 2.0：知識グラフ traversal/retrieval と計画機構による個人化LLMエージェントの強化](https://tldr.takara.ai/p/2605.13481)
