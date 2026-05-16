---
title: "Google Cloud上でサーバーレスTransformersパイプラインを構築した記録"
url: "https://huggingface.co/blog/how-to-deploy-a-pipeline-to-google-clouds"
date: 2026-04-14
tags: [HuggingFace, Transformers, Google Cloud Run, Docker, DistilBERT, sentiment-analysis, Flask, gunicorn, serverless, PyTorch]
category: "infra"
related: [1761, 1448, 26, 1529, 1760]
memo: "[HF Blog] My Journey to a serverless transformers pipeline on Google Cloud"
processed_at: "2026-04-14T12:51:02.205324"
---

## 要約

本記事は、HuggingFaceコミュニティメンバーのMaxence Dominiciが、DiscordのカスタマーレビューをポジティブかNegativeかで自動分類するマイクロサービスをGoogle Cloud上に構築した実践記録である。月間リクエスト数が2,000件程度を想定し、スケーラビリティより手軽さを優先した設計となっている。

モデルはDistilBERT base uncased finetuned SST-2（distilbert-base-uncased-finetuned-sst-2-english）を採用し、HuggingFaceのTransformersライブラリのpipeline APIを通じて推論を実行する。

デプロイ先の選定にあたり、著者は3つのGCPサービスを試行した。まずAI-Platform Predictionは、モデルがKerasの純粋なSavedModel形式ではなくチェックポイント形式であるため適合せず、ベータ版の不安定さも問題となった。次にApp Engineを試したが、TensorFlowはシステム依存ファイルの欠如でインストール失敗。PyTorchはF4_1Gインスタンスで動作したものの、同一インスタンスで同時2リクエストが限界という制約があった。最終的にCloud Runを選択し、Dockerイメージとして配布することで高メモリ（4GB）・複数vCPUの割り当てが可能になった。

実装構成は4要素からなる。①Flask製のmain.pyはGETリクエストでreviewとapi_keyパラメータを受け取り、簡易APIキー認証後にpipelineを起動して結果を返す。②Dockerfileはpython:3.7ベースイメージを使用し、gunicornをエントリーポイントとして--workers 1 --threads 1で起動する。ワーカーを1に絞るのは同時2インスタンス起動によるコスト増大を防ぐため、スレッドを1に絞るのは4GBメモリをモデルロードに専有させるためである（スレッド数を増やすとメモリ不足でエラーになる）。③モデルディレクトリにはpytorch_model.bin、config.json、vocab.txtを配置する。④requirements.txtにはFlask==1.1.2、torch===1.7.1、transformers~=4.2.0、gunicorn>=20.0.0を指定する。

デプロイはgcloud CLIで2コマンドにて完了する（gcloud builds submitでイメージをContainer Registryへプッシュ、gcloud run deployでCloud Runへデプロイ）。デプロイ後はCloud Runのデフォルト256MBから4GBへメモリを手動で引き上げる必要がある。

監査エージェント開発への示唆としては、軽量分類モデル（DistilBERT）をサーバーレス環境でゼロスケール運用するパターンが参考になる。モデルをコンテナに同梱してステートレスに推論するアーキテクチャは、監査ログの自動分類やリスク判定マイクロサービスにも直接応用可能である。

## アイデア

- モデルをDockerイメージに同梱することで外部ストレージ依存を排除し、コールドスタート時の複雑性を削減できる点
- gunicornのworker/thread数をメモリ制約から逆算して決定するアプローチ（4GB÷スレッド数でモデルロード可否を判断）
- AI-Platform Prediction→App Engine→Cloud Runと3サービスを試行した失敗の記録が、GCPでのMLデプロイ選定基準として実践的な判断材料になる点

## 前提知識

- **Transformers pipeline API** (TODO: 読むべき)
- **DistilBERT** → /deep_705 Transformerベースのソースコード表現を用いた並列化可能ループの自動識別
- **Docker** → /deep_584 ScreenSuite - GUIエージェント向け最も包括的な評価スイート
- **Cloud Run** → /deep_408 Google Cloud の GPU 付き Cloud Run で Ollama + ローカル LLM を動かす
- **gunicorn** (TODO: 読むべき)

## 関連記事

- /deep_1761 PythonによるSentiment Analysis入門：事前学習モデルの活用からファインチューニングまで
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新
- /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする

## 原文リンク

[Google Cloud上でサーバーレスTransformersパイプラインを構築した記録](https://huggingface.co/blog/how-to-deploy-a-pipeline-to-google-clouds)
