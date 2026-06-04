---
title: "Per-Layer Embeddingsの仕組み：Gemma 4のEシリーズモデルにおける埋め込みパラメータの扱い"
url: "https://zenn.dev/sudy_super/articles/8651027e38b3ae"
date: 2026-06-04
tags: [Gemma4, Per-Layer Embeddings, embedding, lookup table, パラメータ効率, LLMアーキテクチャ, VRAM最適化]
category: "ai-ml"
related: [3548, 2056, 161, 5761, 7286]
memo: "[Zenn LLM] Per-Layer Embeddingsの中身"
processed_at: "2026-06-04T21:21:54.423943"
---

## 要約

GoogleのGemma 4シリーズには、gemma-4-E2BとgemmaE4Bという2つの小型モデルが存在する。名称の「E」はEffective（有効）パラメータを意味する。gemma-4-E2Bは全体で51億パラメータを持つが、そのうち28億は埋め込みパラメータ（embedding parameters）であり、Googleはこれを「有効パラメータ」にカウントしない。その結果、有効パラメータは23億となりE2Bと呼称される。同様に、gemma-4-E4Bは全体80億パラメータのうち埋め込みが35億を占め、有効パラメータは45億でE4Bとなる。

埋め込みパラメータをカウントしない根拠は、埋め込み行列の性質にある。埋め込み行列は各行が独立した分散表現であり、行間に相互関係はなく、実質的にlookup table（ベクトルを並べたもの）として機能する。推論時は行列積を計算する必要はなく、token idに対応するベクトルを取り出すだけでよい。Gemma 4のtokenizerは語彙数約26万を持つが、実際に使用するのは入力シーケンス長分のベクトルのみであるため、全ての埋め込みをVRAMやDRAMに常駐させる必要がなく、高速なディスクに格納しておけば十分とされる。

Per-Layer Embeddings（PLE）の設計思想は、モデルの次元数や層数を単純に増やして性能向上を図るのではなく、各decoder layerに小さな独立したembedding layerを設けることで、各decoder layerが「埋め込みから得た情報の保持」以外の処理にキャパシティを集中できるようにするというものである。これにより、パラメータ効率を維持しつつ各層の表現能力を高める設計となっている。

監査エージェント開発への示唆としては直接的な関連性は薄いが、推論時のメモリ効率化という観点は、ローカルLLMインフラ構築（RTX 3090環境など）においてVRAM消費を抑えながら大型モデルを運用する際の設計指針として参考になる。PLEにより埋め込みをディスクに退避できるという特性は、リソース制約環境でのモデル展開戦略に影響を与える可能性がある。

## アイデア

- 埋め込み行列はlookup tableであるため行列積が不要という事実を利用し、全語彙分の埋め込みをVRAMではなく高速ディスクに格納できる——これはVRAM制約の厳しいローカル環境でのLLM運用に直結する設計上のポイント
- Per-Layer Embeddingsにより各decoder layerが独立したembedding情報を受け取ることで、「情報保持」以外にlayer capacityを割けるという設計は、深いTransformerにおける情報圧縮・伝搬の問題への構造的アプローチ
- 「有効パラメータ数」という概念の導入：物理的なパラメータ数とメモリ・計算上の実コストを分離して表記することで、モデルサイズの比較基準が変わりうるという命名・ベンチマーク上の示唆

## 前提知識

- **Transformer decoder** → /deep_369 視覚的In-Contextデモンストレーション選択の学習
- **Embedding matrix** (TODO: 読むべき)
- **Tokenizer / vocabulary** (TODO: 読むべき)
- **VRAM / メモリ階層** (TODO: 読むべき)
- **Gemma 3n** (TODO: 読むべき)

## 関連記事

- /deep_3548 Hyperloop Transformer：パラメータ効率を約50%改善するループ型Transformerアーキテクチャ
- /deep_2056 Gemma 4 思考モード検証：26B vs E4B — ローカルLLMでのオイラー数問題を題材にした精度・速度比較
- /deep_161 鳥の音声で訓練されたAIが水中の謎を解明：Perch 2.0の転移学習
- /deep_5761 論文メモ：BERTからEmbeddingを整理する
- /deep_7286 誰も教えてくれないベクトル検索RAGの真実

## 原文リンク

[Per-Layer Embeddingsの仕組み：Gemma 4のEシリーズモデルにおける埋め込みパラメータの扱い](https://zenn.dev/sudy_super/articles/8651027e38b3ae)
