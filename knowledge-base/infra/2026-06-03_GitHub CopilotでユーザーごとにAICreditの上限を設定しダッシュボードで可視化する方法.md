---
title: "GitHub CopilotでユーザーごとにAICreditの上限を設定しダッシュボードで可視化する方法"
url: "https://zenn.dev/port_inc/articles/edd7db058df9b3"
date: 2026-06-03
tags: [GitHub Copilot, GitHub Enterprise, AICredit, コスト管理, Budgets and alerts, Usage-based billing]
category: "infra"
related: [4372, 6194, 395, 6475, 5973]
memo: "[Zenn LLM] GitHub Copilotで個人単位でAICreditの制限をかけ、ダッシュボードで見れるようにする"
processed_at: "2026-06-03T21:01:37.483212"
---

## 要約

GitHub Enterprise環境においてGitHub CopilotのAICredit（AIC）消費量を個人単位で制限し、ダッシュボードから使用状況を確認できるようにする設定手順を解説した記事。

GitHub Enterpriseでは「Budgets and alerts」機能を利用して予算（Budget）を作成できる。設定手順はEnterprise管理者権限で `github.com/settings/enterprises` にアクセスし、「Billing and licensing」→「Budgets and alerts」→「New Budget」と進むことで行える。BudgetのスコープをUsersに設定することで全ユーザーに一律の上限を適用でき、特定ユーザーを選択しないことがポイント。

記事では上限値として3000AICを設定している。これはGitHub Copilot Businessの既存契約者に付与されるプロモーションクレジットが3000AICであるため、実質的なコスト超過が発生しない範囲に揃えたものである（Enterpriseプランは7000AIC）。なお使用量ベースの課金はプレビュー期間と通常期間で料金が異なるため注意が必要。

Budget設定後は「View Details」からダッシュボードでユーザーごとの消費状況を確認できるようになり、VS CodeのUI上からもMonthly Limitが表示されるようになる。これにより、従来は自作ダッシュボードで対応していたAI使用量の可視化がGitHub標準機能のみで実現できる。

ポート株式会社では半年以上前からエンジニアにGitHub Copilotを提供し、活用方法の共有も含めてAI利用を推進しているとのこと。監査AI開発への直接の示唆は薄いが、大規模エンタープライズ環境でのAIツールコスト管理・可視化の実装パターンとして参考になる。

## アイデア

- GitHubのネイティブ予算機能（Budgets and alerts）を使うことで、自作ダッシュボード不要でAIクレジット消費量を個人単位で可視化・制限できる点
- プロモーションクレジット（Business: 3000AIC、Enterprise: 7000AIC）の存在を把握し、上限値をプロモーション範囲内に設定することで追加課金を回避する設計思想
- VS CodeのUIにMonthly Limitが表示されるようになるため、管理者だけでなく開発者本人がリアルタイムで使用量を把握できるようになる点

## 前提知識

- **GitHub Enterprise** (TODO: 読むべき)
- **GitHub Copilot** → /deep_1739 8リポジトリに同じ変更を並列展開したら、Copilotレビューのばらつきがシグナルになった話
- **Usage-based billing** (TODO: 読むべき)
- **AIC（AICredit）** (TODO: 読むべき)
- **Budgets and alerts** (TODO: 読むべき)

## 関連記事

- /deep_4372 GitHub Copilotを半年間使用して得られた各種LLMモデルの所感と使い分け
- /deep_6194 急変するAIコードレビューツール市場：2026年版比較と選び方
- /deep_395 図形入りの PowerPoint を Markdown に変換する方法（GitHub Copilot + OpenXML SDK）
- /deep_6475 コードレビューを6段階にしたら、AIと人間の分業が見えた
- /deep_5973 【エンジニア必読】GitHub Copilot訴訟で学ぶ、コードと著作権の基礎

## 原文リンク

[GitHub CopilotでユーザーごとにAICreditの上限を設定しダッシュボードで可視化する方法](https://zenn.dev/port_inc/articles/edd7db058df9b3)
