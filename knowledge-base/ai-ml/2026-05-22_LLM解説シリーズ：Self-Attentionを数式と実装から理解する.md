---
title: "LLM解説シリーズ：Self-Attentionを数式と実装から理解する"
url: "https://zenn.dev/kas_blog/articles/20260509-llm-06-self-attention"
date: 2026-05-22
tags: [Self-Attention, Transformer, Multi-Head Attention, Scaled Dot-Product Attention, causal mask, KV Cache, PyTorch, LLM基礎]
category: "ai-ml"
related: [5761, 201, 585, 2654, 2381]
memo: "[Zenn LLM] LLM解説シリーズ：Self-Attentionを数式と実装から理解する"
processed_at: "2026-05-22T09:06:17.463086"
---

## 要約

本記事は、2017年のTransformer原論文「Attention Is All You Need」（Vaswaniら）を起点に、Self-AttentionおよびMulti-Head AttentionをPyTorchで実装しながら解説する技術メモである。

Self-Attentionの本質は、同一系列内の任意のtokenペアを1層の中で直接比較できる点にある。RNNでは遠いtokenへの情報伝達に複数ステップを要するが、Self-Attentionではスコア行列 QK^T を一括計算することで長距離依存を直接捉えられる。

計算の核心はScaled Dot-Product Attention： softmax(QK^T / √d_k) V である。d_kで割るスケーリングは、次元数増加による内積値の肥大化を防ぐための措置。実装上重要なのは、maskをsoftmax前に適用することである。softmax後にゼロ乗算すると重みの和が1でなくなり正規化が崩れるため、softmax前に不可視位置のスコアをfloat最小値（torch.finfo().min）で上書きし、見える位置だけで再正規化を成立させる。

tensor形状は (B, H, T, D) で管理する。scoresは (B, H, T, T) となるため、系列長Tが伸びると計算量・メモリがO(n^2)で増加する。これが長文LLMの根本的なボトルネックである。

GPT系の自己回帰モデルではcausal maskが必要で、未来tokenへの参照を遮断する。build_causal_mask関数ではtorch.arangeで位置インデックスを生成し、現在位置以前のみTrueとなる下三角マスクを構築する。

Multi-Head Attentionは、headごとに別の投影行列 W_i^Q, W_i^K, W_i^V を持つことで、同一token列に対し複数の表現空間で関係を並列に捉える仕組みである。単純なAttentionの繰り返しではなく、投影によって異なる特徴（近傍参照・主語述語関係・指示語解決など）をheadに分担させる効果が期待される。

よくある誤解として、「maskはsoftmax後でよい」「KV CacheでO(n^2)が消える」などが挙げられる。KV Cacheは自己回帰推論時にKey/Valueを再利用して逐次的な再計算を省くものであり、学習時の二乗計算量を根本解決するものではない。

監査エージェント開発への示唆：LLMを用いた文書参照・監査証跡のクロスレファレンス処理において、Self-Attentionのtoken間スコア構造（scores行列）はどのtokenがどの文脈を参照しているかの解釈に活用できる。ただし、attention weightは因果的説明として過信せず、参照傾向の可視化として慎重に扱う必要がある。

## アイデア

- maskをsoftmax前に適用する理由が数学的に明確：softmax後のゼロ乗算では正規化の和が1を割るため、不可視位置を-∞相当の値で潰してから確率変換する設計が必須
- scoresテンソルが (B, H, T, T) であることを体感すると、FlashAttentionやGQA/MQAのような後続最適化技術の動機（O(n^2)メモリ削減）が直感的に理解できる
- Multi-Headの本質は単純な繰り返しではなく、投影行列の独立性により各headが異なる特徴空間で関係を学習できる点にあり、1つのheadでは表現しきれない多様な依存関係を並列に捉えられる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **行列積・内積** (TODO: 読むべき)
- **softmax** → /deep_3691 GSQ：Gumbel-Softmaxサンプリングによる高精度低ビット幅スカラー量子化
- **PyTorch Tensor操作** (TODO: 読むべき)
- **自己回帰モデル** → /deep_19 LLMのコード生成はなぜ同じミスを繰り返すのか — 失敗を「演算子」にして生成過程を書き換える

## 関連記事

- /deep_5761 論文メモ：BERTからEmbeddingを整理する
- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_585 nanoVLMでゼロから実装するKVキャッシュ
- /deep_2654 Multi-Head Attentionはなぜ効くのか？（現代編）— 論文から理解の変遷を整理する
- /deep_2381 Multi-Head Attentionはなぜ効くのか？ — 論文から辿る理解の変遷

## 原文リンク

[LLM解説シリーズ：Self-Attentionを数式と実装から理解する](https://zenn.dev/kas_blog/articles/20260509-llm-06-self-attention)
