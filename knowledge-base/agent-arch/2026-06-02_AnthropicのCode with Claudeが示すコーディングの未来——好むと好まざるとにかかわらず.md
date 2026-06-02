---
title: "AnthropicのCode with Claudeが示すコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-06-02
tags: [Claude Code, Claude Managed Agents, Dreaming, マルチエージェント, 自律コーディング, PR自動化]
category: "agent-arch"
related: [5496, 4753, 6745, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-06-02T21:29:45.430834"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeを開催した（Google I/Oと同日）。会場では「過去1週間にClaudeが完全に書いたPRをマージした人」への挙手を求めたところ、ほぼ半数が挙手。さらに「そのコードを一切読まずにマージした人」という質問でも大半の手が下りなかった。Anthropicの発表によれば、Anthropicの全ソフトウェアの大部分はすでにClaudeが記述しており、Claude Code自体のコードもClaudeが書いているという。

Claude Codeのリードを務めるBoris Chernyは基調講演で「デフォルトは『Claudeにプロンプトを投げる』ではなく、『ClaudeにClaudeをプロンプトさせる』になった」と説明した。目標は人間がエラーメッセージを見ることなく、Claudeが自律的にtest→tweak→testのループを回して問題を解決する完全自動化だ。

新機能「Dreaming」はClaude Managed Agents（マルチエージェントのクラウド基盤）の機能として発表された。コーディングエージェントがタスク実行中にノートを書き残し、別のエージェントが同じコードベースに取り組む際にそれを参照することで、過去のエラーパターンや知見を再利用できる。Dreamingはそれらのノートを横断的に読み込んでパターンを抽出・統合し、エージェント群がコードベースに関する知識を蓄積する仕組みだ。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが登壇し、Claude Codeを中心に再構成した開発ワークフローを紹介した。会場内には不安の気配はなかったと記者は伝えている。

一方、会場外では懸念の声も上がっている。HackerNewsやRedditでは「生成コードを問題なしと言う人は読んでいない人だけ」という批判や、AIツールへの依存によるエンジニアのコーディング能力低下、セキュリティリスクの増大が指摘されている。Claudeエンジニアリングリードのkatelyn Lesseは「古いソフトウェア開発のベストプラクティスは今でも有効。見失っているチームが多いだけ」と述べる一方、管理職が大量生成されるコードの把握に疲弊していることも認めた。「Claudeはいまミッドレベルエンジニアとしてのコーディングはこなせる水準」とし、最終目標としてClaudeが自分自身（Claude）をビルドできるようになることが挙げられた。

## アイデア

- Dreamingによるエージェント間の知識共有：複数エージェントがノートを書き残し、後続エージェントがそれを参照・統合することでコードベース固有の知識を蓄積するアーキテクチャは、監査エージェントにおける調査知見の引き継ぎ・ナレッジ蓄積にそのまま応用できる
- 「ClaudeにClaudeをプロンプトさせる」自己駆動型ループ：エラーの検出・修正をClaudeが自律的に行うアーキテクチャは、監査ワークフローにおける証拠収集→判断→再調査のReActループの完全自動化モデルとして参考になる
- 人間の監視コストが新たなボトルネックに：コード生成速度が上がることで人間のレビュー・管理が追いつかなくなる現象は、監査エージェント導入時に監査人のレビュー設計を先に固める必要があることを示唆する

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **ReActループ** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **PR（Pull Request）** (TODO: 読むべき)
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示すコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
