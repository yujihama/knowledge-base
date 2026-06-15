---
title: "AttentionとTransformerの仕組み：RNNのボトルネックからRoPEまで"
url: "https://zenn.dev/zak2718/articles/attention-and-transformers"
date: 2026-06-15
tags: [Attention, Transformer, Multi-head Attention, Self-attention, RoPE, Positional Encoding, Layer Normalization, Residual Connection]
category: "ai-ml"
related: [6207, 4483, 201, 585, 2654]
memo: "[Zenn LLM] Attention"
processed_at: "2026-06-15T09:07:25.507764"
---

## 要約

本記事はAttentionメカニズムの誕生背景からTransformerアーキテクチャ、さらにRotary Positional Embedding（RoPE）まで、数式を交えて体系的に解説している。

AttentionはRNNのencoder-decoderが抱えるボトルネック問題を解消するために考案された。従来手法では入力文全体を単一の固定長ベクトルに圧縮するため、文が長くなると情報が欠落し翻訳品質が低下する。Attentionはデコーダが入力系列を直接参照できる「ソフトな辞書引き」の仕組みを導入した。Query（何を探すか）、Key（何を提供するか）、Value（実際の内容）の3役に分け、QueryとKeyのスコアをsoftmaxで正規化したAttention Weightを用いてValueの加重平均を計算する。数式では Attention(Q,K,V) = softmax(QK^T / √d_k) V と表現され、√d_kによるスケーリングは次元数増大に伴うsoftmaxの飽和を防ぐ。

Multi-head Attentionは複数のAttentionを並列実行することで、各ヘッドが異なる種類の依存関係（構文・意味など）を専門的に学習できる構造。各ヘッドは独自の重み行列W^Q, W^K, W^Vで入力Xを投影し、得られた結果をConcatしてW^Oで元の次元に変換する。

Self-attentionは同一系列内の全トークン間でAttentionを計算する特殊ケースで、「it」のような代名詞が「animal」を参照するような長距離依存を1ステップで解決できる。RNNでは再帰的な多段更新が必要だった処理を単一操作に圧縮できる点が最大の利点。

TransformerはSelf-attentionを核としたアーキテクチャで、入力トークン数と出力ベクトル数は変わらず内容のみが変化する。各ブロックはMulti-head Self-attentionとトークン単位のFeed-Forward Network（FFN）の2段構成で、それぞれにResidual ConnectionとLayer Normalizationを適用する（Z = LayerNorm(X + MultiHead(X))、Y = LayerNorm(Z + FFN(Z))）。Residual Connectionは勾配を直接流すことで深いスタックの学習を安定させる。

Self-attentionは順列等価性（permutation-equivariant）を持つため、トークンの順序情報が自動的には保持されない。元論文（Vaswani et al., 2017）では正弦波位置エンコーディングを加算することで絶対位置を付与する。各次元に異なる周波数のsin/cosを割り当て、位置シフトが各sin-cosペアの固定回転として表現できるため相対オフセットも線形関数で表現可能。

RoPE（Rotary Positional Embedding, Su et al., 2021）は現代の大規模モデルで標準となっている手法で、位置ベクトルの加算ではなくQueryとKeyを位置に比例した角度で回転させる。これによりドット積スコアが絶対位置m・nではなく相対オフセット(m-n)のみに依存するため、学習時と異なる位置でも同じパターンを適用でき、学習長を超える系列への汎化性能が向上する。監査エージェント開発においては、長い監査ドキュメントや複数文書間の参照関係をAttentionで直接モデル化できる可能性があり、RoPEによる長文対応は実務上の長い契約書や財務報告書処理にも直結する。

## アイデア

- RoPEが絶対位置でなく相対オフセット(m-n)のみに依存するよう設計されている点：これにより学習長を超える系列への外挿が可能になり、長文処理の実用性が大幅に向上する
- Self-attentionの順列等変性（permutation-equivariance）という盲点：加重和∑α_i v_iはトークン順序に依存しないため、意味のある語順情報は別途（位置エンコーディングで）注入しなければならないという構造的制約
- Attentionを「ソフトな辞書引き」として定式化することで解釈可能性が生まれる：α_iの大きさがどのトークンがどれほど参照されたかを直接示し、翻訳例の重み行列のような形で可視化・デバッグが可能

## 前提知識

- **RNN encoder-decoder** → /deep_5902 論文メモ：Bahdanau AttentionからAttentionを理解する
- **softmax関数** (TODO: 読むべき)
- **行列積・転置** (TODO: 読むべき)
- **Feed-Forward Network** (TODO: 読むべき)
- **勾配消失問題** (TODO: 読むべき)

## 関連記事

- /deep_6207 LLM解説シリーズ：Transformerの基本構造をAttention論文から読む
- /deep_4483 Transformerの数式を完全整理：埋め込みからAttentionまで一気に俯瞰
- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_585 nanoVLMでゼロから実装するKVキャッシュ
- /deep_2654 Multi-Head Attentionはなぜ効くのか？（現代編）— 論文から理解の変遷を整理する

## 原文リンク

[AttentionとTransformerの仕組み：RNNのボトルネックからRoPEまで](https://zenn.dev/zak2718/articles/attention-and-transformers)
