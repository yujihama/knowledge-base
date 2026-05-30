---
title: "AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-30
tags: [Claude Code, Claude Managed Agents, Dreaming, マルチエージェント, 自律コーディング, Code with Claude, Anthropic]
category: "agent-arch"
related: [5496, 4753, 6745, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-30T09:14:52.441844"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeと題した2日間の開発者向けイベントを開催した。同日はGoogleのI/Oと重なったが、Anthropic側は偶然と説明した。基調講演でClaudeエンジニアのJeremy Hadfieldが「先週、Claudeが完全に書いたPRをshipしたことがある人」と問いかけたところ、会場の約半数が挙手。さらに「コードを一切読まずにshipしたことがある人」という問いかけでも、多くの手がそのまま残った。

AnthropicのBoris Cherny（Claude Codeリード）は「デフォルトが『Claudeにプロンプトを打つ』から『Claudeが自分自身にプロンプトを打つ』に変わった」と述べた。人間がエラーメッセージを見ることなく、Claudeがtest→tweakのループを自律的に繰り返す完全自動化を目指している。エンジニアのRavi Trivediはこれを「Claudeに料理させる（Let it cook）」と表現した。

技術面では、Claude Managed Agentsの新機能「Dreaming」が紹介された。これはエージェントが特定タスクに関する知見をノートとして記録・保存し、後続エージェントがそのノートを参照して学習コストを削減する仕組みだ。Dreamingはノート群を横断的に読み込み、パターンや共通エラーを抽出することで、コードベースへの理解をエージェント間で共有・蓄積する。なお、DreamingはClaude Codeではなくclaude Managed Agentsの機能である（記事は当初誤記があり訂正済み）。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが参加し、開発チームをClaude Code中心に再編した事例を紹介した。Anthropicのエンジニアリングリード Katelyn Lesseは「Claudeはミドルレベルエンジニアと同程度のコード品質を持つ」としつつ、システム設計や難易度の高い問題解決には依然として専門家が必要と述べた。製品リードのAngela Jiangは最終目標として「ClaudeがClaude自身をビルドできること」を挙げた。

Anthropicのコードの大部分はすでにClaude自身が生成しているという。一方、会場外ではRedditやHacker Newsでコーダーの懸念も噴出している。「生成コードで問題がないと言うのは読んでいない人だけ」という声や、AIへの依存によるコーディング能力の低下、セキュリティ脆弱性リスクも指摘されている。Lesseはこれに対し「従来のソフトウェア開発ベストプラクティスは依然有効であり、この瞬間に多くの人がそれを見失っているだけ」と応答した。自動化が進む中で人間のオーバーサイト縮小が課題として残ることを示唆している。

監査エージェント開発への示唆：マルチエージェント間でのナレッジ共有（Dreaming機能）は、監査エージェントが複数のサブタスクを並列実行する際の知見蓄積・エラー学習ループとして直接応用可能。ただし「コードを読まずにshipする」慣行は監査プロセスの証跡管理と根本的に矛盾するため、自動化範囲の設計には慎重な判断が必要。

## アイデア

- Dreamingはエージェント間の暗黙知を明示的なノートとして永続化し、後続エージェントの学習コストを削減する設計——監査ログの知識グラフ化と同じ発想
- 「ClaudeがClaude自身をビルドする」という再帰的自己改善ループは、エージェントの自律度の理論的上限を示しており、監査AIの自律設計範囲を考える際の参照点になる
- コードを読まずにPRをshipする慣行が既に半数以上のエンジニアに浸透しているという実態は、AIアウトプットの品質保証とオーバーサイト設計をシステム側で強制する必要性を示している

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **Pull Request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **Claude Managed Agents** → /deep_2364 Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす
- **LLMコード生成** → /deep_19 LLMのコード生成はなぜ同じミスを繰り返すのか — 失敗を「演算子」にして生成過程を書き換える

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
