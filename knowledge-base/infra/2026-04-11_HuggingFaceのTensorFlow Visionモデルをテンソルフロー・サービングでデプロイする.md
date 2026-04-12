---
title: "HuggingFaceのTensorFlow Visionモデルをテンソルフロー・サービングでデプロイする"
url: "https://huggingface.co/blog/tf-serving-vision"
date: 2026-04-11
tags: [TensorFlow Serving, ViT, SavedModel, HuggingFace Transformers, REST API, gRPC, Docker, TFViTForImageClassification, model deployment]
category: "infra"
memo: "[HF Blog] Deploying TensorFlow Vision Models in Hugging Face with TF Serving"
related: [1579, 1574, 1264, 1575, 878]
processed_at: "2026-04-11T21:29:17.382630"
---

## 要約

本記事は、HuggingFace TransformersのTensorFlow実装であるVision Transformer（ViT、google/vit-base-patch16-224）をTensorFlow Serving（TF Serving）を使ってローカルにデプロイする手順を解説している。TF ServingはRESTおよびgRPCエンドポイントとしてモデルを公開でき、モデルウォームアップやサーバーサイドバッチング等の本番向け機能をすぐに利用できる。

デプロイの主要ステップは以下の通り。①`save_pretrained(saved_model=True)`でViTモデルをSavedModel形式にシリアライズ。デフォルトでバージョンディレクトリ（`vit/saved_model/1`）が作成される。②`saved_model_cli`で入力シグネチャを確認すると、入力は`pixel_values`（shape: [-1,-1,-1,-1]のfloat32）、出力は1000次元の`logits`。③「モデルサージェリー」として前処理（ピクセル値を[0,1]にスケール→mean/std=0.5で[-1,1]に正規化→224×224にリサイズ→チャネルファースト変換）と後処理（ArgMaxによるラベル選択、Softmaxによる確信度計算）をSavedModelの計算グラフに埋め込む。REST/gRPCリクエスト時のペイロード削減のため、画像はbase64エンコードした文字列として受け取り、サーバー側でデコードする設計としている。④`tf.saved_model.save()`でシグネチャを`serving_default`に紐付けてエクスポートし、`MODEL_DIR`環境変数を設定。⑤Dockerで`tensorflow/serving`イメージを起動し、REST（ポート8501）またはgRPC（ポート8500）でリクエストを受け付ける。⑥Pythonクライアントから画像をbase64エンコードしてJSONペイロードを作成し、`requests.post()`でREST推論を実行。レスポンスは`{"label": "...", "confidence": 0.xx}`形式。

この手法の核心は、前処理・後処理をモデルグラフ内に内包させることで「学習時と推論時のスキュー（training-serving skew）」を防止し、クライアント側の実装を簡素化する点にある。ImageNet-1kの1000クラス分類ラベルもモデル設定（`model.config.id2label`）から直接グラフに埋め込まれる。

## アイデア

- 前処理・後処理をSavedModelグラフに埋め込む「モデルサージェリー」パターンにより、クライアントは生画像（base64）を送るだけで推論結果を受け取れる設計が、training-serving skewを構造的に防止する
- tf.functionとconcrete_functionを組み合わせてサービングシグネチャを上書きする手法は、任意のPythonロジック（前処理・ラベルマッピング等）をTensorFlowグラフとして固定化できる汎用テクニック
- TF ServingはgRPCとRESTの両プロトコルをネイティブサポートし、サーバーサイドバッチングやモデルウォームアップを設定ファイルのみで有効化できるため、高スループット推論基盤を低コストで構築できる
## 関連記事

- /deep_1579 TF ServingとKubernetesを用いたHugging Face ViTモデルのデプロイ
- /deep_1574 HuggingFace ViTモデルをVertex AIにデプロイする
- /deep_1264 本番環境でのLLM最適化：低精度・Flash Attention・アーキテクチャ革新
- /deep_1575 ビジョントランスフォーマー（ViT）をHugging Face Optimum Graphcoreで活用する詳細ガイド
- /deep_878 データフリー共分散推定によるモデルマージ

## 原文リンク

[HuggingFaceのTensorFlow Visionモデルをテンソルフロー・サービングでデプロイする](https://huggingface.co/blog/tf-serving-vision)
