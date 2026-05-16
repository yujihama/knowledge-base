---
title: "SageMaker Training Jobを使う理由を整理しつつ、Terraformで試してみた"
url: "https://zenn.dev/fusic/articles/f48b25bf83a58f"
date: 2026-04-17
tags: [SageMaker, Training Job, Terraform, AWS, PyTorch, IAM, S3, 機械学習インフラ, MNIST, CNN]
category: "infra"
related: [1882, 1619, 1446, 1879, 1791]
memo: "[Zenn 機械学習] SageMaker Training Jobを使う理由を整理しつつ、Terraformで試してみた"
processed_at: "2026-04-17T12:13:12.782079"
---

## 要約

本記事は、AWSのSageMaker Training Jobをテーマに、Terraformによるインフラ構築からPyTorch CNNモデルの学習実行までをハンズオン形式で解説したものである。SageMaker Training JobはAWSのマネージド機械学習実行サービスで、指定したCPU/GPUインスタンスを学習時のみ自動起動・停止する従量課金モデルを採用している。これにより、Notebookインスタンスの削除忘れによる意図しない課金リスクを回避できる点が強調されている。また、.ipynbファイルはGit差分が見づらくコードレビューに不向きであるため、学習コードを通常の.pyスクリプトとして管理できる点もTraining Job採用の理由として挙げられている。インフラ構成はTerraform（v1.5以上、AWSプロバイダv6系）で管理され、S3バケット（AES256暗号化・パブリックアクセスブロック設定済み）とIAMロール（S3・CloudWatch Logs・ECRへのアクセス権限付与）を定義する。学習データにはKaggle Digit RecognizerコンペのMNISTデータセットを使用し、Kaggle CLIでダウンロード後にboto3経由でS3にアップロードする。学習スクリプトはPyTorchで実装したCNNで、SageMaker環境変数（SM_CHANNEL_TRAIN、SM_MODEL_DIR等）経由でデータパスを受け取る設計となっている。Training JobはSageMaker Python SDKのPyTorchEstimatorを用いてml.c5.xlargeインスタンス上で起動し、学習済みモデルはtar.gz形式でS3に自動保存される。最後にS3からモデルをダウンロードしてローカルで推論テストを行い、精度確認まで完結させる構成となっている。検証後はterraform destroyで全リソースを一括削除できる設計になっており、コスト管理の観点でも実用的な構成といえる。監査エージェント開発においても、バッチ的な推論・学習タスクをSageMaker Training Jobとして切り出すことで、コスト効率の高いGPUリソース活用が可能になる示唆がある。

## アイデア

- Notebookインスタンスとの比較でTraining Jobを選ぶ判断軸（コスト管理・コードレビュー適性）が明確に整理されており、MLOpsの実務判断フレームとして再利用できる
- TerraformでIAMポリシーをS3・CloudWatch Logs・ECRに分割定義することで最小権限原則を実現しつつ、検証後にterraform destroyで一括削除できる設計が学習コストと運用コストのバランスを保っている
- SageMaker環境変数（SM_CHANNEL_*、SM_MODEL_DIR）を介したデータパス管理により、学習スクリプトをローカル実行とクラウド実行で同一コードのまま切り替えられる移植性の高い設計になっている

## 前提知識

- **SageMaker Training Job** (TODO: 読むべき)
- **Terraform** → /deep_1428 AIがソフトウェア開発を変える——2026年、エンジニアリングの自動化最前線
- **IAM Role / Policy** (TODO: 読むべき)
- **PyTorch CNN** (TODO: 読むべき)
- **boto3 / S3** (TODO: 読むべき)

## 関連記事

- /deep_1882 Amazon SageMakerとHugging Faceのパートナーシップ：NLPモデルのトレーニングと推論を簡略化
- /deep_1619 敵対的データを用いた動的モデル訓練の方法（MNISTを例に）
- /deep_1446 Hugging FaceとAWSが提携：AIの民主化に向けた戦略的パートナーシップ
- /deep_1879 🤗 Accelerate 紹介：あらゆるデバイスでPyTorchトレーニングスクリプトをそのまま実行
- /deep_1791 金融系データサイエンティストがAWS11冠を通して見えたこと

## 原文リンク

[SageMaker Training Jobを使う理由を整理しつつ、Terraformで試してみた](https://zenn.dev/fusic/articles/f48b25bf83a58f)
