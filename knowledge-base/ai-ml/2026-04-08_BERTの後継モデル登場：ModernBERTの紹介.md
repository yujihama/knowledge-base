---
title: "BERTの後継モデル登場：ModernBERTの紹介"
url: "https://huggingface.co/blog/modernbert"
date: 2026-04-08
tags: [ModernBERT, encoder-only, BERT, RoPE, Flash Attention, RAG, 埋め込みモデル, 長文脈]
category: "ai-ml"
memo: "[HF Blog] Finally, a Replacement for BERT: Introducing ModernBERT"
processed_at: "2026-04-08T12:28:11.601249"
---

## 要約

ModernBERTは、Answer.AIとLightOnが共同開発したエンコーダー専用モデルのファミリーで、2018年に登場したBERTの事実上の後継モデルとして2024年12月に公開された。BERTはHugging Faceハブで月間6,800万ダウンロードを誇る2番目に人気のモデルであり続けているが、ModernBERTはその性能と速度を全面的に上回るPareto改善を実現している。

アーキテクチャ面では、近年のLLM研究の成果を多数取り込んでいる。具体的には、RoPE（Rotary Position Embeddings）の採用、Alternating Attention（全トークン注目のグローバルアテンションとローカルスライディングウィンドウアテンションの交互適用）、Flash Attention 2のサポート、GeGLU活性化関数、レイヤーノルムの位置変更（Pre-normalization）などが含まれる。これらにより、BERTの512トークン制限に対してModernBERTは8,192トークンまでのシーケンス長を処理可能となった。

モデルサイズはbase（149Mパラメータ）とlarge（395Mパラメータ）の2種類。学習データは2兆トークン以上で構成され、英語・多言語テキストに加えてコードデータを大量に含む点が従来のエンコーダーと大きく異なる。これにより、コード検索やIDEの機能拡張といった新たなユースケースへの適用が可能になった。

性能面では、GLUE、SQUAD、NERなどの標準NLPベンチマークで既存のエンコーダーモデルを上回り、特にlong-contextタスクでは8kトークン対応が際立った優位性をもたらす。推論速度もBERTより大幅に向上しており、特にFlash Attention 2使用時にその恩恵が顕著である。

使用方法はBERTと互換性があり、`AutoModelForMaskedLM`や`pipeline`（fill-maskタスク）でそのまま利用可能。token_type_IDsが不要になった点が唯一の差異。RAGパイプラインでの文書埋め込み、テキスト分類、固有表現抽出など、既存のBERTユースケースにそのままスロットイン置換として使用できる。

## アイデア

- 8,192トークンのコンテキスト長により、チャンク分割不要な全文書検索（full document retrieval）が可能になり、RAGパイプラインの設計を根本から変えられる点
- Alternating Attentionによりグローバルとローカルの注意機構を交互に適用することで、長いシーケンスの計算コストを抑えつつ精度を維持する設計
- コードデータを大量に含む学習データにより、コード検索・コード分類など開発ツール領域へのエンコーダー適用範囲が大幅に拡大した点
## 関連記事

- /deep_1264 本番環境でのLLM最適化：低精度・Flash Attention・アーキテクチャ革新
- /deep_1021 Text Generation Inference（TGI）ベンチマークツールの使い方と活用指針
- /deep_707 Sentence Transformers v4によるリランカーモデルのトレーニングとファインチューニング
- /deep_1218 Hugging Face Inference EndpointsでEmbeddingモデルをデプロイする
- /deep_1016 Amazon SageMaker向けHugging Face埋め込みコンテナの正式リリース

## 原文リンク

[BERTの後継モデル登場：ModernBERTの紹介](https://huggingface.co/blog/modernbert)
