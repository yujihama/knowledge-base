---
title: "Claudeは夢を見る｜「メモリー」と「dreaming」の正体を時系列で整理する"
url: "https://zenn.dev/yamato_snow/articles/45edb2b07b2cee"
date: 2026-05-17
tags: [Claude, dreaming, Managed Agents, memory, outcomes, multiagent orchestration, Harvey, エージェント設計]
category: "agent-arch"
related: [5496, 3764, 2920, 5000, 3820]
memo: "[Zenn LLM] Claudeは夢を見る｜「メモリー」と「dreaming」の正体を時系列で整理する"
processed_at: "2026-05-17T09:01:45.272527"
---

## 要約

Anthropicが2026年にリリースした2つの機能「メモリー」と「dreaming」の違いと関係性を整理した解説記事。

**メモリー機能（2026年3月16日〜）**：Claudeアプリ向けに提供された、過去チャット検索と文脈記憶の機能。ユーザーの好みや作業文脈（文体の好み、職種、進行中プロジェクト等）をセッションをまたいで保持する。設定画面の「メモリーを管理」から確認・削除が可能。

**dreaming（2026年5月6日〜）**：Claude Managed Agents向けのresearch preview機能。エージェントが過去の作業ログやメモリーストアを非同期でレビューし、成功・失敗パターンを抽出して次回セッションに活かすスケジュール処理。人間が仕事終わりに日報を振り返り改善点を整理する行為に相当する。法律AIスタートアップHarveyがManaged Agents＋dreamingを長文法律ドラフト業務に適用した社内テストでは、タスク完了率が約6倍に向上した（ただしベースラインや評価指標の詳細は非公開）。

同発表では**outcomes**（開発者がルーブリックで成功基準を定義し、graderエージェントが出力を評価する仕組み）と**multiagent orchestration**（リードエージェントが複数専門エージェントへ並列委任）も同時発表。3機能を組み合わせると「記憶→振り返り→成功基準評価→複数エージェント分担→再記憶」というサイクルが形成される。

**監査エージェント開発への示唆**：outcomesの「合格条件をシステムに渡す」設計は、監査判断基準をルーブリック化してエージェントに評価させるReAct/LangGraphベースの監査エージェントと直接親和性がある。またdreamingの「セッション間学習」は、監査調書・不正パターン・内部統制評価の蓄積ナレッジをエージェントが自律的に整理・改善するアーキテクチャへの布石となる。現時点ではresearch previewのため本番投入フェーズではなく、「何を成功と定義するか」「どのセッションログを残すか」を設計段階で意識し始めるフェーズ。

## アイデア

- dreamingはプロンプトエンジニアリングの延長ではなく「エージェント運用設計」という新たなレイヤーを要求する——何を経験させ何を記録に残すかの設計が、エージェント性能を左右する
- outcomesの「ルーブリック＋graderエージェント」パターンは監査AI領域で直接応用可能——内部統制評価の合否基準をシステムに渡し、LLM-as-judgeで自動評価するサイクルに対応する
- Harveyの6倍という数字よりも重要なのは、セッション間学習が業務成果に定量的に影響し始めたという事実——AIエージェントの価値がシングルセッション性能から累積学習性能へシフトしている

## 前提知識

- **Claude Managed Agents** → /deep_2364 Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **multiagent orchestration** (TODO: 読むべき)
- **ReAct Agent** (TODO: 読むべき)
- **セッション管理** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_3764 責任を固定するだけでは足りない――責任経路工学という設計対象
- /deep_2920 見て・指して・磨く：視覚フィードバックを用いたGUI接地のマルチターンアプローチ
- /deep_5000 自動計画における反事実推論
- /deep_3820 知ったかぶりのGPTか、すぐ意見を変えるClaudeか？「修復」がLLMのマルチターン対話の不安定性を明らかにする

## 原文リンク

[Claudeは夢を見る｜「メモリー」と「dreaming」の正体を時系列で整理する](https://zenn.dev/yamato_snow/articles/45edb2b07b2cee)
