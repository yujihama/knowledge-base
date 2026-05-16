---
title: "FGDM: Chain-of-ThoughtとTree-of-Thoughtプロンプティングを用いたソフトウェアバグ検出のための推論対応マルチエージェントフレームワーク"
url: "https://tldr.takara.ai/p/2604.24831"
date: 2026-05-10
tags: [マルチエージェント, バグ検出, Chain-of-Thought, Tree-of-Thoughts, フローグラフ, FAISS, RAG, コード修正, LLM]
category: "agent-arch"
related: [762, 1252, 1844, 3446, 861]
memo: "[HF Daily Papers] FGDM: Reasoning Aware Multi-Agentic Framework for Software Bug Detection using Chain of Thought and Tree of Thought Prompting"
processed_at: "2026-05-10T09:38:29.073539"
---

## 要約

FGDMは、ソフトウェアバグ検出・修正を目的とした4エージェント構成のマルチエージェントフレームワーク。従来のDeep Learning手法は大規模・複雑なコードベースにおいてモジュール間依存関係の把握が弱いという課題があったが、FGDMはLLMの依存関係捕捉能力を活用してこれを解決する。

アーキテクチャは以下の4エージェントが順次動作する構成：(1) コードをフローグラフに変換するエージェント、(2) 誤りのあるセグメントを特定するエージェント、(3) 修正コードを生成するエージェント、(4) 全体を統括するエージェント（論文中の詳細による）。全エージェントはChain-of-Thought（CoT）およびTree-of-Thoughts（ToT）プロンプティングを使用し、段階的・分岐的な推論を実現する。また、FAISS векторデータベースを統合し、過去の類似バグとその修正事例をRAGで取得・参照する。

評価はAnsible、Black、FastAPI、Keras、Luigi、Matplotlib、Pandas、Scrapy、SpaCy、Tornadoを含む複数OSSプロジェクトから100プログラム（PythonおよびC）を対象に実施。既存手法との比較で、Python/CそれぞれのLevenshtein距離を平均24.33・8.37削減し、コサイン類似度は0.951・0.974を達成した。

監査エージェント開発への示唆：コードレビューや内部統制チェックリストの検証プロセスにおいて、フローグラフ変換→異常箇所特定→修正案生成という本フレームワークの逐次エージェント構成は参考になる。特にCoT+ToTの組み合わせで推論経路を明示化しつつFAISSで過去事例を参照するパターンは、LangGraphベースの監査エージェントにおける証拠収集→リスク判断→是正提案フローに直接応用可能。

## アイデア

- コードをフローグラフに変換してからLLMエージェントに渡すことで、モジュール間依存関係を構造化情報として扱える点が設計的に巧み
- CoTとToTを組み合わせることで、直線的な推論（CoT）と分岐探索的な推論（ToT）を同一エージェントに持たせ、バグ特定の精度と修正候補の多様性を両立させている
- FAISSによる類似バグ事例のRAG参照を組み込むことで、LLMの汎用的な推論能力だけでなくドメイン固有の修正知識を活用できる設計になっており、知識蓄積型エージェントとしての発展可能性がある

## 前提知識

- **Chain-of-Thought prompting** (TODO: 読むべき)
- **Tree-of-Thoughts** (TODO: 読むべき)
- **マルチエージェントフレームワーク** → /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- **FAISS** → /deep_487 Nishika 日本酒銘柄画像検索コンペ 7位解法（備忘録）
- **フローグラフ解析** (TODO: 読むべき)

## 関連記事

- /deep_762 HabitatAgent: 住宅相談のためのエンドツーエンド・マルチエージェントシステム
- /deep_1252 DSPyによる宣言的学習を用いたLLMプロンプトエンジニアリングの最適化
- /deep_1844 Argus: マルチエージェントアンサンブルによる静的解析の再編成とフルチェーン脆弱性検出
- /deep_3446 表形式データの自動特徴量生成のためのメモリ拡張LLMベースマルチエージェントシステム（MALMAS）
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力

## 原文リンク

[FGDM: Chain-of-ThoughtとTree-of-Thoughtプロンプティングを用いたソフトウェアバグ検出のための推論対応マルチエージェントフレームワーク](https://tldr.takara.ai/p/2604.24831)
