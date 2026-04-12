---
title: "【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜"
url: "https://zenn.dev/hitama/articles/fcbe6662c63a76"
date: 2026-04-02
tags: [Transformer, Self-Attention, Multi-Head Attention, Seq2Seq, RNN, 自然言語処理, 埋め込みベクトル]
category: "ai-ml"
memo: "[Zenn 機械学習] 【Transformerとは？ - 第七回A】Self-Attentionの正体 ~Self-Attentionは何を変えたのか~"
processed_at: "2026-04-02T09:01:27.156275"
---

## 要約

本記事はZenn上の連載「機械学習素人がTransformerを理解するまでの記録」第七回。RNNベースのSeq2SeqおよびAttentionの限界を整理した上で、TransformerのコアメカニズムであるSelf-Attentionを概念・数式・具体例の三層で解説している。

RNN型Seq2Seqは入力系列を単一ベクトルに圧縮するため長文で情報が欠落する問題があり、Attentionはその改善として「必要な情報をその都度参照する」仕組みを導入した。しかしAttentionは既に意味が確定したEncoder出力から選ぶだけ（参照）であり、逐次処理・並列化不可・長距離依存の不完全さという根本的制約はRNNから引き継がれていた。

TransformerはRNNを完全に排除し、Attentionのみで系列を扱う設計。EncoderはTransformerブロックを一度通すだけで処理が完了し、DecoderもRNNのように前の隠れ状態を引き継がず、「これまでのトークンすべてを毎回参照して再計算する」方式をとる。

通常のAttentionとSelf-Attentionの本質的な違いは「クエリの出所」にある。Attentionのクエリはデコーダ側の状態s_iという外部から来るのに対し、Self-AttentionのクエリはEncoder内部のh_i自身。α_ij = softmax(h_i^T h_j)により、入力同士が相互に関連度を計算し、各単語の表現h_iをh_i'（他の全単語を加重平均した新ベクトル）に更新する。「銀行」が「川の近く」か「お金の話」かで意味が変わる例が示すように、意味は入力単体ではなく文脈との相互作用で「生成」される。

進化の差分を機能ベースで整理すると、①Seq2Seq→②Attention（重み付き参照）→③Self-Attention（入力内の関係性）→④QKV型（役割分離）→⑤Multi-Head（視点の並列化）という5段階。本記事はSelf-Attention（③）までをカバーし、次回はQKV型とMulti-Headを扱う予定。

## アイデア

- Attentionは『既成の情報を選ぶ（参照）』であり、Self-Attentionは『情報そのものを再構築する（生成）』という役割の非対称性は、RAGにおける検索フェーズ（参照）と読解フェーズ（文脈統合）の設計を直感的に理解する枠組みとして応用できる
- 進化を5段階（Seq2Seq→Attention→Self-Attention→QKV→Multi-Head）の差分表で整理したアプローチは、新技術の能力評価フレームワーク構築の方法論として参考になる
- Transformerが状態を持たず『毎回全トークンを参照して再計算する』設計は、エージェントが会話履歴を毎ターン全量コンテキストに含めるアーキテクチャと本質的に同型であり、メモリ管理コストとのトレードオフを考える出発点となる
## 関連記事

- /deep_585 nanoVLMでゼロから実装するKVキャッシュ
- /deep_879 Mamba解説：TransformerへのState Space Modelによる挑戦
- /deep_262 Mambaとは何か：TransformerへのState Space Modelによる挑戦
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜](https://zenn.dev/hitama/articles/fcbe6662c63a76)
