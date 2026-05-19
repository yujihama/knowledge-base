---
title: "RAGの精度を改善する：query rewrite・hybrid search・rerank・評価ログ"
url: "https://zenn.dev/wqy/articles/4fe29ac264ea63"
date: 2026-05-19
tags: [RAG, query-rewrite, hybrid-search, BM25, RRF, rerank, FAISS, evidence-gate, evaluation]
category: "ai-ml"
related: [5769, 5500, 5721, 4335, 969]
memo: "[Zenn LLM] RAGの精度を改善する：query rewrite・hybrid search・rerank・評価ログ"
processed_at: "2026-05-19T21:01:03.082043"
---

## 要約

最小構成RAG（FAISS dense search + LLM回答生成）をベースに、検索品質を段階的に改善する手法を実装・比較評価した記事。青空文庫の吉川英治『三国志』全12巻（2602 chunk）を対象に実験。

主な改善要素は5つ。①Query Rewrite：曖昧なクエリをLLMで書き換え、「三人が兄弟になる場面」→「劉備・関羽・張飛が桃園で義兄弟の誓いを立てる場面」のように固有名詞を補完。これにより正解chunkのdenseスコアが0.5419→0.6915に向上。②BM25によるキーワード検索：Dense embeddingが苦手な表記ゆれや固有名詞のマッチングを補完。③Hybrid Search + RRF（Reciprocal Rank Fusion）：DenseとBM25の検索結果をRRFで統合。両手法のランキングを逆数スコアで合算し、どちらかだけでは拾えないchunkを上位に引き上げる。④LLM Rerank：top-k候補を再度LLMに評価させ、質問への関連度でスコアリングし直す。FAISSの近傍距離が高くても質問の答えでないchunkを後退させる役割。⑤Evidence Gate：LLMの一般知識による補完を抑止し、検索結果に根拠がない場合は拒答する制御機構。

評価基準として、query_log.jsonlへのログ記録とeval/questions.yamlを使った自動評価スクリプトを実装。eval_summary.mdとeval_details.jsonで改善効果を比較可能にしている。

実験結果として、baseline_dense（original query + FAISS）ではtop3のうち有効根拠はtop1のみだったが、query rewrite導入でtop3すべてのスコアが向上し関連chunkの密度が改善。Hybrid SearchとRerankの組み合わせでノイズchunkの混入をさらに抑制できることを確認。

監査エージェントへの示唆：契約書・規則文書・監査調書など表記ゆれが多い業務文書に対して、Hybrid Search（Dense+BM25）とQuery Rewriteの組み合わせは特に有効。Evidence Gateは「LLMが知っている情報で補完してしまう」リスクを抑え、根拠のある回答のみを返す拒答制御として内部統制上の信頼性を高める。Evaluation Logの仕組みは、本番RAGシステムの品質モニタリングとして再利用可能な設計。

## アイデア

- Evidence Gate（拒答制御）はLLMの一般知識による「幻覚的補完」を防ぐ機構で、根拠chunkが存在しない場合に明示的に回答拒否させる設計。RAGの信頼性担保として監査文書への応用価値が高い
- RRF（Reciprocal Rank Fusion）はDenseとBM25のスコア体系が異なる問題を、順位の逆数で正規化して統合する手法。スコアの絶対値に依存しないため異種検索エンジンの統合に汎用的
- Query Rewriteをクエリ変換だけでなく「Multi-query Retrieval（複数クエリ生成）」と組み合わせることで、一つの曖昧な質問から複数の検索軸を並列展開し、recall（再現率）を向上させる設計が示されている

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **FAISS** → /deep_4918 FGDM: Chain-of-ThoughtとTree-of-Thoughtプロンプティングを用いたソフトウェアバグ検出のための推論対応マルチエージェントフレームワーク
- **BM25** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **Embedding** → /deep_33 2時間ごとに自分を再構築する — 自律AIエージェントの記憶アーキテクチャ
- **Reranker** → /deep_707 Sentence Transformers v4によるリランカーモデルのトレーニングとファインチューニング

## 関連記事

- /deep_5769 長期LLMペルソナ一貫性のための異種時系列メモリガバナンスフレームワーク（ARPM）
- /deep_5500 【RAGが逆効果な時も!?】医療QAにおけるRAGの限界：When Retrieval Hurts in Medical Question Answering
- /deep_5721 RAGナレッジベース作成を簡単にしたくてツールを作った（mrag）
- /deep_4335 RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法
- /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた

## 原文リンク

[RAGの精度を改善する：query rewrite・hybrid search・rerank・評価ログ](https://zenn.dev/wqy/articles/4fe29ac264ea63)
