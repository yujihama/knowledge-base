---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-28
tags: [Claude Code, マルチエージェント, Claude Managed Agents, Dreaming, 自律コーディング, エージェント知識共有, Anthropic]
category: "agent-arch"
related: [5496, 4753, 6745, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-28T21:14:27.580551"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeという開発者向け2日間イベントを開催した。同日はGoogle I/Oと重なったが、Anthropic側は偶然だと説明した。

イベントでAnthropicエンジニアのJeremy Hadfieldが「過去1週間でClaudeが完全に書いたプルリクエストをシップした人は？」と問うと、会場の約半数が挙手。さらに「コードを一切読まずにシップした人は？」との問いにも、大半の手が下りなかった。

Claudeのコードリード・Boris Chernyは基調講演で「デフォルトが『Claudeにプロンプトを投げる』から『Claudeが自分自身にプロンプトを投げる』に変わった」と述べ、AIによるコード生成→自己テスト→自己修正のループを人間が介在せずに完結させる方向性を示した。エラーメッセージも人間が見る前にClaudeが対処し、「Let it cook（Claudeに任せる）」という設計思想を強調した。

新機能として、Claude Managed Agents（2週間前に発表されたクラウドベースのマルチエージェント基盤）に「Dreaming（ドリーミング）」が追加された。コーディングエージェントがタスク実行中にメモを書き残し、後続エージェントがそのメモを参照して学習コストを削減する仕組み。Dreamingはそれらのメモを集約・パターン分析し、特定コードベースへの習熟を累積的に高めることを目的とする。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなども登壇し、Claude Codeを中心に開発体制を再編した事例を紹介。「ほとんどのAnthropicのソフトウェアはClaudeが書いており、Claude Code自体のコードもClaudeが書いている」とも語られた。

一方で会場外では懸念の声も上がっている。HackerNewsやRedditでは「生成コードを問題ないと言うのは読んでいない人だけ」「AIツールで自分のコーディング力が落ちた」「安全でないコードが増える」などの意見が散見される。

ClaudeエンジニアリングリードのKatelyn Lesseは「従来のソフトウェア開発ベストプラクティスは今も有効。多くのチームがこの変化の中でそれを見失っているだけ」と応じ、「現状のClaudeはミドルレベルのエンジニア相当のコード品質」と評価。システム設計や難問のトラブルシューティングには引き続き熟練エンジニアが必要だと述べた。製品リードAngela Jiangは「最終的にClaudeが自分自身をビルドできるようにすることが目標」と語った。

監査エージェント開発への示唆：エージェントが実行ログをメモとして残し後続エージェントが活用するDreamingのアーキテクチャは、監査エージェントにおける証跡蓄積・知識継承の設計（ReActループの実行履歴を次回エージェントに引き渡す構造）と直接対応する。マルチエージェント環境での知識共有メカニズムとして参考になる。

## アイデア

- Dreamingはエージェントがタスクメモを書き残し後続エージェントが参照することでコードベースへの集合知を累積するアーキテクチャで、長期記憶をエージェント間で共有する実用的な設計パターン
- 「Claudeが自分自身にプロンプトを投げる」というメタ自律ループの設計——人間のレビューを前提としない自己修正サイクルがデフォルトになると、品質保証の責任所在が根本的に変わる
- コードを一切読まずにPRをマージする開発者が会場の過半数というデータは、AIコード生成のリスク認識と生産性圧力のトレードオフを定量的に示す社会的指標として興味深い

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **プルリクエスト** → /deep_1665 Hugging Face Hubにプルリクエストとディスカッション機能が追加
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **自己修正ループ** → /deep_2825 Claude Codeハーネスエンジニアリングを最小構成でA/Bテストしてみた

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
