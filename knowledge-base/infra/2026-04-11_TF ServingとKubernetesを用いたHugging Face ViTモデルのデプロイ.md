---
title: "TF ServingとKubernetesを用いたHugging Face ViTモデルのデプロイ"
url: "https://huggingface.co/blog/deploy-tfserving-kubernetes"
date: 2026-04-11
tags: [TensorFlow Serving, Kubernetes, Docker, GKE, ViT, SavedModel, gRPC, Locust, HuggingFace, コンテナデプロイ]
category: "infra"
memo: "[HF Blog] Deploying 🤗 ViT on Kubernetes with TF Serving"
processed_at: "2026-04-11T21:09:06.063801"
---

## 要約

本記事は、Hugging Face TransformersのVision Transformer（ViT）モデルをTensorFlow Serving（TF Serving）とKubernetesを使ってスケーラブルにデプロイする手順を解説する。前回記事でローカルデプロイ済みのViTモデル（SavedModel形式、前処理・後処理を内包）をベースとし、本記事ではDockerによるコンテナ化からGoogle Kubernetes Engine（GKE）への本番デプロイまでを網羅する。

【Dockerによるコンテナ化】SavedModelは`<MODEL_NAME>/<VERSION>/`というTF Serving規定のディレクトリ構造に配置する（例: `hf-vit/1/`）。`tensorflow/serving`の公式Dockerイメージをベースに、`docker run`でコンテナを起動し、`docker cp`でモデルディレクトリをコピー後、`docker commit`で新イメージを作成する。この際、環境変数`MODEL_NAME=hf-vit`を設定することでTF Servingがデプロイ対象モデルを認識する。gRPCポート8500、HTTP/RESTポート8501で待ち受ける。AVX512等のハードウェア最適化ビルドを使うと推論速度が向上する点も言及されている。完成したイメージはGoogle Container Registry（GCR）に`gcr.io/<PROJECT_ID>/tfserving:hf-vit`形式でプッシュする。

【GKEクラスタのプロビジョニング】`gcloud container clusters create`コマンドでクラスタを作成する。設定例はクラスタ名`tfs-cluster`、ゾーン`us-central1-a`、ノード数2、マシンタイプ`n1-standard-8`。`gcloud container clusters get-credentials`でkubeconfigを更新し、`kubectl`からクラスタを操作できる状態にする。

【KubernetesマニフェストによるDeploymentとService】YAMLファイルでDeploymentリソースを定義し、GCRからプルしたコンテナイメージを使用、コンテナポート8500・8501を公開する。Serviceリソース（LoadBalancer型）を定義してクラスタ外からのアクセスを可能にし、外部IPアドレスを払い出す。`kubectl apply -f`でデプロイを実行し、`kubectl get pods`・`kubectl get svc`で状態を確認する。

【ロードテスト】Locustを使ってスケール性能を検証する。30ユーザー・毎秒1ユーザー増加という条件でHTTP/RESTエンドポイントに対してテストを実施し、レイテンシ・スループットを計測する。結果として2ノード構成でも安定したサービングが確認できている。また、`kubectl scale deployment`コマンドでレプリカ数を動的に変更可能であり、KubernetesのHorizontal Pod Autoscaler（HPA）による自動スケーリングも適用できる。

全体として、SageMakerやVertex AIのようなマネージドMLプラットフォームに依存せず、汎用的なDocker+Kubernetes構成でMLモデルを運用する際の標準的なワークフローを提示している。

## アイデア

- SavedModel内に前処理・後処理を埋め込むことでサービング側のコードを最小化できる設計パターンは、監査エージェントのモデルAPIサービング時にも同様に適用できる
- AVX512最適化ビルドのTF Servingイメージを使うことで、GPUなし環境でも推論スループットを改善できる点は、コスト効率重視のオンプレ・クラウド混在構成で有用
- Locustによるロードテストとkubectl scaleの組み合わせで、実際の負荷に応じたレプリカ数チューニングを定量的に行えるワークフローが確立されている

## Yujiの取り組みへの示唆

監査エージェントをLangGraphで構築する際、推論APIをTF Serving＋Kubernetesで提供する構成は、エージェントのツール呼び出し先として本番運用に耐えうるスケーラブルなエンドポイントを整備する際の参考になる。特にSavedModelに前処理を内包するパターンは、LangGraphのノード設計でツール側の入力変換ロジックを削減する観点から応用できる。ローカルLLMインフラ（RTX 3090）でOllamaを使う場合でも、TF ServingのKubernetes構成と比較することでサービング設計の引き出しが広がる。

## 原文リンク

[TF ServingとKubernetesを用いたHugging Face ViTモデルのデプロイ](https://huggingface.co/blog/deploy-tfserving-kubernetes)
