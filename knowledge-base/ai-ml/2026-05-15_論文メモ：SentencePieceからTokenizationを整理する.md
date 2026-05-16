---
title: "論文メモ：SentencePieceからTokenizationを整理する"
url: "https://zenn.dev/kas_blog/articles/20260509-llm-02-tokenization"
date: 2026-05-15
tags: [SentencePiece, Tokenization, BPE, Unigram Language Model, subword, NMT, 日本語LLM, subword regularization]
category: "ai-ml"
related: [4230, 4231, 2248, 1961, 2403]
memo: "[Zenn LLM] 論文メモ：SentencePieceからTokenizationを整理する"
processed_at: "2026-05-15T09:01:44.442828"
---

## 要約

SentencePiece（Kudo & Richardson, 2018）は、NMT（ニューラル機械翻訳）向けに設計された言語非依存のサブワードtokenizerシステムである。従来のサブワード分割ツール（subword-nmtなど）は、入力が既に単語列に分割済みであることを前提としており、日本語・中国語のようなnon-segmented languages（空白で単語境界が示されない言語）では形態素解析などの前処理が別途必要だった。SentencePieceはこの言語依存の前処理をなくし、raw textから直接サブワードモデルを学習できる点が最大の新規性である。

設計上の重要な特徴として「lossless tokenization」がある。空白を▁（メタ記号）として保持することで、token列を結合するだけで正規化後の文字列を復元できる。復元されるのは元のraw textではなく、Normalize後の文字列である点に注意が必要（例：全角→半角正規化後の表記）。

アルゴリズムとしてBPEとUnigram Language Modelの両方を実装している。BPEは頻出する隣接記号ペアを順次結合して語彙を構築し、分割は決定的になりやすい。Unigram Language Modelはサブワード列の確率P(x)=∏p(x_i)を最大化し、大きい候補語彙から不要なものを削る方向で学習する。推論時は最高確率の分割を選びつつ、学習時には複数候補を確率的にサンプリングする「subword regularization」と親和性が高い。

LLMへの影響として、語彙サイズはtoken数・文脈長消費・Embedding層メモリのトレードオフに直結する。語彙サイズが小さければtoken数が増えAttentionコストが上昇し、大きければEmbedding・出力層が肥大化する。日本語は空白による単語境界がないため分割が細かくなりやすく、コードはsnake_caseや括弧など意味を持つ記号が多いため分割設計の品質が出力安定性に直結する。

実験ではKFTT（京都関連英日翻訳データセット）でword modelよりサブワード分割のBLEUが高く、pre-tokenizationなしのraw textからの学習でも同等性能が報告されている。segmentation速度もsubword-nmtより大幅に高速。2018年時点のNMT実験であるが、tokenizerを自己完結モデルとして設計する思想は現在のLLM実務でも有効である。監査エージェント開発においては、日本語の法令・報告書テキストをLLMに入力する際のトークン効率とtoken列の解釈安定性の観点から、tokenizerの語彙設計とnon-segmented language対応の理解が直接的に役立つ。

## アイデア

- lossless tokenizationの設計：▁メタ記号で空白を保持しtoken列から正規化後テキストを完全復元可能にする発想は、LLMの入出力の可逆性保証として重要
- Unigram Language Modelのsubword regularization：学習時に複数の分割候補を確率的にサンプリングすることでモデルの汎化性能を高める正則化手法として、データ拡張の一種として捉えられる
- 語彙サイズのトレードオフ：token数（文脈長・Attentionコスト）とEmbedding/出力層サイズは逆相関し、言語・ドメイン特性に応じた最適化が必要という設計上の根本的制約

## 前提知識

- **BPE（Byte Pair Encoding）** (TODO: 読むべき)
- **サブワード分割** (TODO: 読むべき)
- **Embedding層** (TODO: 読むべき)
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **形態素解析** → /deep_5132 RAGの精度を上げる：チャンキングとハイブリッド検索をGoで実装した記録

## 関連記事

- /deep_4230 トークン超入門 — LLM の「単位」を腑に落とす
- /deep_4231 トークン入門 — すべてのLLMを支える最小単位
- /deep_2248 【LLM基礎】トークンとは何か？トークナイザーの仕組みと日本語のコスト特性
- /deep_1961 国産LLMは公開されている。なぜ誰も知らないのか！
- /deep_2403 国産LLMで日本語IoTデバイス制御を実現するOSSランタイム「nllm」を公開した

## 原文リンク

[論文メモ：SentencePieceからTokenizationを整理する](https://zenn.dev/kas_blog/articles/20260509-llm-02-tokenization)
