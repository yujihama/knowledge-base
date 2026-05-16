---
title: "🤗 TransformersでViTを画像分類にファインチューニングする"
url: "https://huggingface.co/blog/fine-tune-vit"
date: 2026-04-13
tags: [ViT, Vision Transformer, 画像分類, ファインチューニング, HuggingFace, Transformers, ViTImageProcessor, Trainer API, beans dataset, transfer learning]
category: "ai-ml"
related: [1529, 1575, 1216, 647, 1579]
memo: "[HF Blog] Fine-Tune ViT for Image Classification with 🤗 Transformers"
processed_at: "2026-04-13T12:36:28.768237"
---

## 要約

本記事は、Hugging FaceのTransformersとDatasetsライブラリを使い、Vision Transformer（ViT）を画像分類タスクにファインチューニングする手順を解説したチュートリアルである。ViTは2021年6月にGoogle Brainが発表したモデルで、NLPで成功したTransformerアーキテクチャを画像に応用した手法。具体的には、画像をグリッド状のパッチ（例：16×16ピクセル）に分割し、各パッチを線形投影でトークン化してTransformerに入力する。これにより、テキストのトークン列と同様の処理が可能になる。

データセットにはHugging Face Hub上の`beans`データセットを使用。葉の画像から「angular_leaf_spot」「bean_rust」「healthy」の3クラスを分類する。データ処理には`ViTImageProcessor`（`google/vit-base-patch16-224-in21k`）を使い、リサイズ（224×224）・正規化（mean/std=0.5）を適用。`ds.with_transform()`でオンザフライ変換を実装することで、大規模データセットでもメモリ効率よく処理できる。

モデルは`ViTForImageClassification.from_pretrained()`でロードし、`num_labels`とラベルマッピング（`id2label`/`label2id`）を指定する。学習はHugging FaceのTrainer APIを使用し、`TrainingArguments`でエポック数・バッチサイズ・評価戦略（`epoch`ごと）・ログ設定を定義。評価指標にはaccuracyを使用し、`datasets.load_metric('accuracy')`で実装。データコレーターはカスタム関数でピクセル値をスタックしてテンソルに変換する。

トレーニング後、`trainer.push_to_hub()`でモデルをHubに公開可能。推論時は`pipeline('image-classification')`を使いURLから直接画像を入力できる。監査AIへの示唆として、このパターン（事前学習済みモデルのドメイン特化ファインチューニング）は監査エージェントにおける証拠書類の画像分類（領収書・契約書・異常検知スクリーンショット等）への応用が直接可能。特に`with_transform`による遅延処理と`Trainer`の抽象化により、少量コードで本番レベルの画像分類器を構築できる点は実用的である。

## アイデア

- NLPのトークン化と全く同じ抽象化で画像を扱える点：パッチ→トークンの変換により、BERTやGPTと同一の学習パイプラインが画像にそのまま適用可能
- `ds.with_transform()`によるオンザフライ変換：前処理をインデックスアクセス時に遅延実行することで、大規模データセットでも全量をメモリに展開せずに済む設計
- 監査書類（領収書・契約書・帳票）の自動分類への応用：少量のラベル付き監査データでViTをファインチューニングすれば、書類種別の自動仕分けエージェントを低コストで構築できる

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Transfer Learning** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **Hugging Face Trainer API** (TODO: 読むべき)
- **画像パッチトークン化** (TODO: 読むべき)
- **ViTImageProcessor** (TODO: 読むべき)

## 関連記事

- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1575 ビジョントランスフォーマー（ViT）をHugging Face Optimum Graphcoreで活用する詳細ガイド
- /deep_1216 パーソナルコパイロット：自分専用コーディングアシスタントのトレーニング方法
- /deep_647 Transformersライブラリ：モデル定義の標準化とエコシステムの統合
- /deep_1579 TF ServingとKubernetesを用いたHugging Face ViTモデルのデプロイ

## 原文リンク

[🤗 TransformersでViTを画像分類にファインチューニングする](https://huggingface.co/blog/fine-tune-vit)
