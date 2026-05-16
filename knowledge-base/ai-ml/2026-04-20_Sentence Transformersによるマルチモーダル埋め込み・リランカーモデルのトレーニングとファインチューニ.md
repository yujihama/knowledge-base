---
title: "Sentence Transformersによるマルチモーダル埋め込み・リランカーモデルのトレーニングとファインチューニング"
url: "https://huggingface.co/blog/train-multimodal-sentence-transformers"
date: 2026-04-20
tags: [Sentence Transformers, マルチモーダル埋め込み, Visual Document Retrieval, Qwen3-VL, CachedMultipleNegativesRankingLoss, MatryoshkaLoss, ファインチューニング, NDCG@10, VLM, RAG]
category: "ai-ml"
related: [1928, 1916, 986, 305, 1440]
memo: "[HF Blog] Training and Finetuning Multimodal Embedding & Reranker Models with Sentence Transformers"
processed_at: "2026-04-20T12:23:09.192889"
---

## 要約

Sentence Transformersライブラリが新たにマルチモーダル埋め込みモデルのトレーニング・ファインチューニング機能をサポートした。本記事では、Qwen/Qwen3-VL-Embedding-2B（2Bパラメータのビジョン言語モデルベース埋め込みモデル）をVisual Document Retrieval（VDR）タスク向けにファインチューニングした実例を詳述する。VDRとは、テキストクエリに対して関連するドキュメントページ画像（チャート・表・レイアウトを含むスクリーンショット）を検索するタスクである。ファインチューニングにはtomaarsen/llamaindex-vdr-en-train-preprocessedデータセット（LlamaIndex公開の多言語VDRデータセットの英語サブセット、約50万件のクエリ-画像ペア）を使用。損失関数はCachedMultipleNegativesRankingLoss（大バッチサイズを効率的に扱うキャッシュ付き対照学習損失）とMatryoshkaLoss（複数の埋め込み次元を同時に最適化し、推論時に次元数を柔軟に選択可能にする手法）を組み合わせた。評価指標NDCG@10において、ベースモデルの0.888からファインチューニング後のtomaarsen/Qwen3-VL-Embedding-2B-vdrは0.947を達成し、4倍のサイズを持つモデルを含む既存VDRモデル全てを上回った。トレーニングパイプラインはテキスト専用モデルと同一のSentenceTransformerTrainerを使用し、データセットに画像カラムを含めることでモデルのプロセッサが自動的に画像前処理を担う。モデル構成としては、単一のVLMバックボーン（Qwen3-VL等）を使うアプローチと、Routerモジュールで各モダリティ用の軽量エンコーダ（テキスト用all-MiniLM-L6-v2、画像用SigLIP2等）を組み合わせるアプローチの2種類をサポート。後者はモダリティ間の埋め込み空間をDense投影層で整合させるためトレーニングが必要。データセット形式はHuggingFace Datasetsのarrow形式で画像をPIL.Imageとして格納し、`sentence-transformers`のDatasetフォーマット変換ユーティリティを介してanchor/positive/negativeトリプレット形式に対応。processor_kwargsでmax_pixels（600×600）を設定することで品質とメモリのトレードオフを制御できる。監査AIへの示唆として、財務諸表やレポートのPDFページ画像を対象としたVDRタスクは、監査エージェントが証拠文書を視覚的に検索する際に直接応用可能であり、同手法でドメイン特化ファインチューニングを行うことで既存汎用モデルを大幅に上回る精度が期待できる。

## アイデア

- MatryoshkaLossにより単一モデルで複数の埋め込み次元（例：512次元〜2048次元）を同時学習でき、推論時にレイテンシ・精度のトレードオフを動的に選択できる点が、検索システムの実運用コスト最適化に有効
- Routerモジュールによりテキストエンコーダとビジョンエンコーダを独立に配置し、クエリ側とドキュメント側で異なるエンコーダを割り当てるroute_mappingsの仕組みは、非対称検索（短いテキストクエリ vs 長い文書画像）のアーキテクチャ設計指針として参考になる
- 汎用VLM（Qwen3-VL-2B）をドメイン特化データでファインチューニングするだけで4倍サイズの既存モデルを超えた結果は、モデルサイズよりもドメイン適合度が検索精度に与える影響の大きさを示しており、小規模モデルの実用化可能性を示す

## 前提知識

- **Sentence Transformers** → /deep_303 Sentence TransformersがHugging Faceに移管——月間100万ユーザーの埋め込みライブラリが新体制へ
- **対照学習（ContrastiveLoss）** (TODO: 読むべき)
- **Vision-Language Model (VLM)** (TODO: 読むべき)
- **NDCG@10** (TODO: 読むべき)
- **RAG（Retrieval Augmented Generation）** (TODO: 読むべき)

## 関連記事

- /deep_1928 隠れた真実を見抜く：フィールド可視化から記号的解析解を推論するVisual-to-Symbolic AI
- /deep_1916 生成AIの回答精度が上がる3つの鉄則！データ品質が企業DXを制する理由
- /deep_986 ドキュメント画像向けマルチモーダルTextImageデータ拡張の紹介
- /deep_305 オープンモデルでOCRパイプラインを強化する：VLMベースドキュメントAIの実践ガイド
- /deep_1440 Sentence TransformersによるマルチモーダルEmbedding・Rerankerモデルのサポート（v5.4）

## 原文リンク

[Sentence Transformersによるマルチモーダル埋め込み・リランカーモデルのトレーニングとファインチューニング](https://huggingface.co/blog/train-multimodal-sentence-transformers)
