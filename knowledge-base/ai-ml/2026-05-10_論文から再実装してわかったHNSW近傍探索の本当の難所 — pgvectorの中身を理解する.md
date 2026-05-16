---
title: "論文から再実装してわかったHNSW近傍探索の本当の難所 — pgvectorの中身を理解する"
url: "https://zenn.dev/jobmore/articles/hnsw-pgvector-deep-dive"
date: 2026-05-10
tags: [HNSW, pgvector, ANN, ベクトル検索, Rust, 近傍探索, Skip List, Small World]
category: "ai-ml"
related: [2839, 3415, 93, 3865, 1936]
memo: "[Zenn 機械学習] 論文から再実装してわかったHNSW近傍探索の本当の難所 — pgvectorの中身を理解する"
processed_at: "2026-05-10T09:35:27.250482"
---

## 要約

本記事は、Malkov & Yashunin (2018) のHNSW（Hierarchical Navigable Small World）論文を読み込み、Rustで実装しながらアルゴリズムを解説した技術記録。pgvectorのHNSWインデックスを「雰囲気で触っている状態」から脱するため、内部構造を体系的に整理している。

HNSWの発想の源流は「Skip List + Small Worldグラフ」の掛け合わせ。Skip Listの多層構造とWatts-Strogatz的な小世界ネットワークの貪欲探索を組み合わせ、上層では疎なノード・長距離エッジで広域ジャンプ、下層では密なノード・短距離エッジで精密探索を行う。ノードのレベルはl = ⌊-ln(uniform(0,1)) × mL⌋（mL = 1/ln M）の指数分布でサンプリングし、上層ほどノード数が1/Mに減る設計で平均探索コストO(log N)を保証する。

アルゴリズム実装の核心は3点。①挿入時、対象層より上ではef=1の貪欲探索、対象層ではef_constructionの幅広探索で品質を確保する。②SEARCH-LAYERではmin-heap（探索候補）とmax-heap（結果管理）の2ヒープ構造を使ったベスト・ファースト探索＋動的枝刈りを行う。③SELECT-NEIGHBORSはSimple（距離順M個）とHeuristic（多様性確保のためクラスタ橋渡しエッジを優先）の2方式があり、業界ごとにクラスタが分かれる求人ベクトルのような「クラスタ間密度ギャップが大きいデータ」ではHeuristicが有効。

実用上のハイパーパラメータはM（エッジ上限、典型値16〜48、構築後変更不可）、ef_construction（構築時探索幅、100〜400）、ef_search（クエリ時探索幅、50〜400、pgvectorでは`SET hnsw.ef_search = 200;`でセッション単位変更可能）の3つ。Recallはef_searchに対して対数的に飽和し、recall 0.95→0.99を狙うコストは大きい。

Rust実装では隣接配列を連続メモリに配置してキャッシュ効率を確保し、距離メトリックをトレイトで抽象化することでSIMD化実装への差し替えを可能にしている。pgvector・Qdrant・Weaviate・Milvus等の主要ベクトルDBはほぼ全てHNSWを採用しており、本記事はそのアルゴリズム基盤を深く理解するための実践的な資料となっている。監査エージェントにおけるセマンティック検索基盤（監査証跡や規程文書の類似検索）の精度チューニングにも直接応用できる知見を含む。

## アイデア

- SELECT-NEIGHBORSのHeuristic方式がクラスタ間の「橋渡しエッジ」を意図的に維持する設計で、密集クラスタを持つドメイン特化ベクトル（求人・法令文書等）でSimpleより精度が大きく向上する点
- mL = 1/ln(M)が理論最適値として論文で導出されており、Mを変更した際にmLも連動して変わることを忘れると実装バグになるという、論文読解と実装の両方が必要な落とし穴
- 2ヒープ構造（min-heap for candidates + max-heap for results）によるベスト・ファースト探索がHNSWの探索品質を保証する核心実装であり、このデータ構造選択がrecall-QPS トレードオフを直接制御している点

## 前提知識

- **ANN（近似最近傍探索）** (TODO: 読むべき)
- **Skip List** (TODO: 読むべき)
- **コサイン類似度** → /deep_371 選択的勾配射影による継続学習での忘却軽減
- **グラフ探索アルゴリズム** (TODO: 読むべき)
- **pgvector** → /deep_93 RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）

## 関連記事

- /deep_2839 Mycelium-Index：菌糸体の成長パターンに着想を得たストリーミング近似最近傍インデックス
- /deep_3415 ベクトル検索のためのSemantic Recall：近似最近傍探索の品質評価指標
- /deep_93 RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）
- /deep_3865 Onyx: コスト効率の高いディスク透過型近似最近傍探索
- /deep_1936 🤗 APIユーザー向けTransformer推論を100倍高速化した方法

## 原文リンク

[論文から再実装してわかったHNSW近傍探索の本当の難所 — pgvectorの中身を理解する](https://zenn.dev/jobmore/articles/hnsw-pgvector-deep-dive)
