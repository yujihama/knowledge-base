---
title: "AWSアカウントでHugging Face Enterprise Hubを購読する方法"
url: "https://huggingface.co/blog/enterprise-hub-aws-marketplace"
date: 2026-04-09
tags: [Hugging Face, Enterprise Hub, AWS Marketplace, SSO, 監査ログ, GDPR, SOC2, DGX Cloud, NVIDIA H100]
category: "infra"
memo: "[HF Blog] Subscribe to Enterprise Hub with your AWS Account"
processed_at: "2026-04-09T09:47:34.025855"
---

## 要約

Hugging FaceはOrganizationアカウントをEnterprise Hubにアップグレードする際、AWSアカウントによる支払いに対応した。これにより企業はAWS Marketplaceを通じてHugging Face Enterprise Hubのサブスクリプションを管理・決済できる。

【Enterprise Hubの主要機能】Enterprise HubはGDPR準拠・SOC2 Type 2認証を受けたプラットフォーム上で、シングルサインオン（SSO）、リソースグループによるアクセス制御、ストレージリージョン選択（欧州でのデータ保存）、監査ログ、高性能GPU（NVIDIA H100）へのアクセス、プライベートデータセットビューア、DGX Cloudでのノーコード学習などの機能を提供する。

【AWS連携の手順】まずAWS MarketplaceでHugging Face Platformのオファーを購読し、「Set up your account」ボタンからHugging FaceプラットフォームへリダイレクトされてOrganizationアカウントを紐付ける。連携後はステータスがsubscribe-pendingからsubscribe-successに変わり、AWSとHugging Faceの両方から確認メールが届く。その後、OrganizationのBilling設定からEnterprise Hubタブでシート数と課金頻度を選択して有効化する。

【価格体系】AWS Marketplace経由の価格はHugging Face公式サイトと同一で、差額や手数料は発生しない。ただし決済はAWSアカウントに統合されるため、企業の既存AWSコスト管理フローや請求統合の恩恵を受けられる。

【対象ユーザーの要件】接続にはOrganizationアカウント（個人アカウント不可）、admin権限、メール確認済みアカウントが必要。AWS側でもMarketplace購読権限を持つアクティブなアカウントが必要。

## アイデア

- AWSの既存請求・コスト管理インフラ（Cost Explorer、タグ付け、組織単位の予算管理）をAI基盤サービスに統合できる点が企業導入障壁を大幅に下げる
- 監査ログ機能とリソースグループによるアクセス制御の組み合わせで、大規模組織でのモデル・データセットへのアクセス追跡が可能になる
- ストレージリージョン選択（欧州）はGDPR対応に直結し、個人データを含む学習データの地理的制約を満たす実用的な仕組みとして注目に値する
## 関連記事

- /deep_989 Hugging FaceとNVIDIA NIMによるサーバーレス推論（DGX Cloud連携）
- /deep_1215 Hugging Face Hubにストレージリージョン機能を導入
- /deep_1310 複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1434 生成AIワークロードの電力プロファイル計測：データセンター全体インフラ計画のための手法

## 原文リンク

[AWSアカウントでHugging Face Enterprise Hubを購読する方法](https://huggingface.co/blog/enterprise-hub-aws-marketplace)
