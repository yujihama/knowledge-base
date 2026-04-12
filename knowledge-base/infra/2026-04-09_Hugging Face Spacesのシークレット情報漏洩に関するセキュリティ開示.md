---
title: "Hugging Face Spacesのシークレット情報漏洩に関するセキュリティ開示"
url: "https://huggingface.co/blog/space-secrets-disclosure"
date: 2026-04-09
tags: [HuggingFace, セキュリティインシデント, シークレット管理, KMS, APIトークン, fine-grained-access-tokens, クラウドセキュリティ]
category: "infra"
memo: "[HF Blog] Space secrets security update"
processed_at: "2026-04-09T09:23:57.670253"
---

## 要約

2024年5月末、Hugging Face（HF）はSpacesプラットフォームにおいて不正アクセスが検出されたことを公表した。具体的には、Spacesに登録されたシークレット情報（APIキーやトークン等）の一部が権限なく閲覧された可能性があるというもの。HFは即座に影響を受けたHFトークンを失効（revoke）させ、対象ユーザーにメール通知を実施した。

対応措置として以下が実行された：
1. 漏洩が疑われるHFトークンの一斉失効
2. Spacesインフラからの組織トークン（org tokens）の完全削除（トレーサビリティと監査能力の向上を目的）
3. Spacesシークレット向けのKMS（Key Management Service）の導入
4. 漏洩トークンの検出・無効化システムの強化・拡充
5. 外部サイバーセキュリティフォレンジック専門家との協力調査
6. 法執行機関およびデータ保護当局への報告

HFは今後の対策として、「クラシック」な読み取り・書き込みトークンを廃止し、細粒度アクセストークン（fine-grained access tokens）への完全移行を計画している。細粒度トークンはすでに新規作成のデフォルトとなっており、機能同等性が達成され次第、旧トークン形式を完全に廃止する方針。

この事例はAIプラットフォームにおけるシークレット管理の重要性を浮き彫りにした。Spacesのような機械学習モデルホスティング・実行環境では、外部APIキー（OpenAI, AWS等）やデータベース認証情報等が環境変数として格納されることが多く、これらが漏洩した場合のリスクは甚大。KMS導入とfine-grained tokenの採用は、最小権限の原則（principle of least privilege）とシークレットライフサイクル管理の観点から標準的なベストプラクティスへの準拠を示している。

## アイデア

- fine-grained access tokenによる最小権限設計は、エージェントシステムにおけるツール別・スコープ別のAPIキー管理パターンとして応用できる
- KMS（Key Management Service）をSpacesに導入したことで、シークレットの暗号化・ローテーション・監査ログが一元管理可能になる点は、マルチテナント型AIシステムの設計参考になる
- org tokensを廃止してトレーサビリティを向上させた判断は、誰がどのリソースにアクセスしたかを追跡する監査ログ設計の重要性を示している

## Yujiの取り組みへの示唆

監査エージェントシステムを開発する上で、エージェントが外部APIやツールにアクセスする際のシークレット管理は直接的な設計課題となる。fine-grained access tokenのスコープ制限思想は、LangGraphの各ノード・ツールに最小権限のAPIキーを割り当てるアーキテクチャ設計に応用可能。また、HFのorg token廃止によるトレーサビリティ向上は、内部監査の文脈において「誰がどのエージェント操作を実行したか」を追跡するための認証・認可設計の参考となる。

## 原文リンク

[Hugging Face Spacesのシークレット情報漏洩に関するセキュリティ開示](https://huggingface.co/blog/space-secrets-disclosure)
