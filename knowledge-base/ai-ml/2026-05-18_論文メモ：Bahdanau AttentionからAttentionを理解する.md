---
title: "論文メモ：Bahdanau AttentionからAttentionを理解する"
url: "https://zenn.dev/kas_blog/articles/20260509-llm-04-attention"
date: 2026-05-18
tags: [Bahdanau Attention, soft alignment, RNN Encoder-Decoder, context vector, 機械翻訳, alignment weight, bidirectional RNN]
category: "ai-ml"
related: [158, 4664, 4527, 706, 1938]
memo: "[Zenn LLM] 論文メモ：Bahdanau AttentionからAttentionを理解する"
processed_at: "2026-05-18T09:02:37.076398"
---

## 要約

本記事は、2014年にBahdanau・Cho・Bengioが発表した論文「Neural Machine Translation by Jointly Learning to Align and Translate」の技術メモである。当時のRNN Encoder-Decoderモデルは、入力文全体を1つの固定長ベクトルに圧縮してDecoder側へ渡す構造を取っており、長文ほど情報圧縮が厳しくなるボトルネックが存在した。Bahdanau Attentionはこの問題を「soft alignment」で緩和する。具体的には、Decoderが各出力位置iに対して固定のcontext vectorを使い回すのではなく、入力側の各位置jのannotation h_jを重み付き和で合成した個別のcontext vector c_iを生成する。重みα_ijはfeedforward neural networkで計算されたalignment score e_ijをsoftmaxで正規化したものであり、翻訳モデル全体と同時にend-to-endで学習される。Encoderにはbidirectional RNNを採用し、各位置のannotationは前向きRNNと後ろ向きRNNの隠れ状態を結合することで前後文脈を含む表現となっている。WMT 2014英仏翻訳タスクの実験では、Attentionなしの RNNencdec-50がBLEU 17.82だったのに対し、RNNsearch-50は26.75を達成し、長時間学習版では28.45まで向上した。TransformerのSelf-Attentionとの主な違いは、BahdanauはDecoder状態がEncoder出力を参照するクロスアテンション構造であるのに対し、Self-Attentionは同一系列内のトークン同士が相互参照する点、またスコア計算がfeedforward networkか内積かという点にある。実装上の注意点として、batch処理時のpadding maskの必要性、attention weightが因果的説明として過信できないこと、Additive AttentionとScaled Dot-Product Attentionの計算コスト・並列性の違いが挙げられている。監査エージェント開発への直接的な示唆は薄いが、LLMのKV CacheやMulti-Head Attentionを理解するための概念的な土台として、context vectorとalignment weightの関係を把握しておくことが有益である。

## アイデア

- soft alignmentにより勾配がattention weightを通じて流れるため、翻訳とalignmentを同時にend-to-endで学習できる点が、hard alignmentや潜在変数アプローチとの決定的な違い
- attention weightは可視化ツールとして有用だが、それが因果的説明になるとは限らないという指摘は、LLM解釈可能性研究（Mechanistic Interpretability）への批判的視点として現代でも有効
- 固定長ボトルネックの解消という発想が、TransformerのKV Cacheや無限コンテキスト研究まで続く「どこを参照するか」という問いの起点になっている

## 前提知識

- **RNN Encoder-Decoder** (TODO: 読むべき)
- **BLEU** → /deep_271 テキスト埋め込みはテキストを完全にエンコードしているか？―vec2textによる埋め込みの逆変換
- **softmax** → /deep_3691 GSQ：Gumbel-Softmaxサンプリングによる高精度低ビット幅スカラー量子化
- **bidirectional RNN** (TODO: 読むべき)
- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは

## 関連記事

- /deep_158 翻訳か暗唱か？極低リソース言語の機械翻訳評価スコアの較正
- /deep_4664 大規模言語モデルにおける文化配慮型機械翻訳：ベンチマークと調査
- /deep_4527 多言語社会における言語イデオロギー：LLMによるルクセンブルク語ニュースコメントの分析
- /deep_706 バイリンガルBabyLMの育成：小規模モデルを用いた多言語言語習得の研究
- /deep_1938 fairseq WMT19翻訳システムをTransformersへ移植する

## 原文リンク

[論文メモ：Bahdanau AttentionからAttentionを理解する](https://zenn.dev/kas_blog/articles/20260509-llm-04-attention)
