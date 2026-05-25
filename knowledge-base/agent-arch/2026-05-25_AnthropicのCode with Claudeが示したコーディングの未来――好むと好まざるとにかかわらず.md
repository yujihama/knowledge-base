---
title: "AnthropicのCode with Claudeが示したコーディングの未来――好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-25
tags: [Claude Code, 自律エージェント, Dreaming, コード生成, マルチエージェント, 自己修正ループ, Anthropic]
category: "agent-arch"
related: [4753, 5160, 5496, 2688, 4520]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-25T12:00:39.252419"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeイベント（2日間）を開催。登壇者Jeremy Hadfield（Anthropicエンジニア）によると、会場の約半数の開発者が「直近1週間でClaudeが完全に書いたPRをマージした」と回答し、さらにその大半が「コードを一行も読まずにマージした」と認めた。Anthropic自身も「Anthropicのソフトウェアの大半は現在Claudeが書いており、Claude CodeのコードもClaudeが書いた」と公言している。

Boris Cherny（Claude Codeリード）はキーノートで方針を明確にした。人間がプロンプトを打ってコードを生成させるのではなく、「Claudeが自分自身にプロンプトを打つ」自律ループが新しいデフォルトだとした。エラーメッセージも人間に見せず、Claudeがテスト・修正を繰り返し、完成形のみを人間に渡す設計を目指している。

技術的な新機能として「Dreaming」が紹介された（2週間前に発表済み）。Claude Codeエージェントがタスク実行中にノートを書き残し、後続エージェントがそのノートを参照してコードベースの文脈を高速に把握し、過去エラーから学習する仕組み。Dreamingはこれらのノートを集約・パターン分析し、特定コードベースへの適応精度を継続的に向上させるシステムである。マルチエージェントの知識継承メカニズムとして機能する。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなど多数の企業が登壇し、Claude Codeを中心に開発体制を再構築した事例を共有した。

一方、会場外ではHacker NewsやRedditで懸念の声も上がっている。「生成コードを問題ないと言う人は読んでいない人だけ」という批判、AIツールによるコーディング能力の低下、セキュリティ脆弱性を含むコードの量産リスクなどが指摘されている。Claude engineering leadのKatelyn Lesseは「従来のソフトウェア開発ベストプラクティスは今も有効で、見失っているチームが多い」と述べた。また「現時点でClaudeはミッドレベルエンジニア程度のコーディング能力がある」とも評価し、上位エンジニアによるシステム設計・難問解決は依然として必要と認めた。最終目標はClaudeが自分自身をビルドできる状態だとClaudeプロダクトリードのAngela Jiangは語った。

## アイデア

- Dreamingによるエージェント間知識継承：個々のエージェントが残したノートをシステムが集約しパターン抽出することで、コードベース固有の知識をエージェント群が共有・蓄積する設計は、監査エージェントの証跡・知見管理にそのまま転用可能
- 「人間はエラーを見ない」設計思想：テスト・修正ループをエージェントが自律完結させ、完成形のみを人間に渡すアーキテクチャは、監査ワークフローにおける例外のみ人間にエスカレートするパターンと同構造
- コードレビューなしのPRマージが常態化しつつある現実：品質・セキュリティリスクの管理責任が開発者からシステム設計者（エージェントアーキテクト）に移行しており、監査観点でのAIガバナンス設計の重要性が高まっている

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **自律エージェントループ** (TODO: 読むべき)
- **マルチエージェント協調** → /deep_3906 検証付きマルチエージェント協調：「計画・実行・検証・再計画」フレームワーク VMAO
- **ReAct / self-correction** (TODO: 読むべき)
- **LLM-as-developer** (TODO: 読むべき)

## 関連記事

- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_5160 通勤中に育てたAIが、放置していたアイデアを勝手に形にした【OpenClawエージェント4体を止めるまで①】
- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来――好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
