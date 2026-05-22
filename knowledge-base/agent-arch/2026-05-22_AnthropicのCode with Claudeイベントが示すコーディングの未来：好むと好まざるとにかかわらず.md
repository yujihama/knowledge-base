---
title: "AnthropicのCode with Claudeイベントが示すコーディングの未来：好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-22
tags: [Claude Code, AI coding, autonomous agent, Dreaming, multi-agent, Anthropic, vibe-coding, software development]
category: "agent-arch"
related: [609, 5801, 3828, 2205, 3379]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-22T21:07:26.860742"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeという2日間の開発者向けイベントを開催した。基調講演ではBoris Cherny（Claude Codeリード）が、AIコーディングの新たなパラダイムを提示した。従来の「人間がClaudeにプロンプトを投げる」モデルから、「Claudeが自らプロンプトを生成して自律的に作業する」モデルへの移行が宣言された。Anthropicのエンジニア、Jeremy Hadfieldによれば、Anthropic社内のソフトウェアの大半はすでにClaudeが記述しており、Claude Code自体のコードもClaudeが書いたという。

注目の新機能は「Dreaming」と呼ばれるシステムで、2週間前に発表済み。Claude Codeエージェントがタスクごとに作業メモを記録・保存し、別のエージェントが同じコードベースに取り組む際にそのメモを参照して素早く状況を把握できる仕組みだ。Dreamingはこれらのメモを横断的に分析し、パターンや共通課題を抽出することで、特定コードベースへの理解をエージェント間で累積的に向上させる。エンジニアのRavi Trivediはこれを「クロードに任せてしまう（Let it cook）」哲学と表現した。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが参加し、Claude Codeを中心に開発チームを再編した事例を共有した。Claude engineering leadのKatelyn Lesseは「現時点でClaudeはミドルレベルのエンジニアと同等のコーディング能力を持つ」と評価しつつ、システム設計や複雑な問題解決には引き続き上級エンジニアが必要だと述べた。最終目標はClaudeが自分自身をビルドできる状態（Angela Jiang談）とされている。

一方、会場外では批判的な声も存在する。RedditやHacker Newsでは「生成コードを問題ないと言うのは読んでいない人だけ」との指摘があり、AIが生成した安全でないコードがセキュリティ脆弱性を増大させるという研究者の警告もある。また、開発者がAIに依存するにつれてコーディングスキルが低下するとの懸念もある。Lesseは「従来のソフトウェア開発ベストプラクティスは今も有効」と主張しながらも、大量コード生成による技術管理職の疲弊という現実も認めた。監査エージェント開発の観点では、エージェントが自律的に作業ノートを蓄積・参照するDreamingの仕組みは、複数エージェントが協調してドキュメントや証跡を管理するマルチエージェント監査ワークフローへの応用可能性がある。

## アイデア

- Dreamingシステム：エージェントが作業メモを蓄積・共有し、後続エージェントがコードベースへの理解を引き継ぐ仕組みは、マルチエージェントシステムにおける暗黙知の形式化・継承メカニズムとして注目できる
- 「Claudeが自らプロンプトを生成する」自己指示型ループは、人間のフィードバックなしにエラー検出・修正を繰り返すRLAIF的な自律改善サイクルに近く、監査エージェントの自己検証ループ設計に示唆がある
- コードを一切読まずにPRをマージするケースが会場の約半数に存在するという事実は、AIが生成したコードの品質保証・セキュリティ検証の自動化需要が急増していることを示しており、LLM-as-judgeによるコードレビューエージェントの市場機会を示す

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **multi-agent system** (TODO: 読むべき)
- **autonomous coding agent** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装

## 関連記事

- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- /deep_5801 嘘を暴くAI vs 嘘を隠すAI — Anthropicが描く自動監査の「知性戦」
- /deep_3828 エージェントオーケストレーション：今のAIで重要な10のこと
- /deep_2205 なぜAnthropicは軍と戦う？1億ドルPartner NetworkとAI研究所の全貌
- /deep_3379 【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α

## 原文リンク

[AnthropicのCode with Claudeイベントが示すコーディングの未来：好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
