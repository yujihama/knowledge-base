---
title: "Amazon S3 VectorsのMetadata Filterを使ったCognitoグループ単位の制限付きRAG実装"
url: "https://zenn.dev/fusic/articles/b772000259b74d"
date: 2026-05-25
tags: [Amazon S3 Vectors, Bedrock Knowledge Bases, RAG, metadata filter, Amazon Cognito, アクセス制御, Terraform, RetrievalFilter, Python 3.14, Cohere Embed]
category: "infra"
related: [1334, 5143, 5231, 1116, 2075]
memo: "[Zenn LLM] Amazon S3 Vectorsでacl.jsonではなくmetadata filterを選んだ制限付きRAG試してみた"
processed_at: "2026-05-25T09:07:30.283391"
---

## 要約

Amazon S3 Vectors（2025年12月GA）をAmazon Bedrock Knowledge Basesのベクトルストアとして利用し、Amazon Cognitoのグループ情報に基づいてユーザーごとに検索対象ドキュメントを制限するRAGシステムを構築した実装レポート。

acl.jsonによるアクセス制御ではなく、S3 VectorsのメタデータフィルタリングAPIを採用。ベクトル登録時に各チャンクへ `domain` フィールドをメタデータとして付与し、検索時には `{"in": {"key": "domain", "value": ["finance"]}}` 形式のRetrievalFilterをBedrock Knowledge BasesのRetrieveAndGenerateAPIに渡すことで、Cognitoグループとドキュメントドメインを1対1で対応させる。

検証データにはallganize/RAG-Evaluation-Dataset-JA（HuggingFace）を使用。finance / it / manufacturing / public / retail の5ドメインに分類された日本語RAG評価用データセットのdomain情報を活用。

検証シナリオは3つ: (1) financeグループのユーザーはfinanceドメイン文書のみ検索可能、(2) financeとit両グループに所属するマルチユーザーは両ドメインを検索可能、(3) どのグループにも属さないユーザーには403を返す。

インフラはTerraform（AWS provider ~6.46）でIaC化。モジュール構成はstorage（S3 Vectors含む）、kb（Bedrock Knowledge Bases）、api（API Gateway + Lambda）、cognito、observabilityの5モジュール。Lambda（Python 3.14ランタイム）がCognito JWTからグループ情報を抽出し、動的にRetrievalFilterを構築してBedrockに渡す設計。

埋め込みモデルはCohere Embed Multilingual v3（1024次元）、生成モデルはanthropic.claude-sonnet-4-6を使用。Cognitoの認証フローはHosted UIとJWT検証で実装。

注意点として、Cognitoグループ名・metadataのdomain値・RetrievalFilterのvalueの3者が完全一致していないと、認可は通るが検索結果が空になるトラップがある点が強調されている。

監査エージェント開発への示唆: ロール・部門・機密レベルに応じてRAGの検索範囲をメタデータフィルタで動的制御するパターンは、監査ワークフローにおける情報アクセス制御（Need-to-Know原則）の実装に直接応用可能。LangGraphのノード内でユーザーコンテキストからフィルタを生成し、Bedrock Knowledge BasesのRetrieveNodeに渡す構成が考えられる。

## アイデア

- acl.jsonではなくメタデータフィルタでアクセス制御を実装することで、ベクトル検索とアクセス制御を同一クエリで完結させ、後段フィルタリング不要なセキュアRAGを実現している点
- Cognitoグループ名・S3 Vectorsメタデータ・RetrievalFilterの3箇所の値を完全一致させる必要があるという設計上のトラップは、マルチテナントRAG実装時の典型的な落とし穴として参考になる
- LambdaでJWTのcognitoグループクレームを動的に解析してRetrievalFilterを生成するパターンは、監査AI等でロールベースの情報アクセス制御が必要なエージェントシステムに汎用的に転用できる

## 前提知識

- **Amazon S3 Vectors** (TODO: 読むべき)
- **Bedrock Knowledge Bases** → /deep_2060 「この文書たちをAIに学ばせたい」に1日で応えた話 ── Amazon Bedrock Knowledge Basesで作る社内RAG
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Amazon Cognito JWT** (TODO: 読むべき)
- **Terraform** → /deep_1428 AIがソフトウェア開発を変える——2026年、エンジニアリングの自動化最前線

## 関連記事

- /deep_1334 製造業向けRAGシステムのアクセス制御設計
- /deep_5143 エンタープライズAIのためのデータスタック再構築：統合・ガバナンス・AI対応インフラの必要性
- /deep_5231 エンタープライズAIのためのデータスタック再構築：統合・ガバナンス・AI対応インフラの必要性
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_2075 関係モデリングによるオフィスオートメーションシステムのアクセス制御フロー承認インテリジェント化

## 原文リンク

[Amazon S3 VectorsのMetadata Filterを使ったCognitoグループ単位の制限付きRAG実装](https://zenn.dev/fusic/articles/b772000259b74d)
