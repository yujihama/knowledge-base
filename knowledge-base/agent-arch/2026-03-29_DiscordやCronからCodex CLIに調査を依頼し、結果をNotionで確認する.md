---
title: "DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する"
url: "https://zenn.dev/kazami/articles/discord-agent-bot-20260328"
date: 2026-03-29
tags: [Codex CLI, Discord Bot, Notion, Vercel, RSS, Feedly, Cron, 自動化パイプライン, LLMオーケストレーション]
category: "agent-arch"
memo: "[Zenn LLM] DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する"
processed_at: "2026-03-29T22:07:42.096642"
---

## 要約

VPS上でCodex CLIを実行し、DiscordまたはCronジョブからタスクを投入して調査・要約を行い、結果をNotionに保存、VercelでRSS配信、FeedlyでFeed管理するパイプラインの構築事例。既存のOpenAI API従量課金型のTelegram要約基盤から移行し、ChatGPTサブスク固定費化によるコスト削減を実現。要約結果の保存先としてSupabase（公開範囲制御の複雑さ）よりもNotion（非公開ページ管理がシンプル）を採用。DiscordはタスクIN/通知OUT、NotionはストレージとRSS情報管理、VercelはRSSエンドポイント、FeedlyはFeed購読・未読管理と役割を明確に分担する設計。

## 要点

- Codex CLIをVPS上で実行することでOpenAI API従量課金をChatGPTサブスク固定費に置き換え、スケール時のコスト増を回避できる
- 通知（Discord）・保存（Notion）・配信（Vercel/RSS）・未読管理（Feedly）を役割別サービスに分離することで、各レイヤーの差し替えや拡張が容易になる
- 要約本文はNotionの非公開ページに保存し、VercelではRSSメタ情報のみ公開することで、シンプルな構成で公開範囲を制御できる
## 関連記事

- /deep_862 VPSに感情モデルを放置したら、罪悪感が育った話

## 原文リンク

[DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する](https://zenn.dev/kazami/articles/discord-agent-bot-20260328)
