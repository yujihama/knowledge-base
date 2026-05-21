---
title: "LLM解説シリーズ：Transformerの基本構造をAttention論文から読む"
url: "https://zenn.dev/kas_blog/articles/20260509-llm-05-transformer"
date: 2026-05-21
tags: [Transformer, Attention, Self-Attention, Multi-Head Attention, Positional Encoding, LLM, 論文解説, 機械翻訳]
category: "ai-ml"
related: [4483, 201, 2654, 2381, 4657]
memo: "[Zenn 機械学習] LLM解説シリーズ：Transformerの基本構造をAttention論文から読む"
processed_at: "2026-05-21T09:11:05.790625"
---

## 要約

本記事は「Attention Is All You Need」（Vaswani et al., 2017）を技術メモ形式で解説したものである。Transformerは、RNNやCNNを排除し、Attentionを系列処理の中心に置いたEncoder-Decoder構造のモデルで、元々は機械翻訳タスク向けに設計された。

主要コンポーネントは、Input Embedding（token IDをベクトル化）、Positional Encoding（sin/cosによる位置情報付与）、Encoder Self-Attention（入力token間の関係計算）、Decoder Masked Self-Attention（未来tokenを参照しない自己回帰処理）、Encoder-Decoder Attention、Feed Forward Network（各位置に独立した2層MLP）の6つ。

Self-Attentionの基本式はScaled Dot-Product Attention：Attention(Q,K,V) = softmax(QK^T / √d_k)V。QueryはQuery対象tokenから「何を参照したいか」、Keyは各tokenの「照合手がかり」、Valueは「混合する中身」を表す。baseモデルはd_model=512、8ヘッドで各ヘッドは64次元で計算する。

RNNとの比較では、RNNが時間方向に順次処理するため並列化が困難で長距離依存に弱いのに対し、Self-Attentionは1層で任意の2トークン間を直接結びつけられる。ただしO(n²)の計算・メモリコストが伴い、これがFlashAttention・Sparse Attention・KV Cache・GQAといった後続研究への動機となった。

Positional EncodingはSelf-Attentionが語順を区別しない集合的処理であるため必須で、現代LLMではRoPE（Rotary Position Embedding）への発展が見られる。Feed Forward Networkは各token位置に同一の2層MLP（ReLU活性化）を適用し、Attentionによるtoken間情報混合の後に各token表現を個別加工する役割を担う。各サブ層には残差接続とLayer Normalizationが付随する。

実験結果ではWMT 2014英独翻訳でTransformer bigが28.4 BLEU、英仏で41.8 BLEUを達成し、当時のSOTA相当を少ない学習コストで実現した。

実装上の注意点として、causal maskはsoftmax前のスコアに適用する（masked_fillで参照禁止位置をfloatの最小値に設定）。Attention weightはデバッグの手がかりとして使えるが、モデル判断の因果的説明には過信すべきでない。

現代のGPT系LLMはDecoder-only構造でRoPEを使用するなど原論文から発展しているが、「tokenをベクトル化→位置情報付与→Attentionで文脈混合→Feed Forwardで加工」という基本発想の理解に本論文が依然として有効な入口となる。

## アイデア

- Self-AttentionのO(n²)計算コストがFlashAttention・GQA・KV Cacheといった一連の効率化研究の出発点になっており、現代LLMの推論最適化を理解する上で原点として重要
- Positional EncodingはSelf-Attentionの語順不感性という構造的限界を補うために外部から注入するという設計思想が、RoPEなど位置埋め込みの発展系を読み解く際の基礎概念になる
- Attention weightは可視化・デバッグに使えるが因果的説明としては不完全という指摘は、LLM-as-judgeや監査エージェントの根拠提示設計において「モデルの内部状態をそのまま説明に使う危険性」を示す実践的示唆となる

## 前提知識

- **RNN** → /deep_115 AIを活用した都市型鉄砲水予測で都市を守る：Googleの新手法
- **Encoder-Decoder** → /deep_317 回帰言語モデル（RLM）による大規模システムのシミュレーション
- **Scaled Dot-Product Attention** (TODO: 読むべき)
- **Layer Normalization** (TODO: 読むべき)
- **残差接続** → /deep_105 TransformerでAttention Residualsを観察する

## 関連記事

- /deep_4483 Transformerの数式を完全整理：埋め込みからAttentionまで一気に俯瞰
- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_2654 Multi-Head Attentionはなぜ効くのか？（現代編）— 論文から理解の変遷を整理する
- /deep_2381 Multi-Head Attentionはなぜ効くのか？ — 論文から辿る理解の変遷
- /deep_4657 AIにおけるジェンダーバイアスの概観：測定・評価・緩和手法のサーベイ

## 原文リンク

[LLM解説シリーズ：Transformerの基本構造をAttention論文から読む](https://zenn.dev/kas_blog/articles/20260509-llm-05-transformer)
