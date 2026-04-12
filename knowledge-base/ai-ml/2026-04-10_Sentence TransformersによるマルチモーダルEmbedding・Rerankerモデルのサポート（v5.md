---
title: "Sentence TransformersによるマルチモーダルEmbedding・Rerankerモデルのサポート（v5.4）"
url: "https://huggingface.co/blog/multimodal-sentence-transformers"
date: 2026-04-10
tags: [SentenceTransformers, multimodal-embedding, CrossEncoder, reranker, Qwen3-VL, RAG, visual-document-retrieval, retrieval]
category: "ai-ml"
memo: "[HF Blog] Multimodal Embedding & Reranker Models with Sentence Transformers"
processed_at: "2026-04-10T12:34:56.281000"
---

## 要約

Sentence Transformers v5.4にて、テキストだけでなく画像・音声・動画を同一API（model.encode()）でエンコードし、共通の埋め込み空間で比較できるマルチモーダル対応が追加された。

主な機能は2つ。①マルチモーダルEmbeddingモデル：異なるモダリティの入力を同一ベクトル空間にマッピングし、テキストクエリと画像ドキュメントを直接コサイン類似度で比較可能。代表モデルはQwen/Qwen3-VL-Embedding-2B（埋め込み次元2048）。画像はURL・ローカルパス・PIL Imageオブジェクトなど複数形式で入力できる。②マルチモーダルRerankerモデル：テキスト/画像/音声/動画の混合ペアに対して関連度スコアを出力するCrossEncoderモデル。Embeddingより精度が高い一方、各ペアを個別推論するためレイテンシは高い。

APIとしてはencode_query()とencode_document()が新設されており、クエリ用・ドキュメント用の異なるインストラクションプロンプトを自動適用する（retrieval系モデルで重要）。これはencode()の薄いラッパーで、既存コードとの互換性を保ちつつ使える。

モダリティギャップ（modality gap）という現象が説明されており、異なるモダリティの埋め込みは同一空間内でも別のクラスターを形成するため、クロスモーダル類似度スコアは同一モダリティ内（例：text-to-text）より低くなる（実験例：最高スコア0.51〜0.67程度）。ただし相対順序は保たれるため検索性能自体は維持される。

Retrieve & Rerankパイプラインの実装例も示されており、BM25やEmbeddingで候補を絞り込んだ後にMultimodalCrossEncoderでリランキングするパターンが推奨されている。

インストールは用途別のextraで対応（image/audio/video）。VLMベースモデル（Qwen3-VL-2B）には最低8GB VRAM必要で、8Bバリアントは約20GBが目安。CPU推論は極めて遅く、CLIPなどのモデルの利用が推奨されている。

## アイデア

- モダリティギャップ（modality gap）の存在：テキストと画像の埋め込みは同一空間内で別クラスターを形成するため類似度スコアが低くなるが、相対順序は保たれる。スコアの絶対値ではなく順序で判断すべきという設計上の示唆
- encode_query()/encode_document()によるインストラクション自動適用：クエリ側とドキュメント側で異なるプロンプトを自動選択する設計は、retrieval性能向上のベストプラクティスであり、エージェントシステムでの検索コンポーネント設計に応用可能
- マルチモーダルReranker（CrossEncoder）のRetrieve & Rerankパターン：Embeddingで粗く候補を絞りRerankerで精度を上げる2段階構造は、監査ドキュメントの検索精度を保ちながらコストを抑える実装戦略として直接応用できる
## 関連記事

- /deep_1580 Sentence Transformersモデルのトレーニングとファインチューニング
- /deep_707 Sentence Transformers v4によるリランカーモデルのトレーニングとファインチューニング
- /deep_1022 Sentence Transformers v3によるEmbeddingモデルのトレーニングとファインチューニング
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1334 製造業向けRAGシステムのアクセス制御設計

## 原文リンク

[Sentence TransformersによるマルチモーダルEmbedding・Rerankerモデルのサポート（v5.4）](https://huggingface.co/blog/multimodal-sentence-transformers)
