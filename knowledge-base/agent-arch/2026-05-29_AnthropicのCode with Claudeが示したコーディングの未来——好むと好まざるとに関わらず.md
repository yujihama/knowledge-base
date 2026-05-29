---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとに関わらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-29
tags: [Claude Code, マルチエージェント, Dreaming, 自律コーディング, Claude Managed Agents, LLMエージェント, ソフトウェア開発自動化]
category: "agent-arch"
related: [5496, 3671, 3490, 3324, 3532]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-29T21:09:37.058845"
---

## 要約

2026年5月19日、AnthropicはロンドンでGoogle I/Oと同日に開発者向けイベント「Code with Claude」を開催した。登壇したAnthropicエンジニアのJeremy Hadfieldによれば、Anthropicの社内コードの大半はすでにClaudeが記述しており、Claude Code自体のコードもClaudeが書いたという。会場では参加者の半数近くが「直近1週間でClaudeが完全に書いたプルリクエストをレビューせずにshipした」と手を挙げるほど、AIコーディングの常態化が進んでいる。

Claudeコードリード責任者のBoris Chernyは基調講演で、今後の方向性を「人間がClaudeにプロンプトを送る」ではなく「ClaudeがClaudeにプロンプトを送る」自律的なモデルへの転換として提示した。エラーメッセージを人間が見ることなく、ClaudeがテストとTweakを繰り返して自律的に問題を解消することを目標としている。

注目の新機能として「Dreaming」が発表された。これはClaude Managed Agents（クラウドベースのマルチエージェント基盤）の機能で、エージェントがタスク実行中に得た知識をノートとして保存・共有する仕組みである。後続のコーディングエージェントはこのノートを参照することで同一コードベースへの理解を高速に獲得し、過去のエラーから学習できる。さらにDreamingシステムはこれら複数のノートを横断的に読み込んでパターンや共通問題を抽出・統合する機能も持つ。

Spotify、Delivery Hero、Lovable、Base44、Monday.comなど複数の企業が開発体制をClaude Code中心に再設計した事例を発表。イベント内の雰囲気は全面的に肯定的だったが、会場外では異論も存在する。Hacker News等では「生成コードが問題ないと言う人は実際に読んでいない人だけ」という批判や、AIコーディングツールが管理職の生産性要求に押し付けられることで実務上のレビュー負荷が増大しているとの声もある。

ClaudeエンジニアリングリードのKatelyn Lesseは「従来のソフトウェア開発のベストプラクティスは今も有効であり、それを見失っているチームがいる」と述べつつ、Anthropicの技術マネージャーがコード量の急増に疲弊していることも認めた。現時点でClaudeは「ミッドレベルエンジニア程度」の実力であり、システム設計や難解な問題解決にはまだ専門家が必要としながらも、最終的には「ClaudeがClaude自身をビルドできる状態」を目指すとClaudeプロダクトリードのAngela Jiangは述べた。監査AI開発の観点では、エージェントが自律的に誤りを検出・修正するアーキテクチャと、エージェント間の知識共有（Dreaming）の設計は、監査エージェントの品質保証やログ共有の仕組みに直接応用可能な示唆を含む。

## アイデア

- 「ClaudeがClaudeにプロンプトを送る」自己反省・自己修正ループの設計は、監査エージェントが自律的に検証結果を再評価するReActループと構造的に同一であり、実装参考になる
- Dreamingによるエージェント間ノート共有は、複数の監査エージェントが異なる時期に同一クライアント環境を調査する際の知識継承・引継ぎ問題を解決する具体的アーキテクチャパターンである
- 「コードを読まずにshipされたPRが約半数」という実態は、AIが生成したコードの品質保証をどのレイヤーで担保するかという問題を提起しており、コード生成の下流にAI-as-judgeを置くアーキテクチャの必要性を示唆する

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **ReActパターン** (TODO: 読むべき)
- **プルリクエストレビュー** (TODO: 読むべき)
- **LLM自律実行** (TODO: 読むべき)

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_3671 エージェントオーケストレーション：今のAIで重要な10のこと
- /deep_3490 エージェントオーケストレーション：今AIで重要な10のこと｜MIT Technology Review
- /deep_3324 エージェントオーケストレーション：今AIで重要な10のこと
- /deep_3532 エージェントオーケストレーション：今AIで重要な10のこと

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとに関わらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
