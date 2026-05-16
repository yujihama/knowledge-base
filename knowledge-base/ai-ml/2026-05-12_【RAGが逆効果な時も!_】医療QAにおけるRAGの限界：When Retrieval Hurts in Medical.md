---
title: "【RAGが逆効果な時も!?】医療QAにおけるRAGの限界：When Retrieval Hurts in Medical Question Answering"
url: "https://zenn.dev/eques/articles/e7e3fc8cfd471d"
date: 2026-05-12
tags: [RAG, 医療QA, BM25, Dense Retrieval, RRF, USMLE-MedQA, MedRAG, multi-hop reasoning, retrieval evaluation]
category: "ai-ml"
related: [2831, 4335, 969, 4480, 4632]
memo: "[Zenn LLM] 【RAGが逆効果な時も!?】 When Retrieval Hurts in Medical Question Answering"
processed_at: "2026-05-12T21:04:06.176936"
---

## 要約

AISNS2025にて発表された論文「When Retrieval Hurts: A Critical Analysis of RAG in Medical Question Answering」を紹介した記事。医療QAタスクにおいて、標準的なRAG手法がLLM単体（No-RAG）より精度を下げるケースがあることを実証した研究。

実験設定はシンプルで、Retrieval手法として①BM25（語彙頻度ベースのlexical search）、②Dense（MiniLM-L6-v2による384次元ベクトル＋FAISSのinner product、cosine similarityによるsemantic search）、③Hybrid（BM25とDenseをReciprocal Rank Fusion＝RRFで統合）の3種類を採用。知識ベースはMedRAGフレームワークに従い18ソースから収集した125,847件の医療教科書文書。評価タスクはUSMLE-MedQA（米国医師国家試験ベースの4択問題）で、指標はAccuracy（正答率）。

結果として、8BサイズLLMのMedQA正答率は約60%で、BM25・Dense・Hybrid RAGいずれを適用しても精度が改善せず、むしろPure LLM（No-RAG）が最高精度となった。さらにRAGのretrievalスコアと正答率の相関も分析したが、スコアの高低が回答品質の信頼度を示す傾向は確認されなかった。Qwen-Plusなどの非オープンモデルでも同様の結果が得られており、モデルサイズに依存しない現象とされる。

原因として、医師国家試験のような問題では質問文や選択肢と語彙的・意味的に類似する文章が必ずしも正答に直結しないことが挙げられる。単純なchunk検索では必要な複数ステップの推論（multi-hop reasoning）を支援できない。これを受けてAgentic RAG、GraphRAG、RAG Fusion、Self-RAG、MedXpert（ICML2025）、Med Co-Reasoner（ACL2026）、ShatterMed-QAといったreasoning重視の発展手法が紹介されている。

監査エージェント開発への示唆：監査判断も医療QAと同様に、単純なキーワード・意味類似検索では不十分な複雑な推論が要求される。RAGを導入する前に「そのタスクがretrieval恩恵を受けやすいか」を検証し、Agentic RAGやGraphRAGなどmulti-hop対応の設計を検討すべき。

## アイデア

- RAGのretrievalスコアが回答品質の信頼度指標にならないという発見は、RAGベースシステムの不確実性定量化（uncertainty quantification）設計に根本的な問いを投げかける
- RRFがスコアの絶対値を捨象しrankのみを使う設計は、異種retrieverの統合には有効だが医療推論のような文脈では情報欠落リスクになり得るというトレードオフの具体例
- モデルの能力向上（8B〜Qwen-Plus）によりLLM内部知識が充実した結果、外部知識注入がノイズ化するという「RAGの効用逓減」現象は、ファインチューニングとRAGの使い分け戦略を再考させる

## 前提知識

- **BM25** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **Dense Retrieval** → /deep_2831 ElasticsearchのDense/BM25/SPLADEをRRFで統合した3-way検索をJMTEB 11タスクで精度検証
- **RRF（Reciprocal Rank Fusion）** (TODO: 読むべき)
- **FAISS** → /deep_4918 FGDM: Chain-of-ThoughtとTree-of-Thoughtプロンプティングを用いたソフトウェアバグ検出のための推論対応マルチエージェントフレームワーク
- **USMLE-MedQA** (TODO: 読むべき)

## 関連記事

- /deep_2831 ElasticsearchのDense/BM25/SPLADEをRRFで統合した3-way検索をJMTEB 11タスクで精度検証
- /deep_4335 RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法
- /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- /deep_4480 AI記憶基盤を自作してしまった話：既存ツール選定の敗戦記とSQLiteベースのhybrid検索設計
- /deep_4632 エンタープライズAI向けマルチモーダル文書処理パイプラインの統合評価フレームワーク：EnterpriseDocBench

## 原文リンク

[【RAGが逆効果な時も!?】医療QAにおけるRAGの限界：When Retrieval Hurts in Medical Question Answering](https://zenn.dev/eques/articles/e7e3fc8cfd471d)
