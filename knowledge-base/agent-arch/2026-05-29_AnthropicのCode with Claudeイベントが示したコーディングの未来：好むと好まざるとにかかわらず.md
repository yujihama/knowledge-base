---
title: "AnthropicのCode with Claudeイベントが示したコーディングの未来：好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-29
tags: [Claude Code, マルチエージェント, Claude Managed Agents, Dreaming, 自律コーディング, AIペアプログラミング, pull request自動生成]
category: "agent-arch"
related: [5496, 4753, 6745, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-29T09:18:21.996410"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeと題した2日間の開発者イベントを開催した。同日はGoogleのI/Oが米国で行われており、競合が重なったが偶然とのこと。

イベントの冒頭、AnthropicエンジニアのJeremy Hadfieldは「先週、Claudeが完全に書いたPRをshipした人は？」と問いかけ、会場の約半数が挙手。さらに「そのコードを一行も読まずにshipした人は？」と問うと、ほぼ同数の手が残ったままだった。これがAIコーディングの現在地を象徴している。

Claude Code責任者Boris Chernyは基調講演で、人間がClaudeにプロンプトを与えるのではなく「ClaudeがClaudeにプロンプトを与える」自律ループを基本モデルとする方針を表明。エラーメッセージすら人間が目にしないよう、Claudeがテスト・修正を繰り返すことを理想とする。

目玉機能として「Dreaming」が紹介された。これはClaude Managed Agentsの機能で、コーディングエージェントがタスク遂行中に自分宛てのメモを残し、後続エージェントがそのメモを参照して同じコードベースへの理解を素早く深めたり、過去のエラーから学習したりする仕組みだ。Dreamingはメモを横断的に読み、パターンや共通問題を抽出することでエージェントの継続的改善を支援する。

参加企業としてSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが事例を発表。しかしイベント外では懸念の声も上がっている。RedditやHacker Newsでは「生成コードを問題なしと言うのは読んでいない人だけ」「AIにタスクを任せるほど自分のコーディング力が落ちる」「安全でないコードが量産されリスクが増す」といった批判が見られる。

Claude engineeringリードKatelyn Lesseは「従来のソフトウェア開発ベストプラクティスは今でも有効。見失っているチームが多いだけ」と回答しつつ、急増するコードのレビューに技術マネージャーが疲弊している実態も認めた。「今のClaudeはミドルレベルエンジニア並み」と評価しつつ、システム設計や難解なデバッグには専門家が依然必要だと述べた。製品リードAngela Jiangは最終ゴールを「Claudeが自分自身をビルドできること」と表現した。

## アイデア

- Dreamingの設計思想：エージェントが自分宛てメモを残し後続エージェントが参照するという仕組みは、コードベース固有の文脈をエージェント間で継承するための軽量な長期記憶メカニズムであり、監査エージェントの引き継ぎ・継続的学習パターンに転用できる
- 「ClaudeがClaudeにプロンプトする」自律ループへの移行は、人間をフィードバックループの外に置くことで生産速度を上げる一方、監査品質の責任所在が曖昧になるリスクを内包しており、内部監査AIの設計でも同様のガバナンストレードオフが生じる
- ミドルレベルエンジニア相当の評価：システム設計・難問デバッグには専門家が必要という分業モデルは、監査領域でも「判断・設計はシニア監査人、証拠収集・文書化はエージェント」という役割分担に直接対応する

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **エージェントメモリ** → /deep_1657 FileGram: ファイルシステムの行動トレースによるエージェントパーソナライゼーション
- **pull request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **LLMコード生成** → /deep_19 LLMのコード生成はなぜ同じミスを繰り返すのか — 失敗を「演算子」にして生成過程を書き換える

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeイベントが示したコーディングの未来：好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
