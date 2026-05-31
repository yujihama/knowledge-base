---
title: "AnthropicのCode with Claudeが示すコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-31
tags: [Claude Code, マルチエージェント, Claude Managed Agents, Dreaming, 自律コーディング, PR自動生成, エージェント知識共有]
category: "agent-arch"
related: [5496, 4753, 4902, 6745, 4520]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-31T21:07:38.489892"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeと題した開発者向け2日間イベントを開催した。会場では「先週Claudeが完全に書いたPRをShipした人」への挙手で約半数が応答し、さらに「コードを一切読まずにShipした人」でもほぼ同数の手が上がったまま維持されたという場面が象徴的だった。

AnthropicのClaude Codeヘッドを務めるBoris Chernyは基調講演で「デフォルトはもはや『Claudeにプロンプトを送る』ではなく、『Claudeに自分自身にプロンプトを送らせる』だ」と述べ、完全自律的なコード生成・検証ループの実現を目指す方針を明言した。エラーメッセージを人間が見ることなく、Claudeが自分でテスト・修正を繰り返して完結させることが最終目標とされる。

新機能として発表されたのが、Claude Managed Agents（クラウドベースのマルチエージェント基盤）における「Dreaming」機能だ。コーディングエージェントがタスク遂行中にメモを自律的に記録・保存し、後続エージェントが同一コードベースで作業する際にそのメモを参照することで立ち上がりを高速化し、過去のエラーから学習できる仕組みである。Dreamingはさらに複数エージェントのメモを統合し、共通パターンや頻出問題を抽出することでコードベース固有の知識を蓄積していく。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが参加し、Claude Codeを中心に開発体制を再構築した実例を披露した。Anthropicエンジニアのパートでは「AnthropicのほぼすべてのソフトウェアはもはやClaudeが書いており、Claude Code自体のコードの大部分もClaudeが書いた」と述べられた。

一方で会場外では批判的な声も存在する。RedditやHacker Newsでは「マネージャーが生産性向上を追求するあまりAIコード生成を推進しているが、実際はレビュー負荷が増えて開発が困難になっている」「生成コードに問題がないと言う人はコードを読んでいない人だけだ」などの意見が出ている。研究者からはAIツールが安全でないコードを生成しセキュリティ脆弱性を増大させるリスクも指摘されている。

AnthropicのKatelyn Lesseは懸念に対し「ソフトウェア開発のベストプラクティスはすべて依然として有効」と応じつつも、コード量増大によりAnthropicの技術マネージャーが管理に疲弊しているという実情も認めた。Claudeの実力については「現時点でミドルレベルのエンジニアと同等程度のコード品質」と評価し、システム設計や難易度の高い問題解決には引き続き上級エンジニアが必要だとした。製品リードのAngela Jiangは「最終的にはClaudeが自分自身をビルドできるようになることを目指している」と述べた。

監査エージェント開発への示唆：Dreamingのような「エージェントが作業ログを自律的に残し後続エージェントが学習する」仕組みは、監査エージェントにおける証跡管理・知識継承アーキテクチャの設計に直接応用できる。特にLangGraphベースの複数エージェント構成で、過去の監査手続きや例外処理のメモを共有ストアに蓄積し再利用するパターンとして検討価値が高い。

## アイデア

- Dreamingによるエージェント間知識継承：個々のエージェントが残したメモを後続エージェントが参照・統合することで、コードベース固有の暗黙知を組織的に蓄積できるアーキテクチャは、監査エージェントにおける手続き知識の引き継ぎに応用可能
- 「Claudeが自分自身にプロンプトを送る」という自己駆動ループ：人間のプロンプト入力を起点とせず、エージェントが自律的にサブタスクを生成・検証する設計は、ReActベースの監査エージェントにおけるオーケストレーション戦略として参考になる
- コードレビューなしのPRマージが常態化するリスク：生成コードの品質保証と人間監視の役割分担をどう設計するかは、監査AIの説明責任・証跡確保の観点とも共鳴する重要な組織設計課題

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **Pull Request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **LLMコード生成** → /deep_19 LLMのコード生成はなぜ同じミスを繰り返すのか — 失敗を「演算子」にして生成過程を書き換える
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_4902 週刊AIニュース（2026/5/4号）：OpenAI Symphony公開・Microsoft独占契約終了・ハルシネーション論文
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）

## 原文リンク

[AnthropicのCode with Claudeが示すコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
