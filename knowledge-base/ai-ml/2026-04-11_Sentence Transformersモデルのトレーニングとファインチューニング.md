---
title: "Sentence Transformersモデルのトレーニングとファインチューニング"
url: "https://huggingface.co/blog/how-to-train-sentence-transformers"
date: 2026-04-11
tags: [SentenceTransformers, embedding, fine-tuning, MultipleNegativesRankingLoss, TripletLoss, semantic-search, RAG, distilroberta]
category: "ai-ml"
memo: "[HF Blog] Train and Fine-Tune Sentence Transformers Models"
related: [1092, 735, 1378, 356, 1440]
processed_at: "2026-04-11T21:09:38.529395"
---

## 要約

本記事はHugging Faceが2022年8月に公開したSentence Transformers v3以前向けのトレーニングガイド。Sentence Transformersの仕組みは2層構造で、第1層にdistilroberta-baseなどの事前学習済みTransformerを用いてトークン単位のコンテキスト化埋め込みを生成し、第2層でMean Poolingなどにより固定長の文ベクトルに集約する。BERTをそのまま文埋め込みに使うと1万文の類似検索に約65時間かかるのに対し、Sentence Transformersは約5秒に短縮できる。また、BERT標準の平均トークン埋め込みは2014年のGloVeより性能が低いことも示されており、専用ファインチューニングの必要性が裏付けられている。

データセット形式は4種類に分類される。Case1は文ペア＋類似度ラベル（整数or浮動小数点）、Case2はラベルなしの正例ペア（パラフレーズ・QAペア・翻訳ペアなど）、Case3は文＋クラスラベル（整数）、Case4はアンカー・正例・負例のトリプレット形式。各形式に対して使用できる損失関数が異なり、Case2ではMultipleNegativesRankingLoss、Case4ではTripletLossが代表的。MultipleNegativesRankingLossはバッチ内の他の文を自動的に負例とするため、大規模な明示的負例ラベルが不要で実用性が高い。

トレーニングはSentenceTransformerクラスのfitメソッドで実行し、DataLoaderとEvaluatorを組み合わせる。EvaluatorにはEmbeddingSimilarityEvaluatorなどが用意されており、検証セットで性能を監視しながら学習できる。学習済みモデルはsave_to_hub()でHugging Face Hubに直接アップロード可能。

Sentence Transformersが適さないケースも明示されており、長文書の照合（チャンク分割が必要）、固有表現抽出・品詞タグ付け等のトークンレベルタスク、テキスト生成タスクには向かないとされている。全体として、RAGパイプラインの検索コンポーネントやセマンティック類似検索の基盤モデル構築に直接適用できる実践的なガイドとなっている。

## アイデア

- MultipleNegativesRankingLossはバッチ内負例を自動活用するため、明示的な負例アノテーションなしで高品質な埋め込みを学習できる点が実用上の最大の利点
- Case2形式（ラベルなし正例ペア）はQAペアや要約ペアから自動構築できるため、監査文書と対応する規制条文のペアなど業務データから教師信号を無標記で抽出できる可能性がある
- BERTをそのまま文埋め込みに使うと1万文の総当たり比較に65時間かかるのに対しSentence Transformersは5秒という定量比較は、本番システムの検索レイテンシ設計に直結する重要な数値
## 関連記事

- /deep_1092 テキスト埋め込みはテキストを完全にエンコードするか？――vec2textによる埋め込みの逆変換
- /deep_735 テキスト埋め込みはテキストを完全にエンコードするか？―vec2textによる埋め込み逆変換
- /deep_1378 テキスト埋め込みはテキストを完全にエンコードするか？——vec2textによる埋め込み反転攻撃
- /deep_356 テキスト埋め込みはテキストを完全にエンコードするか？—vec2textによる埋め込み逆変換攻撃
- /deep_1440 Sentence TransformersによるマルチモーダルEmbedding・Rerankerモデルのサポート（v5.4）

## 原文リンク

[Sentence Transformersモデルのトレーニングとファインチューニング](https://huggingface.co/blog/how-to-train-sentence-transformers)
