---
title: "Vector RAG vs LLMコンパイルWiki：小規模マルチドメイン研究コーパスでの事前登録比較"
url: "https://tldr.takara.ai/p/2605.18490"
date: 2026-05-20
tags: [RAG, Vector RAG, LLM-as-judge, preregistration, research synthesis, citation grounding, decomposition RAG, knowledge compilation]
category: "ai-ml"
related: [112, 2563, 75, 2877, 93]
memo: "[HF Daily Papers] Vector RAG vs LLM-Compiled Wiki: A Preregistered Comparison on a Small Multi-Domain Research"
processed_at: "2026-05-20T09:17:31.490376"
---

## 要約

本研究は、LLMが小規模研究コーパス（24論文）に対して質問に答える際の2つのアーキテクチャを事前登録（preregistered）形式で比較したものである。比較対象は「単一ラウンドのVector RAGシステム」と「LLMがコンパイルしたMarkdown形式のWiki」で、同一の回答生成モデルを使って13の質問に答えさせ、ブラインド状態のLLMジャッジがスコアリングした。

【主な結果】
- **論文横断的な知見の統合**：WikiがRAGを大幅に上回った。複数論文にまたがる合成・比較が必要な質問ではWikiが優位。
- **単一事実の検索（lookup）**：RAGが事前登録した検定基準を満たした。単純な事実確認タスクではRAGが有効。
- **クエリコスト**：予想に反してWikiの方がRAGよりクエリトークン消費量が多く、Wikiのビルドコストをクエリ削減で回収できなかった。
- **引用の正確性（claim-level citation）**：Wikiが優位。RAGは全体的なgroundednessスコアは高いが、各クレームを支持する引用の精度ではWikiに劣る。
- **Decomposition-based RAG変種**：通常RAGより低いLLMトークンコストで、論文横断合成においてWikiに近い性能を達成。ただしclaim単位の引用精度はWikiに及ばなかった。

【背景・手法】
事前登録（preregistration）とは、仮説と分析計画をデータ収集前に公開登録する手法で、後付け解釈のバイアスを防ぐ。本研究はこれをNLP/AI評価に適用した点が特徴的。LLMジャッジはブラインド評価を実施し、judge adjustment（ジャッジのバイアス補正）も行った。

【主要な示唆】
「grounded research synthesis（根拠付き研究合成）」は単一の能力ではなく、(1)証拠の整理・構造化、(2)クレーム単位の引用サポート、(3)実行コスト、という3つの軸が存在し、どのアーキテクチャも全軸で最優秀ではなかった。監査エージェント開発への示唆として、複数文書にまたがるエビデンス合成が必要な監査タスクではWikiまたはDecomposition RAGが有効で、単純な規程・基準の検索にはVector RAGが低コストかつ十分な精度を提供する可能性がある。

## アイデア

- Wikiがクエリトークンを多消費するという逆説：Wikiを事前構築することでクエリコストが下がると期待されたが、実際はWikiの全文をコンテキストに含めるコストが上回り、RAGより高コストになった
- claim-level citation checkingの導入：通常のgroundednessルーブリックでは見えない「各主張を支持する引用の正確性」を分解評価することで、RAGとWikiの質的な違いが明確化された
- Decomposition-based RAGがWikiとRAGのトレードオフを部分的に解決：低コストで論文横断合成能力を獲得できるが、引用精度という別次元ではWikiに劣る——能力の分離可能性を示す重要な実験結果

## 前提知識

- **Vector RAG** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **preregistration** (TODO: 読むべき)
- **groundedness評価** (TODO: 読むべき)
- **retrieval-augmented generation** (TODO: 読むべき)

## 関連記事

- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた
- /deep_2563 文字通りの要約を超えて：医療SOAPノート評価におけるハルシネーションの再定義
- /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成
- /deep_2877 SemiFA：半導体故障解析レポートを自律生成するエージェント型マルチモーダルフレームワーク
- /deep_93 RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）

## 原文リンク

[Vector RAG vs LLMコンパイルWiki：小規模マルチドメイン研究コーパスでの事前登録比較](https://tldr.takara.ai/p/2605.18490)
