---
title: "Decoder-only TransformerとはなにかGPT系LLMの構造を整理"
url: "https://zenn.dev/kas_blog/articles/20260509-llm-08-decoder-only-transformer"
date: 2026-05-25
tags: [Decoder-only Transformer, GPT-2, causal mask, KV Cache, 自己回帰言語モデル, byte-level BPE, Pre-LN, zero-shot]
category: "ai-ml"
related: [4044, 1968, 6277, 1758, 1531]
memo: "[Zenn LLM] Decoder-only Transformerとは？GPT系LLMの構造を整理"
processed_at: "2026-05-25T09:08:03.010476"
---

## 要約

GPT-2論文「Language Models are Unsupervised Multitask Learners」（Radfordら、2019年）を起点に、Decoder-only Transformerの構造と実装上の要点を解説した技術メモ。

Decoder-only Transformerは、元のTransformerのDecoder部分からEncoder-Decoder Attentionを取り除き、Masked Self-AttentionとFeed Forward Networkを積み重ねた構成。各位置で過去tokenのみを参照して次tokenを予測する自己回帰型言語モデル（causal language model）の実装に対応する。

GPT-2の学習目的は自己回帰分解 P(u) = ∏P(u_i|u_1,...,u_{i-1}) で表され、WebTextと呼ばれる大規模Webテキストを用いてタスク別ラベルなしの自己教師あり学習を実施。タスク専用fine-tuningなしのゼロショット評価で複数タスクの性能を示した点が新規性。

構造の流れは「token ids → token embedding + positional embedding → Transformer block × N（masked multi-head self-attention + FFN） → final LayerNorm → vocabulary logits」。GPT-2ではLayer Normalizationを各sub-blockの入力側に移動し（Pre-LN）、最終出力前にも追加することで深層モデルの安定学習を図っている。

causal maskは Attention score行列に M_ij（j>i のとき -∞、それ以外0）を加算し、未来tokenへの参照をsoftmax後に確率0にする。実装ではtorch.triu(..., diagonal=1)で上三角マスクを生成してmasked_fillで適用する。diagonal=1のずれを逆にすると過去ではなく未来を参照するモデルになり自己回帰として破綻するため注意が必要。

KV Cacheとの相性が良い理由はDecoder-onlyの因果構造にある。未来tokenを参照しないため、過去tokenのKey/Valueは後続stepで変化しない。生成時にキャッシュを再利用することで毎step全tokenを再計算するコスト（O(n²)）を削減できる一方、シーケンス長に比例したキャッシュメモリが必要になるトレードオフがある。

byte-level BPEによるトークナイズ、learned positional embedding、residual connectionもGPT-2の設計要素として列挙されており、特にbyte-level BPEは未知語を排除し多様な文字列を扱えるようにする実装上の利点がある。

「ゼロショットで動くこと」と「常に正しく安全に動くこと」は別問題であり、Webデータに由来するバイアス・事実誤り・評価データとの重複・生成内容の制御は別途対処が必要と著者は指摘している。

## アイデア

- causal maskの数式（M_ij = -∞ for j>i）とtorch.triu(diagonal=1)の対応関係が明確で、学習時に全位置を並列計算しながら自己回帰生成と同じ条件を維持できる仕組みが実装視点で整理されている
- KV Cacheが有効な理由がDecoder-onlyの因果構造（過去K/Vは後から変化しない）に直結しており、Encoder-Decoder構造では同様に使えない理由と対比して理解できる
- GPT-2の新規性はモデル構造よりもWebTextという大規模・無ラベルデータでの学習によりタスク汎化が出現することを示した点にあり、複雑なマルチタスクヘッドを不要にするスケーリング仮説の前身として位置づけられる

## 前提知識

- **Transformer（Attention Is All You Need）** (TODO: 読むべき)
- **Self-Attention** → /deep_5561 Context Engineeringとは何か？──プロンプトの次に来る、LLMへの情報設計という技術【2026】
- **softmax / scaled dot-product attention** (TODO: 読むべき)
- **自己教師あり学習** → /deep_225 LeWorldModel入門: 15Mパラメータで実現するJEPAベースWorld Model
- **BPE（Byte Pair Encoding）** (TODO: 読むべき)

## 関連記事

- /deep_4044 多肉植物LMを育てる (1) — データセットの作成とモデル訓練まで
- /deep_1968 Transformer に触れてみる (6) — GPT-2 もどきで簡単な会話をする
- /deep_6277 LLM解説シリーズ：Self-Attentionを数式と実装から理解する
- /deep_1758 🤗 TransformersにおけるConstrained Beam Searchによるテキスト生成の制御
- /deep_1531 🤗 EvaluateライブラリによるLLMバイアス評価

## 原文リンク

[Decoder-only TransformerとはなにかGPT系LLMの構造を整理](https://zenn.dev/kas_blog/articles/20260509-llm-08-decoder-only-transformer)
