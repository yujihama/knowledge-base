---
title: "Sentence Transformers v3によるEmbeddingモデルのトレーニングとファインチューニング"
url: "https://huggingface.co/blog/train-sentence-transformers"
date: 2026-04-09
tags: [SentenceTransformers, EmbeddingModel, FineTuning, MultipleNegativesRankingLoss, CoSENTLoss, RAG, SemanticSearch, HuggingFace]
category: "ai-ml"
memo: "[HF Blog] Training and Finetuning Embedding Models with Sentence Transformers v3"
processed_at: "2026-04-09T09:25:27.017765"
---

## 要約

Sentence Transformers v3.0は、プロジェクト開始以来最大のアップデートであり、新しいトレーニングアプローチを導入している。本ブログ記事では、特定タスクに向けたEmbeddingモデルのファインチューニング手法を解説する。

【主要コンポーネント】
トレーニングは5つの要素で構成される：(1) Dataset（datasets.Dataset/DatasetDict形式）、(2) Loss Function、(3) Training Arguments（任意）、(4) Evaluator（任意）、(5) SentenceTransformerTrainer。

【データセット】
Hugging Face Hub上の`sentence-transformers`タグ付きデータセットを`load_dataset`で直接利用可能。ローカルCSV/JSON/Parquet/Arrow/SQLも対応。データセットのカラム順序はロス関数の入力順序に対応させる必要があり、`"label"`または`"score"`カラムがラベルとして認識される。

【ロス関数】
CoSENTLoss、AnglELoss、CosineSimilarityLoss、TripletLoss、MultipleNegativesRankingLossなど多数。データ形式（ペア+スコア、トリプレット等）によって選択が異なる。MultipleNegativesRankingLossはラベル不要で、バッチ内の他サンプルをnegativeとして活用するため、教師なしデータに有効。

【Evaluator】
- EmbeddingSimilarityEvaluator：STSbデータセットでSpearman相関を計測
- TripletEvaluator：AllNLIデータセットでtripletの正解率を計測
eval_stepsごとに実行可能で、訓練中のモデル品質をモニタリングできる。

【Training Arguments】
SentenceTransformersTrainingArgumentsでbatch_size、epochs、learning_rate、warmup_ratio、eval_strategy、save_strategy等を制御。W&B・MLflow・TensorBoardとのインテグレーションもサポート。

【Multi-Dataset Training】
複数データセットを辞書形式で渡し、データセットごとに異なるロス関数を適用可能。各バッチはラウンドロビン方式でサンプリングされ、多様なタスクを同時学習できる。

【後方互換性】
旧来のfit()メソッドは非推奨となり、新Trainerへの移行が推奨されている。

## アイデア

- MultipleNegativesRankingLossはラベルなしペアデータだけでEmbeddingモデルを訓練できるため、ドメイン固有データが少ない環境（監査文書等）でも活用しやすい
- Multi-Dataset Trainingにより、異なる性質のタスク（類似度判定・検索・分類）を単一モデルに同時学習させる設計が可能で、汎用Embeddingの品質向上が期待できる
- EvaluatorとW&B/MLflowの統合により、訓練中のモデル品質をリアルタイム追跡できる評価パイプラインを構築でき、LLM-as-judgeと組み合わせた自動評価ループの設計に示唆を与える
## 関連記事

- /deep_1021 Text Generation Inference（TGI）ベンチマークツールの使い方と活用指針
- /deep_1440 Sentence TransformersによるマルチモーダルEmbedding・Rerankerモデルのサポート（v5.4）
- /deep_141 Hugging Faceにおけるオープンソースの現状：2026年春
- /deep_1016 Amazon SageMaker向けHugging Face埋め込みコンテナの正式リリース
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド

## 原文リンク

[Sentence Transformers v3によるEmbeddingモデルのトレーニングとファインチューニング](https://huggingface.co/blog/train-sentence-transformers)
