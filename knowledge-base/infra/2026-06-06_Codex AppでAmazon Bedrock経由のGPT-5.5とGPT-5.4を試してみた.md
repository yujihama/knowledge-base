---
title: "Codex AppでAmazon Bedrock経由のGPT-5.5とGPT-5.4を試してみた"
url: "https://zenn.dev/fusic/articles/75c7b795429091"
date: 2026-06-06
tags: [Amazon Bedrock, Codex App, GPT-5.5, GPT-5.4, Bedrock Mantle, IAM, AWS CLI, OpenAI]
category: "infra"
related: [6201, 140, 6802, 5033, 2920]
memo: "[Zenn LLM] Codex AppでAmazon Bedrock経由のGPT5.5 とGPT5.4 試してみた"
processed_at: "2026-06-06T21:17:00.324222"
---

## 要約

2026年6月にOpenAIのGPT-5.5およびGPT-5.4がAmazon Bedrockで一般提供開始された。本記事はOpenAIのコーディングエージェントアプリ「Codex App」をAmazon Bedrock経由で動作させる手順を解説している。

通常Codex AppはOpenAI APIキーまたはChatGPTサインインで利用するが、Amazon Bedrock経由に切り替えることでAWSの認証情報・請求・アクセス制御に統合できる。内部的には「Bedrock Mantle」と呼ばれるAPIレイヤーを経由しており、従来のClaude Code on Bedrockで使用するbedrock:InvokeModelではなく、bedrock-mantle:CreateInferenceアクションが必要になる点が重要な差異となる。

手順は大きく3ステップで構成される。Step 1ではAWS CLIでプロファイルログインし、sts get-caller-identityで認証確認。Step 2ではbedrock-mantle:CreateInference、bedrock-mantle:GetProject、bedrock-mantle:ListProjects、bedrock-mantle:ListTagsForResourcesの4アクションを許可するカスタムIAMポリシー「CodexBedrockMantleInference」をJSONで定義しcreate-policyで作成。AWS管理ポリシーAmazonBedrockMantleInferenceAccessを使う方法もあるが、権限の可視性のためカスタムポリシーが推奨されている。Step 3では専用IAMユーザー「codex-bedrock-user」を作成し、当該ポリシーをアタッチする。

設定面では~/.codex/config.tomlにmodel_provider="amazon-bedrock"、model="openai.gpt-5.5"を指定し、aws.profileとaws.region（us-east-2）を記述する。Codex App再起動後にモデル選択メニューがGPT-5.4-MiniやGPT-5.3-Codex-SparkからGPT-5.5とGPT-5.4に切り替わることで動作を確認できる。

AWSをすでに利用している組織にとって、生成AIの利用料をAWS請求に一元化でき、IAMによる細かなアクセス制御も適用可能になる構成として実用的な選択肢となる。監査エージェント開発の観点では、AWSインフラ上でIAMポリシーによりAIツールのアクセス範囲を厳密に制御するパターンは、エンタープライズ環境でのガバナンス実装として参考になる。

## アイデア

- Bedrock Mantleという中間レイヤーがOpenAIモデルをAWSエコシステムに統合しており、bedrock:InvokeModelとは別の新たなIAMアクション体系（bedrock-mantle:*）が導入されている点が新しい設計パターン
- Codex AppのプロバイダーをAmazon Bedrockに切り替えるだけで利用可能モデルが変わる（GPT-5.4-Mini→GPT-5.5等）という、config.toml1ファイルによるマルチプロバイダー対応の柔軟なアーキテクチャ
- AIコーディングエージェントのアクセス制御をIAMポリシーで管理することで、組織のガバナンス・コンプライアンス要件（監査ログ、最小権限原則）をAWS標準の仕組みのみで実現できる

## 前提知識

- **Amazon Bedrock** → /deep_2247 AI for Science の歩き方 #8 ― 分野別の事例と失敗から学ぶ教訓
- **IAM ポリシー** (TODO: 読むべき)
- **AWS CLI** (TODO: 読むべき)
- **Codex App** → /deep_5033 Codex appを使ってみた。CLIより「作業の見通し」が良くてけっこう好きだった
- **OpenAI Responses API** → /deep_5211 同じプロンプトなのに毎回答えが変わる——LLMの非決定性という落とし穴

## 関連記事

- /deep_6201 GPT-5.5 で「ステップ・バイ・ステップで考えて」が効かなくなる場面？OpenAI 公式の新プロンプト構造を実例で読み解く
- /deep_140 GPT-5.4 miniとnanoの紹介
- /deep_6802 Codex が SKILL.md を 220 行で切る原因は、Codex 自身の prompt の 1 行だった
- /deep_5033 Codex appを使ってみた。CLIより「作業の見通し」が良くてけっこう好きだった
- /deep_2920 見て・指して・磨く：視覚フィードバックを用いたGUI接地のマルチターンアプローチ

## 原文リンク

[Codex AppでAmazon Bedrock経由のGPT-5.5とGPT-5.4を試してみた](https://zenn.dev/fusic/articles/75c7b795429091)
