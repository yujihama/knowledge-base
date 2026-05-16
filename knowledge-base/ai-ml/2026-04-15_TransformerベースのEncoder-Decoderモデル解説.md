---
title: "TransformerベースのEncoder-Decoderモデル解説"
url: "https://huggingface.co/blog/encoder-decoder"
date: 2026-04-15
tags: [Transformer, Encoder-Decoder, seq2seq, クロスアテンション, 自己回帰生成, T5, BART, MarianMT, Pegasus, HuggingFace]
category: "ai-ml"
related: [1880, 1664, 1529, 1494, 201]
memo: "[HF Blog] Transformer-based Encoder-Decoder Models"
processed_at: "2026-04-15T12:27:12.052605"
---

## 要約

本記事は、Vaswani et al. (2017) の「Attention is All You Need」で提案されたTransformerベースのEncoder-Decoderアーキテクチャを、数学的定式化と推論時の動作に焦点を当てて詳細に解説するHugging Faceのブログ記事である。

まず背景として、自然言語生成（NLG）におけるseq2seqタスク（要約・翻訳等）の歴史を概説する。DNN（固定次元マッピング）の限界を指摘した上で、Cho et al. (2014) とSutskever et al. (2014) によるRNNベースのEncoder-Decoderへと至る経緯を説明する。RNNエンコーダは入力系列 X_{1:n} を固定ベクトル c に圧縮し、デコーダは c を初期状態として自己回帰的にターゲット系列 Y_{1:m} を生成する。デコーダは p(y_i | Y_{0:i-1}, c) の条件付き分布をモデル化し、積の形で完全な系列確率を構成する。

TransformerベースのEncoder-Decoderでは、エンコーダが入力トークン列をコンテキスト行列（contextualized encoding）に変換し、デコーダはクロスアテンション機構を通じてこの行列の全ステップを参照しながらトークンを自己回帰的に生成する。RNNの固定長ベクトル c と異なり、Transformerエンコーダは各入力位置に対応する隠れ状態ベクトルの行列を出力するため、長距離依存関係の把握が大幅に改善される。

エンコーダ部は複数のTransformerブロックから構成され、各ブロックは自己アテンション層とフィードフォワード層を持つ。入力トークンはまずワード埋め込みと位置埋め込みに変換され、各ブロックを経て文脈化された表現へと変換される。デコーダ部も同様にTransformerブロックを重ねるが、各ブロックにマスク済み自己アテンション層（因果的マスク）とエンコーダ出力へのクロスアテンション層を追加で持つ。

推論時の生成はgreedy decoding（各ステップで最大確率トークンを選択）またはbeam searchで行われる。生成は特殊トークン（BOS）から始まり、EOSトークンが生成されるか最大長に達するまで続く。実装例としてMarianMTによる翻訳と、T5によるテキスト要約のコードが示されており、🤗Transformersライブラリ（v4.2.1）のtranslation_pipelineやsummarization_pipelineで数行で実行可能なことが示される。

T5、BART、MarianMT、Pegasusなど複数のモデルが同アーキテクチャを採用しており、事前学習目標の設計（マスク言語モデル、ノイズ除去など）が異なるのみである。監査エージェント開発への示唆としては、このEncoder-Decoderアーキテクチャは「文書→要約」「長文→構造化出力」といったseq2seqタスクに直接応用可能であり、監査報告書の自動要約や調書生成パイプラインの基盤モデルとして活用できる点が挙げられる。

## アイデア

- RNNの固定長コンテキストベクトル c の情報ボトルネック問題を、Transformerのエンコーダが行列（全位置の隠れ状態）を出力することで根本的に解決している点：クロスアテンションにより各デコードステップで入力の任意位置を参照可能
- デコーダの因果的マスク（causal masking）により、学習時は教師強制（teacher forcing）で全ステップを並列計算しつつ、推論時は自己回帰的に逐次生成するという非対称性：これが高速な学習と柔軟な生成を両立させる設計の核心
- T5・BART・Pegasusなど多数のモデルがアーキテクチャを共有しながら事前学習目標のみを変えることでタスク適性が異なる点：同一の推論コードで複数のseq2seqタスク（翻訳・要約・QA）に対応できる汎用性が🤗Transformers設計思想の中心にある

## 前提知識

- **Transformer self-attention** (TODO: 読むべき)
- **RNN Encoder-Decoder** (TODO: 読むべき)
- **自己回帰言語モデル** (TODO: 読むべき)
- **Beam Search** → /deep_1758 🤗 TransformersにおけるConstrained Beam Searchによるテキスト生成の制御
- **Teacher Forcing** (TODO: 読むべき)

## 関連記事

- /deep_1880 分散学習：🤗 TransformersとAmazon SageMakerでBART/T5を要約タスクにファインチューニング
- /deep_1664 GraphcoreとHugging FaceがIPU対応Transformerモデル群を大幅拡充
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜

## 原文リンク

[TransformerベースのEncoder-Decoderモデル解説](https://huggingface.co/blog/encoder-decoder)
