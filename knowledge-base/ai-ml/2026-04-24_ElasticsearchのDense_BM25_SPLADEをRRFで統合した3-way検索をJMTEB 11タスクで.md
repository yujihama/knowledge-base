---
title: "ElasticsearchのDense/BM25/SPLADEをRRFで統合した3-way検索をJMTEB 11タスクで精度検証"
url: "https://zenn.dev/taimo/articles/28a1d0eccbc199"
date: 2026-04-24
tags: [RAG, Elasticsearch, Dense Retrieval, BM25, SPLADE, RRF, JMTEB, ハイブリッド検索, NDCG@10]
category: "ai-ml"
related: [969, 1336, 2421, 2360, 1116]
memo: "[Zenn 機械学習] Elasticsearchの3検索を混ぜて精度検証してみた - Dense, Lexical, Sparse Retrival"
processed_at: "2026-04-24T12:34:49.818851"
---

## 要約

Elasticsearchで利用可能な3つの検索手法（Dense Retrieval・Lexical Retrieval/BM25・Sparse Retrieval/SPLADE）を単独および組み合わせで評価し、RRF（Reciprocal Rank Fusion）による統合効果をJMTEBの11Retrievalタスクで定量検証した記事。

各手法の特性は次の通り。Dense Retrievalはtext-embedding-3-large（OpenAI）による埋め込みのコサイン類似度を使い、言い換えや文脈理解に強い一方、固有名詞・バージョン番号の完全一致が弱い。Lexical Retrieval（BM25）はkuromojiによる形態素解析＋TF-IDF重み付けで固有名詞・エラーコード検索に強いが、語彙不一致には対応できない。Sparse Retrieval（SPLADE：hotchpotch/japanese-splade-v2）はMLMによるスパースベクトル拡張で「猫→cat・ネコ・子猫」のような自動言い換えを行い、BM25とDenseの中間的特性を持つ。

RRFは各手法の順位の逆数を合算してスコアを算出（k=60、ESデフォルト）。3-way検索（D+L+S）はRRFによる統合スコアで全7モード中1位（RRFスコア0.1736）を獲得し、最悪順位が4位と大崩れしないのが特徴。対してSparse Retrieval onlyは1位3回・最下位3回、Lexical onlyも1位2回・最下位4回と振れ幅が大きい。

ただし単一手法が圧倒的に強いタスクでは3-wayが劣る。Mintaka（エンティティQA）ではDense only（NDCG@10=0.393）に対し3-wayは0.232と大幅に下回り、MultiLongDoc（長文検索）ではLexical only（0.599）に対し3-wayは0.495にとどまる。これはRRFが弱い手法のノイズを混入させ、強い手法のスコアを希釈するためと解釈される。

結論として「クエリ傾向が事前に読めない汎用RAGやエージェントのメモリー検索には3-wayが適し、ドメイン固定で最適手法が既知なら単一手法の方が高精度」という実務的指針が得られた。監査エージェントのメモリー検索は多様なクエリを受けるため、3-way構成の採用根拠が実験により裏付けられた形となる。コスト面ではDense埋め込み生成やSPLADEモデル推論のレイテンシ・リソースとのトレードオフも考慮が必要。

## アイデア

- RRFは「下振れ防止」と「上振れ抑制」という表裏一体の特性を持ち、汎用性と特化性のトレードオフを定量的に示した点が実務設計に直結する
- エージェントのメモリー検索のようにクエリ分布が事前に読めないユースケースでは、最高精度より最悪精度の担保が重要という設計思想の実証
- Mintaka（NDCG: Dense=0.393 vs 3-way=0.232）とMultiLongDoc（Lexical=0.599 vs 3-way=0.495）という反例が明示されており、3-way採用の判断基準として「クエリのドメイン固定度」を軸にする実践的フレームワークが得られる

## 前提知識

- **BM25/TF-IDF** (TODO: 読むべき)
- **SPLADE** (TODO: 読むべき)
- **RRF** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **NDCG@10** → /deep_2421 Sentence Transformersによるマルチモーダル埋め込み・リランカーモデルのトレーニングとファインチューニング
- **埋め込みベクトル検索** (TODO: 読むべき)

## 関連記事

- /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- /deep_1336 Claude Codeの長期記憶を「記憶の宮殿」アーキテクチャで実装したCLIツール「Codeatrium」
- /deep_2421 Sentence Transformersによるマルチモーダル埋め込み・リランカーモデルのトレーニングとファインチューニング
- /deep_2360 NLP2026 参加報告：言語処理学会第32回年次大会レポート
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング

## 原文リンク

[ElasticsearchのDense/BM25/SPLADEをRRFで統合した3-way検索をJMTEB 11タスクで精度検証](https://zenn.dev/taimo/articles/28a1d0eccbc199)
