---
title: "Claude CoworkをAmazon Bedrock経由で使ってみた"
url: "https://zenn.dev/fusic/articles/7ac5229f4d65f0"
date: 2026-05-11
tags: [Amazon Bedrock, Claude Desktop, Claude Cowork, クロスリージョン推論, claude-sonnet-4-6, AWS, サードパーティ推論]
category: "infra"
related: [2140, 4815, 2208, 3851, 3881]
memo: "[Zenn LLM] Claude CoworkをAmazon Bedrock 経由で使ってみた"
processed_at: "2026-05-11T09:41:09.821479"
---

## 要約

AnthropicのデスクトップチャットアプリClaude Desktopで、推論バックエンドにAmazon Bedrockを利用できる「Claude Cowork in Amazon Bedrock」が発表された。Claude CodeがCLIベースでエンジニア向けであるのに対し、Claude CoworkはチャットUIベースで非エンジニアでも扱いやすい点が特徴。本記事はmacOS環境でClaude DesktopにAmazon Bedrockを設定する手順を検証したものである。

設定手順は3ステップで構成される。Step 1では、Amazon BedrockのAPIキーを取得する。短期キーと長期キーがあり、今回は短期キーを使用。Step 2では、Claude Desktopの「ヘルプ→トラブルシューティング→開発者モードを有効にする」から開発者モードをオンにし、再起動後に「開発→サードパーティ推論を設定...」を選択する。Step 3では、AWS regionに「ap-northeast-1」（東京）、取得したAPIキーをAWS bearer tokenに設定し、モデルIDに日本リージョン間クロスリージョン推論プロファイルID「jp.anthropic.claude-sonnet-4-6」を入力する。「ローカルに適用」を押して再起動すると設定が完了する。

設定完了後は画面に「Cowork 3P・Bedrock」の表示が出現し、Amazon Bedrock経由でClaude Sonnet 4.6の応答が得られることを確認した。Amazon Bedrock経由で利用することの利点として、AWSの一括請求・Cost Explorerによるコスト管理の統合、および東京・大阪リージョンへのデータローカライズが挙げられる。

監査エージェント開発への示唆として、Claude DesktopをBedrockバックエンドで運用する構成は、エンタープライズ環境での統制要件（データ所在地・コスト可視化・請求一元化）を満たしやすく、非エンジニアの内部監査担当者がAIを活用する際のフロントエンドとして有力な選択肢となり得る。

## アイデア

- Claude DesktopがサードパーティLLMバックエンドとして任意のAmazon Bedrockエンドポイントを受け入れる「サードパーティ推論」機能を持っており、UIはそのままでバックエンドを差し替えられる設計になっている点
- 日本リージョン間クロスリージョン推論プロファイル（jp.anthropic.claude-sonnet-4-6）を利用することで、データを東京・大阪リージョン内に閉じながら高可用性を得られる構成が可能な点
- 非エンジニア向けのClaude Cowork（チャットUI）とエンジニア向けのClaude Code（CLI）という同一ブランド内での役割分担が明確化されており、組織内の異なるユーザー層への展開戦略として参考になる点

## 前提知識

- **Amazon Bedrock** → /deep_2247 AI for Science の歩き方 #8 ― 分野別の事例と失敗から学ぶ教訓
- **Claude Desktop** → /deep_4742 MCP（Model Context Protocol）実践入門──LLMを外部ツールとつなぐ標準規格を自分で実装する【2026】
- **推論プロファイル** (TODO: 読むべき)
- **AWS IAM** (TODO: 読むべき)
- **クロスリージョン推論** (TODO: 読むべき)

## 関連記事

- /deep_2140 メルカリのClaude Codeセキュリティ設定を参考に、金融機関向けの方針を考えた
- /deep_4815 フリーミアムAIアプリのマネタイズ設計 ― Qwen3 80B無料×Claude Sonnet有料の二層構造と損益分岐の数学
- /deep_2208 スクショ→AI分析アプリの全体設計：iOS MVVM + AWSサーバーレスで恋愛分析AIアプリを作る
- /deep_3851 エージェントオーケストレーション：今AIで重要な10のこと
- /deep_3881 エージェントオーケストレーション：AIが本当に世界を変えるための10の重要事項

## 原文リンク

[Claude CoworkをAmazon Bedrock経由で使ってみた](https://zenn.dev/fusic/articles/7ac5229f4d65f0)
