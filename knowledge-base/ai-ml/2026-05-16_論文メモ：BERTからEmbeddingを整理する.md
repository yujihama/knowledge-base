---
title: "論文メモ：BERTからEmbeddingを整理する"
url: "https://zenn.dev/kas_blog/articles/20260509-llm-03-embedding"
date: 2026-05-16
tags: [BERT, Embedding, Transformer, MLM, WordPiece, contextualized representation, Sentence-BERT, RAG, Self-Attention, PyTorch]
category: "ai-ml"
related: [585, 2381, 1759, 1016, 113]
memo: "[Zenn LLM] 論文メモ：BERTからEmbeddingを整理する"
processed_at: "2026-05-16T12:00:41.697574"
---

## 要約

BERT論文（Devlin et al., 2018）を起点に、LLMにおけるEmbeddingの仕組みを整理した技術メモ。BERTはBidirectional Encoder Representations from Transformersの略で、Transformer EncoderとWordPieceトークナイザーを用い、Masked Language Modeling（MLM）とNext Sentence Prediction（NSP）の2つのタスクで事前学習される。

Embeddingの数式的な定義として、語彙サイズをV、隠れ次元をHとするとtoken embedding行列はE∈R^{V×H}で表され、token ID iのベクトルはその行列のi行目に対応する。BERTの入力表現は単純なtoken embeddingではなく、(1) token embedding（どのtokenか）、(2) segment embedding（文A/Bのどちらか）、(3) position embedding（系列中の位置）の3つを加算して構成される。TransformerのSelf-Attentionは語順情報を持たないため、position embeddingの付加が不可欠。

特殊トークンとして[CLS]（分類用）、[SEP]（文境界）、[MASK]（MLM予測対象）が定義される。文ペア入力時は「[CLS] 文A [SEP] 文B [SEP]」の形式に統一される。

MLMでは入力tokenの15%を予測対象とし、そのうち80%を[MASK]に置換、10%をランダムtokenに置換、10%をそのまま残すことで、事前学習とFine-tuning時の入力分布の乖離を緩和する。損失はmask対象位置のみで計算する（L_MLM = -Σ log p(t_i|x_{\M})）。NSPは[CLS]の最終表現を用いて2文の連続性を50%/50%の割合で学習するが、後続研究（RoBERTa等）でその必要性は再検討されている。

静的Embedding（word2vec, GloVe）との最大の違いは「文脈化表現（contextualized representation）」にある。入力層のtoken embeddingは同一単語で同一ベクトルだが、Transformer層通過後は周囲のtokenとのSelf-Attentionを経て文脈依存の表現に変化する。「bank（銀行/川岸）」の例が示すように、多義語の意味分離に有効。

実装上の注意点として、(1) tokenizerとEmbedding行列は必ずセットで管理（差し替えるとIDとtokenの対応が崩れる）、(2) [CLS]表現はRAGや類似度検索には必ずしも最適でなく、Sentence-BERTのように文類似度特化モデルを使うべき、(3) batch処理時はpadding位置をattention maskで明示的に除外する、の3点が強調されている。実装例としてPyTorchによるBertStyleInputEmbeddingクラスが示されており、LayerNormとDropout（0.1）も含む構成になっている。

監査エージェント開発への示唆として、RAGベースの証拠検索システムを構築する際には「BERTのCLS出力を汎用Embeddingとして流用する」落とし穴を避け、検索タスクに特化した学習目的のモデル（Sentence-BERT系）を選定することが重要。

## アイデア

- BERTの入力Embeddingは3種（token/segment/position）の加算で構成されるが、文脈化は入力層ではなくTransformer通過後に発生するという層ごとの責務分離の明確さが、モデル設計の理解を深める上で重要
- MLMの15%ルールで[MASK]置換80%・ランダム10%・そのまま10%という分割は、事前学習とFine-tuningの入力分布ギャップを意図的に緩和する設計であり、データ拡張戦略として汎用的に応用できる発想
- [CLS]表現が分類タスクには有効でも類似度検索には不適という指摘は、RAGシステム設計において「タスクに合った学習目的のEmbeddingモデルを選ぶ」という原則を具体的に示しており、監査証拠検索エンジン設計に直結する

## 前提知識

- **Transformer Encoder** (TODO: 読むべき)
- **Self-Attention** → /deep_5561 Context Engineeringとは何か？──プロンプトの次に来る、LLMへの情報設計という技術【2026】
- **WordPiece tokenizer** (TODO: 読むべき)
- **word2vec / GloVe** (TODO: 読むべき)
- **Fine-tuning** → /deep_1224 AIモデルのカスタマイズへの移行はアーキテクチャ上の必須事項

## 関連記事

- /deep_585 nanoVLMでゼロから実装するKVキャッシュ
- /deep_2381 Multi-Head Attentionはなぜ効くのか？ — 論文から辿る理解の変遷
- /deep_1759 BERT 101：最先端NLPモデルの仕組みを解説
- /deep_1016 Amazon SageMaker向けHugging Face埋め込みコンテナの正式リリース
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた

## 原文リンク

[論文メモ：BERTからEmbeddingを整理する](https://zenn.dev/kas_blog/articles/20260509-llm-03-embedding)
