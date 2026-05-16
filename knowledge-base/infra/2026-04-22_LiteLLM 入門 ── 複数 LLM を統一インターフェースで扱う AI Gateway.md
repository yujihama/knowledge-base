---
title: "LiteLLM 入門 ── 複数 LLM を統一インターフェースで扱う AI Gateway"
url: "https://zenn.dev/activecore/articles/5ed3d42eda81ae"
date: 2026-04-22
tags: [LiteLLM, AI Gateway, LLMOps, Proxy Server, バーチャルキー, Bedrock Guardrails, OpenAI互換, コスト管理, PII, フォールバック]
category: "infra"
related: [2103, 2404, 827, 1427]
memo: "[Zenn LLM] LiteLLM 入門 ── 複数 LLM を統一インターフェースで扱う AI Gateway"
processed_at: "2026-04-22T12:10:10.620309"
---

## 要約

複数のLLMプロバイダー（OpenAI, Anthropic, AWS Bedrock, Ollamaなど）を個別のSDKで直接呼び出す構造は、プロバイダーが増えるにつれてSDK乱立・モデル切り替えコスト・コスト不可視・APIキー管理リスク・障害時の手動対応という5つの構造的問題を生む。LiteLLMはこれをオープンソースのAI Gatewayとして解消するツールで、100以上のLLMプロバイダーをOpenAI互換の統一インターフェースでラップする。

利用形態は2種類ある。Python SDKはアプリに直接組み込み、`litellm.completion()`でプロバイダー差異を吸収する。Proxy Server（AI Gateway）はHTTPサーバーとして立ち上げ、複数アプリからのリクエストを集約管理する。特に複数チーム・複数アプリが存在する組織ではProxy Server形態が推奨される。

Proxy Serverの主要機能は4つ。①コスト・使用量追跡：どのチーム・アプリがどのモデルをどれだけ使ったかをトークン数・コストで集約し、予算上限（Budget）設定とアラートも可能。②ロードバランシング・フォールバック：複数プロバイダーへのリクエスト分散と、障害・レート制限時の自動切り替えをアプリ側実装なしで実現。③バーチャルキー管理：チーム・用途ごとに仮想APIキーを発行し、利用モデル・予算・有効期限を個別設定。本物のプロバイダーキーはGatewayのみが保持する。④ログ・可観測性：Langfuse・Datadogなど外部サービスへのログ転送をサポート。

セキュリティ面ではAWS Bedrock Guardrailsとの連携が可能。PII（個人情報）フィルタリングは氏名・電話番号・メールアドレスなど汎用カテゴリに加え、金融（クレジットカード番号、IBAN等）、IT（IPアドレス、AWSアクセスキー等）、国別識別子（SSN、NHS番号等）を含む31種類を事前定義。正規表現によるカスタムパターン追加も可能。プロンプトインジェクション・ジェイルブレイク検知もGatewayレベルで一括対応でき、アプリごとの個別実装が不要になる。実行タイミングはpre_call/during_call/post_callから選択可能。

LLMOpsの観点では、モニタリング/オブザーバビリティ・デプロイ/バージョニング・セーフティ/ガバナンスの3領域をカバーし、評価やプロンプトマネジメントはLangfuse等と組み合わせてスタックを構成する。監査エージェント開発への示唆として、複数LLMを使い分けるマルチエージェント構成においてコスト管理・セキュリティ統制・フォールバックをGateway層に集約できる点は、本番運用設計で直接活用できるアーキテクチャパターンである。

## アイデア

- 「どのプロバイダーを使うか」をコードの構造ではなく設定の問題に変えるという設計思想：モデル切り替えがビジネス判断として扱えるようになる点は、LLMを多用するエージェントシステムの運用設計で本質的な価値を持つ
- バーチャルキーによるセキュリティ局所化：本物のプロバイダーキーをGateway一箇所に集約し、各アプリには用途別の仮想キーのみを渡す設計は、最小権限原則をLLM運用に適用した具体的な実装パターン
- Bedrock Guardrailsとのpre_call/during_call/post_call連携：アプリ側コード変更なしにPIIマスキングやプロンプトインジェクション防御をGatewayレベルで一括適用できる構造は、監査・コンプライアンス要件への対応を横断的に担保する手段になる

## 前提知識

- **OpenAI API** → /deep_137 DescriptがOpenAI APIを使って多言語動画吹き替えをスケールさせる仕組み
- **REST API / HTTP** (TODO: 読むべき)
- **APIキー管理** (TODO: 読むべき)
- **LLMOps** (TODO: 読むべき)
- **AWS Bedrock** (TODO: 読むべき)

## 関連記事

- /deep_2103 製造業RAG運用編：監査ログ + イベント駆動再インデックスを実装する
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_827 smolagentsの紹介：コードでアクションを記述するシンプルなエージェントライブラリ
- /deep_1427 Claude Code CLIをGLM/MiniMaxで代替した話（コスト大幅削減の実測）

## 原文リンク

[LiteLLM 入門 ── 複数 LLM を統一インターフェースで扱う AI Gateway](https://zenn.dev/activecore/articles/5ed3d42eda81ae)
