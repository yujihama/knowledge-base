---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-06-01
tags: [Claude Code, Claude Managed Agents, Dreaming, マルチエージェント, 自律コーディング, Pull Request自動生成, vibe-coding]
category: "agent-arch"
related: [5496, 4753, 6745, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-06-01T09:18:08.805374"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeを開催。GoogleのI/Oと同日の開催だったが、Anthropicスタッフは偶然と強調。会場では参加者の約半数が「過去1週間でClaudeが完全に書いたPull Requestをマージした」と手を挙げ、さらにその大半が「コードをまったく読まずにマージした」とも回答した。

Claude Codeの責任者Boris Chernyは基調講演で、「デフォルトは『Claudeにプロンプトを投げる』ではなく、『ClaudeがClaudeにプロンプトを投げる』になっている」と述べ、人間の介在を最小化する自律的な自己修正ループを志向していることを明確にした。エンジニアのRavi Trivediは「Claudeの邪魔をしないことが原則。Let it cook（任せてしまえ）」と表現した。

新機能として、Claude Managed Agents（クラウドベースのマルチエージェント基盤）の一部として「Dreaming」が紹介された。これはClaude Agentが特定タスクに関するメモを記録・保存し、後続のエージェントがそのメモを参照してコードベースの文脈を素早く把握し、過去のエラーから学習できる仕組み。Dreamingはこれらのメモを横断的に読み込み、パターンや共通課題を抽出することで、エージェント群がコードベースへの理解を継続的に深化させることを目指す。

登壇企業はSpotify、Delivery Hero、Lovable、Base44、Monday.comなど。「バイブコーディング（vibe-coding）」を支援するアプリを自らバイブコーディングで構築している企業もあり、再帰的な構造が見られた。

一方、会場外では懸念の声も広がっている。RedditやHacker Newsでは「生成コードが問題ないと言っているのは、それを読んでいない人だけ」という批判が上がり、コーディング能力の低下やAIが生成するコードのセキュリティ脆弱性も研究者から指摘されている。Anthropicエンジニアリングリードのkatelyn Lesseは「既存のソフトウェア開発ベストプラクティスはすべて今も有効。ただしこの時期に忘れている人が多い」と述べた上で、「現時点のClaudeはミドルレベルのエンジニア程度のコード品質」と評価。上位のアーキテクチャ設計や難問のトラブルシューティングには依然として熟練エンジニアが必要だとした。最終的なゴールとしてプロダクトリードのAngela Jiangは「ClaudeがClaudeを構築できるようになること」と明言した。

監査エージェント開発への示唆：Dreamingのような「エージェント間のナレッジ継承」機構はLangGraphベースの監査エージェントに応用可能。審査履歴・エラーパターンをエージェントが共有・蓄積する設計は、反復的な監査タスク（仕訳チェック、コントロールテスト等）における品質向上に直結する。

## アイデア

- Dreamingによるエージェント間ナレッジ継承：過去のエラーや知見をメモとして保存し後続エージェントが参照することで、コードベース固有の文脈をゼロから学習するコストを削減する設計
- 「ClaudeがClaudeにプロンプトを投げる」自己ループ：人間がプロンプトを書くのではなくエージェント自身が次のプロンプトを生成・実行するパラダイムシフトと、それに伴うレビューレスデプロイのリスク
- 会場内の熱狂と会場外の懸念の乖離：コードを読まずにマージする行動が半数規模で常態化している一方、Hacker NewsやRedditではセキュリティ・品質・スキル劣化への危機感が高まっており、採用側と批判側の認識ギャップが拡大している

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **Pull Request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **LLMコード生成** → /deep_19 LLMのコード生成はなぜ同じミスを繰り返すのか — 失敗を「演算子」にして生成過程を書き換える
- **Claude Managed Agents** → /deep_2364 Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
