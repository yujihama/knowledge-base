---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-06-01
tags: [Claude Code, Claude Managed Agents, Dreaming, multi-agent, agentic coding, 自律コーディング, PR自動生成]
category: "agent-arch"
related: [5496, 609, 3828, 2689, 6783]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-06-01T21:29:19.821138"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeイベントを開催した（同日Google I/Oと重なったのは偶然とのこと）。会場でのアンケートでは、参加者の約半数が「コードを一切読まずにClaudeが書いたPRをShipした」と手を挙げた。AnthropicのBoris Cherny（Claude Code責任者）は基調講演で「デフォルトが『Claudeにプロンプトする』ではなく、『ClaudeがClaudeにプロンプトする』になった」と表現し、人間の介在なしにClaudeが自律的にテスト・修正を繰り返す自動化を目標として掲げた。エンジニアのRavi Trivediは「Claude Managed Agents」（マルチエージェントシステム構築・実行のクラウド基盤）の新機能「Dreaming」を紹介した。Dreamingとは、コーディングエージェントがタスクに関するメモを自動記録・保存し、後続の別エージェントがそのメモを読み込んで過去のエラーやパターンを学習できる仕組みである。これによりコードベースへの習熟が累積的に蓄積される。イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが登壇し、開発チームをClaude Code中心に再編した事例を共有した。一方、イベント外では否定的な声も上がっており、HackerNewsやRedditでは「AIが生成したコードのレビューで業務が増えた」「コーディング能力が低下している」といった批判や、AIツールがセキュリティ脆弱性を含むコードを生成するリスクへの警告も出ている。Anthropicエンジニアリングリードのkatelyn Lesseは「従来のソフトウェア開発のベストプラクティスは今も有効」と述べつつ、多くのチームがそれを見失っていると認めた。また「現時点でClaudeはミドルレベルエンジニア程度のコード作成能力を持つ」とし、上位設計や難問トラブルシューティングには専門家が必要だと述べた。製品リードのAngela Jiangは最終目標を「ClaudeがClaudeを自己構築できる状態」と表現した。監査エージェント開発への示唆として、Dreamingのような「エージェント間での知識・エラー履歴の共有・蓄積」はLangGraphベースのマルチエージェント監査システムにも直接応用可能であり、監査手続きの反復実行による品質向上メカニズムとして設計参考になる。

## アイデア

- Dreamingによるエージェント間のメモ共有・パターン蓄積は、監査エージェントがチェックリスト実行履歴や過去の指摘パターンを後続エージェントに引き継ぐ仕組みとして転用できる
- 『ClaudeがClaudeにプロンプトする』という自己ループ型自動化は、ReActエージェントにおけるself-refinementループの実用化事例として注目に値する
- コードを読まずにPRをShipする開発者が半数という現状は、コードレビューそのものをLLM-as-judgeで代替するニーズを示しており、監査AIの『証跡レビュー自動化』に対する市場感度と合致する

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **multi-agent systems** (TODO: 読むべき)
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **pull request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- /deep_3828 エージェントオーケストレーション：今のAIで重要な10のこと
- /deep_2689 「並列は速い」は本当か──subagent 76% DENIED検証とCladeの選択
- /deep_6783 Google I/Oは何を示したか——コーディングAIの方向性がどう変わりつつあるか

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
