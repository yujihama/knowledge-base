---
title: "AWSの環境をシステムプロンプトでAIに理解させる：XML+YAMLテンプレートv2.1"
url: "https://zenn.dev/itsdaichi/articles/a802c6b2ed9817"
date: 2026-06-11
tags: [システムプロンプト設計, AWS, XML, YAML, LLM活用, Claude, IaC, SRE]
category: "infra"
related: [7112, 6953, 5843, 5165]
memo: "[Zenn LLM] AWSの環境をシステムプロンプトでAIに理解させる"
processed_at: "2026-06-11T12:11:49.246683"
---

## 要約

AWS環境の構成情報をLLM（Claude等）のシステムプロンプトとして構造化する手法を解説した記事。XML（セクション構造）とYAML（属性・変数値）を組み合わせたスキーマ（schema_version 2.1）を定義し、AIがAWSインフラを「現在運用中の環境のSource of Truth」として正確に解釈できるようにする。

主な設計要素は5つ。①`<variables>`セクションによる値の一元管理：`${var.xxx}`参照記法でリージョン・CIDR・環境名などの環境固有値を一箇所で定義し、本文中から参照する。②値の状態規約（TBD/UNVERIFIED/N/A）：未転記・未突合・対象外の3状態を明示し、AIが推測で補完せず「要確認」として扱うよう指示する。③`<task_modes>`による出力契約：review・incident・cost・change・docs・qaの6モードを定義し、各モードごとに出力フォーマット（指摘→根拠→推奨対応→優先度など）を規定する。④`<document_meta>`による鮮度管理：`last_verified`日付と`warn_after_days`（デフォルト90日）を設定し、期限超過時にAIが回答冒頭で鮮度警告を出す。⑤EC2のmiddlewareスキーマ：Apache 2.4・PHP-FPM 8.2等のversion・eol・config_path・managed_byを記述し、EOL超過・6ヶ月以内接近をレビュー時に自動指摘させる。

具体的なリソース定義としては、VPC（10.0.0.0/16）・パブリック/プライベートサブネット各2つ（AZ: ap-northeast-1a/1c）・NAT Gateway（prod環境はAZごとに1台）・ALB→ターゲットグループ→ASG/ECS→Aurora（Serverless v2、最大ACU 8）のフルスタック構成が例示されている。セキュリティグループはALB用・アプリ用・DB用の3層で、ALBからアプリへはポート8080、アプリからDBへはポート3306のみ許可するホワイトリスト設計。IaCツールにTerraformを指定した場合、AIはコンソール手作業でなくコード変更を前提とした手順を提示する。

監査エージェント開発への示唆：同様のアプローチで監査対象システムの構成情報・コントロール要件・リスク規約をシステムプロンプト化すれば、LLMが「監査環境のSource of Truth」として動作するエージェントを構築できる。TBD/UNVERIFIED規約はエビデンス確認状況の管理に、task_modesはレビュー・インシデント対応等の業務フロー別出力制御に直接転用可能。

## アイデア

- TBD/UNVERIFIED/N/Aという値の状態規約をシステムプロンプトに埋め込むことで、AIの推測補完を抑制し回答の信頼性を制御する設計パターン
- task_modesによる出力契約：ユーザーの発話トリガーキーワードからモードを自動判定し、モードごとに異なる出力フォーマットを強制する構造化プロンプト手法
- document_metaの鮮度管理機能：last_verifiedとwarn_after_daysを組み合わせ、AIが古い情報に基づく回答をする際に自律的に警告を出す仕組み

## 前提知識

- **システムプロンプト** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **AWS VPC/ALB/ECS** (TODO: 読むべき)
- **XML/YAML構造化** (TODO: 読むべき)
- **IaC (Terraform)** (TODO: 読むべき)
- **LLMコンテキスト管理** → /deep_5566 LLMコンテキスト管理徹底解剖：3つの記憶戦略で「7秒の記憶」を克服し、低コストで賢く会話を繋ぐ方法

## 関連記事

- /deep_7112 Claudeと対話しながらIT作業手順書プロンプトの標準フォーマットを設計した話
- /deep_6953 壁打ちエンジニアリング 軸①〜③（無料公開）— 前提共有・問いの粒度・答えの種類
- [コードを書けない私が、AIに「チーム」を持たせるまで](../agent-arch/2026-05-04_コードを書けない私が、AIに「チーム」を持たせるまで.md)
- /deep_5843 「LLMと一緒に学ぶWebアプリ開発」第2章：開発環境の準備（無償公開）
- /deep_5165 RFPを貼るだけでAWSアーキテクチャ設計書が出てくるSaaSを個人開発した

## 原文リンク

[AWSの環境をシステムプロンプトでAIに理解させる：XML+YAMLテンプレートv2.1](https://zenn.dev/itsdaichi/articles/a802c6b2ed9817)
