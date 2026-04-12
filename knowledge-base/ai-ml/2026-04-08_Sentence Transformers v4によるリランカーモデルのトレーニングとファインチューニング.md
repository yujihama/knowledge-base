---
title: "Sentence Transformers v4によるリランカーモデルのトレーニングとファインチューニング"
url: "https://huggingface.co/blog/train-reranker"
date: 2026-04-08
tags: [Sentence Transformers, reranker, cross-encoder, ModernBERT, fine-tuning, RAG, hard negative mining, BinaryCrossEntropyLoss]
category: "ai-ml"
memo: "[HF Blog] Training and Finetuning Reranker Models with Sentence Transformers v4"
processed_at: "2026-04-08T09:13:25.173197"
---

## 要約

Sentence Transformers v4.0では、クロスエンコーダー（リランカー）モデルのトレーニング基盤が刷新された。リランカーモデルはクエリとドキュメントのペアを同時に処理し、1つのスコアを出力するアーキテクチャで、バイエンコーダー型の埋め込みモデルよりも精度が高い一方、全ペアの計算が必要なため処理速度は遅い。実用的には「検索→リランク」の2段階パイプラインの後段として使われる。

トレーニングの主要コンポーネントは5つ：Dataset（HuggingFace Hub または CSV/JSON等のローカルデータ）、Loss Function（BinaryCrossEntropyLoss等、データ形式に応じて選択）、TrainingArguments、Evaluator（CrossEncoderCorrelationEvaluatorやCrossEncoderRerankingEvaluator）、そしてCrossEncoderTrainer。データセットのカラム構成とロス関数の入力要件を一致させる必要があり、「label/score」カラムが自動的にラベルとして認識される。

ハードネガティブマイニングも標準サポートされており、意味的に近いが誤った候補文書を学習データに含めることでモデルの識別精度を向上させる。マルチデータセットトレーニングにも対応し、異なるドメインのデータを同時に学習可能。

評価結果として、ModernBERT-baseをベースにGooAQデータセットでファインチューニングした tomaarsen/reranker-ModernBERT-base-gooaq-bce は、一般公開されている13の主要リランカーモデルを評価データセットで上回り、4倍大きいモデルにも勝利した。さらにModernBERT-largeベースの tomaarsen/reranker-ModernBERT-large-gooaq-bce は汎用リランカーモデルの中で最高性能を達成。ドメイン特化ファインチューニングがモデルサイズの差を補って余りあることを実証した。

トレーニングTipsとして、学習率・バッチサイズ・エポック数のチューニング指針、W&BやTensorBoardによるトラッキング設定、EarlyStoppingCallbackの活用なども解説されている。

## アイデア

- ドメイン特化ファインチューニングにより、4倍大きい汎用モデルを超えられることが定量的に示された点は、リソース制約下での実用戦略として重要
- ハードネガティブマイニングを標準パイプラインに組み込むことで、意味的に近い誤答を識別する難タスクへの対応力が上がる
- CrossEncoderRerankingEvaluatorによりトレーニング中の実タスク性能をリアルタイム監視でき、過学習・汎化のバランスを制御しやすい

## Yujiの取り組みへの示唆

監査エージェントのRAGパイプラインで「監査基準・規程文書の中から最も関連する根拠を精度高く選別する」後段リランカーを自社データでファインチューニングする際に直接活用できる。特に監査領域特有の語彙・表現（内部統制、リスク評価、勘定科目等）を含むドメインデータでModernBERTベースモデルをファインチューニングすることで、汎用リランカーを超える性能が期待できる。LangGraphで構築中のエージェントの検索ステップにCrossEncoderTrainerで作成したモデルを組み込む構成は、実装コストも低く即効性が高い。

## 原文リンク

[Sentence Transformers v4によるリランカーモデルのトレーニングとファインチューニング](https://huggingface.co/blog/train-reranker)
