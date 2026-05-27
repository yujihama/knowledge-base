---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-27
tags: [Claude Code, マルチエージェント, Claude Managed Agents, Dreaming, 自律コーディング, LLMエージェント, AIペアプログラミング]
category: "agent-arch"
related: [5496, 3671, 3490, 3324, 3532]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-27T09:17:55.397557"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeを開催（Google I/Oと同日）。参加した開発者の約半数が「直近1週間でClaudeが完全に書いたPRをマージした」と挙手し、その多くが「コードを一切読まずにマージした」と認めた。AnthropicエンジニアのBoris Chernyは基調講演で「デフォルトは『Claudeにプロンプトする』ではなく『Claudeが自分自身にプロンプトする』」と述べ、人間がエラーを見ることなくClaudeが自律的にテスト・修正を繰り返す自動化を目指す方針を明示した。注目機能として「Dreaming」が紹介された。これはClaude Managed Agents（マルチエージェント構築・実行向けクラウド基盤）の機能で、コーディングエージェントがタスクごとにノートを記録・保存し、別のエージェントが同一コードベースを扱う際に過去のノートを参照して学習・引継ぎを行う仕組み。さらにDreamingはノートを横断的に読み込んでパターンや共通課題を抽出することで、エージェントがコードベースへの理解を継続的に深める効果を持つ。Spotify、Delivery Hero、Lovable、Monday.comなど複数企業がClaude Codeを中心に開発体制を再編した事例を共有。一方で、イベント外では「AIが生成した大量コードのレビュー負担増」「AIへの過度な依存によるコーディングスキル低下」「安全でないコード生成によるセキュリティリスク」への懸念がHacker NewsやRedditで広まっている。ClaudeエンジニアリングリードのKatelyn Lesseは「旧来のソフトウェア開発のベストプラクティスは今も有効だが、見失っているチームが多い」と指摘。現時点のClaudeを「ミドルレベルエンジニア相当」と位置づけつつ、最終目標は「ClaudeがClaude自身をビルドできる状態」（プロダクトリードAngela Jiang）と表明。監査エージェント開発への示唆として、Dreamingのようなエージェント間ナレッジ共有・継続学習の仕組みは、複数エージェントが同一監査ルールセットやワークペーパーを扱う場面での引継ぎ精度向上に直接応用できる。また人間のオーバーサイト省略リスクは監査分野では致命的であり、自律化と統制のバランス設計が重要な設計課題となる。

## アイデア

- DreamingによるエージェントのKnowledge Persistenceは、監査エージェントが複数の調書・ルールを跨いで学習を蓄積する仕組みへそのまま転用できる
- 「Claudeが自分自身にプロンプトする」自己ループ構造は、ReActやLangGraphのself-reflection設計の延長として捉えると、ループ終了条件とコスト制御が鍵になる
- 技術マネージャーがコード量の急増でオーバーサイト不能になっている現実は、AIエージェント導入時の組織設計問題として、生成量ではなくレビュー可能量を制約条件にするアーキテクチャ設計を示唆する

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **Pull Request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **LLMエージェント自律性** (TODO: 読むべき)
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_3671 エージェントオーケストレーション：今のAIで重要な10のこと
- /deep_3490 エージェントオーケストレーション：今AIで重要な10のこと｜MIT Technology Review
- /deep_3324 エージェントオーケストレーション：今AIで重要な10のこと
- /deep_3532 エージェントオーケストレーション：今AIで重要な10のこと

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
