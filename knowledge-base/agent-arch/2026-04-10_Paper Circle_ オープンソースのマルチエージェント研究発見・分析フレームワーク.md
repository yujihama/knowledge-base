---
title: "Paper Circle: オープンソースのマルチエージェント研究発見・分析フレームワーク"
url: "https://tldr.takara.ai/p/2604.06170"
date: 2026-04-10
tags: [multi-agent, LLM, knowledge-graph, RAG, research-discovery, coder-LLM, orchestration, BibTeX, graph-QA]
category: "agent-arch"
memo: "[HF Daily Papers] Paper Circle: An Open-source Multi-agent Research Discovery and Analysis Framework"
processed_at: "2026-04-10T09:36:17.017743"
---

## 要約

科学論文の急増により、研究者が関連文献を効率的に発見・評価・統合することが困難になっている問題に対応するため、Paper Circleというマルチエージェントシステムが提案された。システムは2つの補完的なパイプラインで構成される。

(1) Discovery Pipeline：オフライン・オンラインの複数ソースからの検索を統合し、多基準スコアリング（multi-criteria scoring）、多様性考慮ランキング（diversity-aware ranking）、構造化出力を実装する。複数の検索源から論文候補を収集し、関連性・品質・多様性を加味したスコアで順位付けを行う。

(2) Analysis Pipeline：個々の論文を「概念」「手法」「実験」「図」などの型付きノードを持つ構造化ナレッジグラフに変換する。このグラフを用いてグラフ対応QA（graph-aware question answering）とカバレッジ検証を実現する。

両パイプラインは「コーダーLLM（coder LLM）」ベースのマルチエージェントオーケストレーションフレームワーク上に実装されており、各エージェントステップごとにJSON・CSV・BibTeX・Markdown・HTMLの完全再現可能な同期出力を生成する。エージェントはコードを書いて処理を実行するアプローチを採用しており、再現性と透明性を確保している。

評価では論文検索タスクと論文レビュー生成タスクの両方でベンチマークを実施し、Hit Rate・MRR（Mean Reciprocal Rank）・Recall@Kを指標として報告。より強力なエージェントモデルを使用するほど一貫した性能改善が見られた。コードはGitHubで公開（https://github.com/MAXNORM8650/papercircle）、デモサイトも公開済み。著者はSalman Khan、Fahad Shahbaz Khan他（2026年4月7日公開、arXiv: 2604.06170）。

## アイデア

- 論文を「概念・手法・実験・図」の型付きノードに分解してナレッジグラフ化するスキーマ設計は、監査証跡や規制文書の構造化にも転用できる
- 各エージェントステップで複数フォーマット（JSON/CSV/Markdown/HTML）を同期出力する設計により、パイプライン中断時の再現性と監査可能性が確保される
- コーダーLLM（コードを書いて実行するLLM）をオーケストレーターとして使う手法は、ツール呼び出しを静的に定義せず動的にコードで表現するため、エージェントの拡張性が高い

## Yujiの取り組みへの示唆

Paper Circleのナレッジグラフスキーマ（概念・手法・実験の型付きノード）は、監査エージェントが規制文書・内部統制文書を構造化する際の設計パターンとして参考になる。Discovery Pipelineの多基準スコアリングと多様性考慮ランキングは、LangGraphで実装する証拠収集エージェントに組み込める優先度付け手法として活用できる。また、各ステップで再現可能な構造化出力を生成するアーキテクチャは、監査プロセスのトレーサビリティ要件に直接対応できる設計思想である。

## 原文リンク

[Paper Circle: オープンソースのマルチエージェント研究発見・分析フレームワーク](https://tldr.takara.ai/p/2604.06170)
