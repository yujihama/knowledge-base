---
title: "RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法"
url: "https://zenn.dev/libercraft/articles/20260430-rag-precision-golden-set"
date: 2026-05-08
tags: [RAG, RAGAS, Golden Set, LLM-as-a-Judge, チャンキング, ハイブリッド検索, BM25, RRF, Weights & Biases, Context Recall, Faithfulness, LangChain]
category: "agent-arch"
related: [969, 2831, 1336, 2446, 2794]
memo: "[Zenn LLM] RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法"
processed_at: "2026-05-08T09:43:59.348926"
---

## 要約

RAGシステムの精度問題は「検索（Retrieval）の問題」と「評価の不在」に大別され、生成側（プロンプト）ではなく検索品質が問題の約8割を占めるという実務知見に基づく記事。原因は3つに整理される。①チャンキング設計の粗さ：固定長分割でセクション境界を無視すると、チャンクが大きすぎて無関係情報が混入したり、小さすぎて文脈が途切れる。LangChainのRecursiveCharacterTextSplitterでchunk_size=512・chunk_overlap=64・日本語対応区切り文字を設定し、セマンティックな境界を尊重することが推奨される。SemanticChunker・MarkdownHeaderTextSplitter等の用途別手法も紹介。②ベクトル検索のみへの依存：固有名詞・製品コード・型番など文字列完全一致が重要なクエリにはベクトル検索が弱い。BM25とベクトル検索を組み合わせたハイブリッド検索をRRF（Reciprocal Rank Fusion）でスコアマージし、さらにCross-Encoderによるリランキングで「取得件数は多め・LLMへの入力は絞る」設計が有効。③評価の不在：手動で10〜20問を目視確認するだけでは改善施策の効果検証も回帰検知もできない。定量評価にはFaithfulness（幻覚検知）・Answer Relevancy（質問への適合度）・Context Recall（正しい文書の取得率）の3指標を用いる。これらを計測するための「正解」データセットがGolden Set（50〜100問）であり、実際のユーザークエリ・LLMによる自動生成（RAGASのTestsetGenerator）・ドメインエキスパートの手動設計を組み合わせて構築する。自動生成にはシングルホップ50%・マルチホップ抽象25%・マルチホップ具体25%の分布が推奨されるが、必ずエキスパートによるレビューが必要。評価実行にはRAGAS v0.4系（2026年1月時点でv0.4.3）を使用し、v0.3からAPIが大幅変更（ground_truth→reference等）されている点に注意。改善サイクルはWeights & Biases（W&B）でchunk_size・chunk_overlap・top_k・プロンプトバージョン等のパラメータとRAGASスコアを記録し、実験を定量的に追跡する。監査エージェント開発への示唆：契約書・規程文書へのRAG適用時、条文境界を考慮したセクション単位チャンキングとGolden Setによる定量評価サイクルの導入が、PoCから本番への移行品質を左右する。

## アイデア

- 検索品質が問題の8割を占めるという実務知見：プロンプトチューニングより先にRetrieval品質を計測すべきという優先順位の逆転が、RAG改善の最大のポイント
- Golden Set構築への投資対効果：50問の作成に3〜5日かけても、以降の評価コストが大幅削減されるという定量的な主張と、TestsetGeneratorによる半自動化の組み合わせ
- Faithfulness・Answer Relevancy・Context Recallの3指標から問題箇所を逆引きするデバッグ手法：どの指標が低いかで「幻覚」「プロンプト」「チャンキング」のどれに問題があるか切り分けられる設計

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **BM25** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **LLM-as-a-Judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **RAGAS** → /deep_2446 AI for Science の歩き方 #9 ― 実践の心得 ― 効率・データ・検証
- **Cross-Encoder** → /deep_707 Sentence Transformers v4によるリランカーモデルのトレーニングとファインチューニング

## 関連記事

- /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- /deep_2831 ElasticsearchのDense/BM25/SPLADEをRRFで統合した3-way検索をJMTEB 11タスクで精度検証
- /deep_1336 Claude Codeの長期記憶を「記憶の宮殿」アーキテクチャで実装したCLIツール「Codeatrium」
- /deep_2446 AI for Science の歩き方 #9 ― 実践の心得 ― 効率・データ・検証
- /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針

## 原文リンク

[RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法](https://zenn.dev/libercraft/articles/20260430-rag-precision-golden-set)
