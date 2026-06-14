---
title: "LLMOps学習でBedrock + Claudeを動かしてみた"
url: "https://zenn.dev/yukika/articles/20260613_bedrock_claude_first_step"
date: 2026-06-14
tags: [AWS Bedrock, Claude Haiku, Converse API, boto3, LLMOps, 推論プロファイル, temperature, トークンコスト, IAM認証]
category: "infra"
related: [5262, 2060, 4747, 6194, 5211]
memo: "[Zenn LLM] LLMOps学習でBedrock + Claudeを動かしてみた"
processed_at: "2026-06-14T09:02:22.086569"
---

## 要約

AWS BedrockのConverse APIを使ってClaude（Haiku 4.5）をPythonスクリプトから呼び出す手順を検証した記事。BedrockではモデルカタログのモデルIDをそのまま使うのではなく、推論プロファイル（inference profile）のIDが必要で、東京リージョンでは`jp.anthropic.claude-haiku-4-5-20251001-v1:0`を指定する必要がある。Bedrock経由のメリットとして、Anthropic APIキー不要でIAM認証を利用できる点が強調されており、aws-vaultと組み合わせて認証情報をコードに埋め込まずに実行できる。

技術的な検証として、言語別トークン数の違いを計測。同内容で日本語は入力27/出力59トークンに対し、英語は入力22/出力31トークンとなり、日本語は出力が約1.9倍のトークンを消費する。Haiku 4.5東京リージョンの料金（入力$1.00/出力$5.00 per 1Mトークン）を元にコスト計算すると、日本語1リクエストあたり$0.000322（約0.05円）。

temperatureパラメータの挙動検証では、temperature=0.0では2回連続で完全に同一の応答が返り、temperature=1.0では表現・書式ともに異なる応答が返ることを確認。温度低：分類・抽出・判定用途、温度高：文章生成・アイデア出し用途という使い分けを整理している。

エラーとして2点記録：①モデルIDにカタログIDを使うとValidationExceptionが発生し、推論プロファイルIDに変更が必要、②`temperature`と`top_p`を同時指定するとValidationExceptionが発生し、Anthropicは両者の同時指定を非推奨としているため一方のみ使用する必要がある。

監査エージェント開発への示唆：BedrockのIAM統合により組織内クレデンシャル管理が一元化でき、監査ログとIAMポリシーを組み合わせたアクセス制御の実装が容易になる。temperature=0での再現性保証は、判定・分類処理を含む監査エージェントの出力安定性確保に直接適用できる。次ステップとしてツール（検索等）を持つ小さなエージェントの構築が予定されており、LangGraphやReActパターンへの展開の足がかりとなる内容。

## アイデア

- 日本語は英語の約1.9倍の出力トークンを消費するため、日本語中心サービスではコスト見積もりに言語係数を掛ける必要がある
- BedrockのIAM認証統合により、APIキー管理不要でエンタープライズのクレデンシャル管理基盤をそのまま流用できる
- temperature=0での完全再現性は監査・分類・判定タスクの品質保証に直結し、テスタビリティを大幅に向上させる

## 前提知識

- **AWS Bedrock** → /deep_3509 Strands Agents SDK入門：3行で始めるAIエージェント開発と他フレームワーク比較
- **Converse API** → /deep_7227 Amazon Bedrock 経由で使える LLM の日本語ベンチマーク性能比較
- **boto3** → /deep_2060 「この文書たちをAIに学ばせたい」に1日で応えた話 ── Amazon Bedrock Knowledge Basesで作る社内RAG
- **inference profile** (TODO: 読むべき)
- **temperature** → /deep_5211 同じプロンプトなのに毎回答えが変わる——LLMの非決定性という落とし穴

## 関連記事

- /deep_5262 【Reincarnation Engineering】忘却のAI工学 ― Part1.実践編
- /deep_2060 「この文書たちをAIに学ばせたい」に1日で応えた話 ── Amazon Bedrock Knowledge Basesで作る社内RAG
- /deep_4747 源内（デジタル庁ガバメントAI）OSS版を技術解剖 — AWS/Azure/GCP 3クラウド対応の行政RAG基盤
- /deep_6194 急変するAIコードレビューツール市場：2026年版比較と選び方
- /deep_5211 同じプロンプトなのに毎回答えが変わる——LLMの非決定性という落とし穴

## 原文リンク

[LLMOps学習でBedrock + Claudeを動かしてみた](https://zenn.dev/yukika/articles/20260613_bedrock_claude_first_step)
