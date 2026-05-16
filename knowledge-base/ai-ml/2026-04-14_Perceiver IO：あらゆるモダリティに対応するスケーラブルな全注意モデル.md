---
title: "Perceiver IO：あらゆるモダリティに対応するスケーラブルな全注意モデル"
url: "https://huggingface.co/blog/perceiver"
date: 2026-04-14
tags: [Perceiver IO, Transformer, マルチモーダル, クロスアテンション, 潜在変数, HuggingFace Transformers, 光学フロー, Fourier特徴量]
category: "ai-ml"
related: [1467, 1639, 1762, 1494, 1615]
memo: "[HF Blog] Perceiver IO: a scalable, fully-attentional model that works on any modality"
processed_at: "2026-04-14T12:11:12.081804"
---

## 要約

Perceiver IOは、DeepMindが提案したTransformerベースのニューラルネットワークで、テキスト・画像・音声・動画・点群など任意のモダリティおよびその組み合わせを単一アーキテクチャで処理できる。2021年12月にHugging Face Transformersライブラリに統合された。

通常のTransformerの自己注意機構は入力長の二乗オーダーでメモリと計算量が増大するため、高次元データへの直接適用が困難だった。Wav2Vec2は生波形を時系列特徴量に変換し、ViTは画像をパッチ列に分割し、ViViTは動画を時空間チューブに分割することでこの問題を回避していたが、いずれもモダリティ固有の前処理が必要だった。

Perceiverはこの問題を潜在変数（latent variables）を介することで解決する。入力はクロスアテンションでのみ潜在変数と対話し（入力→KV、潜在変数→Q）、自己注意は256〜512個の潜在変数間でのみ行われる。これにより、エンコーダの計算量は入力サイズに対して線形となり、潜在空間での自己注意は入力サイズに非依存となる。Perceiver IOはさらに出力側も汎化し、クロスアテンションにより任意形式の出力（分類ロジット、光学フロー等）を生成する。

Hugging Face実装では、PerceiverModelクラスを基盤に、preprocessor・decoder・postprocessorの3コンポーネントをオプションで組み合わせる設計となっている。テキスト分類ではPerceiverTextPreprocessor（バイトID埋め込み＋位置エンコーディング）＋PerceiverClassificationDecoderを使用し、2048バイト長の生UTF-8バイト列を直接入力できるためWordPieceやBPEなどのトークナイザが不要。画像分類ではFourier特徴量による位置エンコーディング（50,176次元の入力を224×224×3のピクセルから生成）を用いる。光学フロー推定ではPerceiverImagePreprocessorで2枚の画像を連結し、デコーダ側でピクセル座標のFourier特徴量をクエリとして使用することで368×496の密な光学フロー場を出力する。マルチモーダル自己符号化では音声・画像・ラベルを同時にエンコードし、モダリティ別のpostprocessorで各出力を復元する。

監査エージェント開発の観点では、Perceiver IOの「モダリティ非依存の単一アーキテクチャ」という設計思想は、テキスト（規程文書）・数値（財務データ）・画像（証憑）など異種データを統合処理する監査AIに応用可能な概念的示唆を持つ。

## アイデア

- 自己注意を潜在空間に閉じ込めることで、入力サイズに対する二乗スケーリング問題を線形＋定数に分解する設計は、長文書や高解像度データを扱う監査AIのアーキテクチャ設計に参考になる
- 生UTF-8バイト列を直接入力できることでトークナイザ起因のバイアスを排除できる点は、LLM-as-judgeにおける公平性担保の文脈で興味深い
- preprocessor・decoder・postprocessorを差し替えるだけで同一基盤モデルを異なるタスクに適用できるモジュール設計は、複数タスクを処理するエージェントシステムのコンポーネント設計の参考になる

## 前提知識

- **Transformer・自己注意機構** (TODO: 読むべき)
- **クロスアテンション** → /deep_574 Attention Frequency Modulation: 拡散モデルのクロスアテンションに対するトレーニング不要なスペクトル変調
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Fourier特徴エンコーディング** (TODO: 読むべき)
- **HuggingFace Transformers** → /deep_1394 TransformersライブラリによるグラフClassification：Graphormerを用いた実装ガイド

## 関連記事

- /deep_1467 Car-GPT: LLMは自動運転を実現できるか？
- /deep_1639 Car-GPT: LLMは自動運転を実現できるか？
- /deep_1762 🤗 TransformersのWav2Vec2で大容量音声ファイルの自動音声認識を実現する方法
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_1615 🤗 Datasetsにおける音声・画像データセット対応の新ドキュメント公開

## 原文リンク

[Perceiver IO：あらゆるモダリティに対応するスケーラブルな全注意モデル](https://huggingface.co/blog/perceiver)
