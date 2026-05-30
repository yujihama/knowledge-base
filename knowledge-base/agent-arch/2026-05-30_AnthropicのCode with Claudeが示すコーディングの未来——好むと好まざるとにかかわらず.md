---
title: "AnthropicのCode with Claudeが示すコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-30
tags: [Claude Code, マルチエージェント, Claude Managed Agents, Dreaming, 自律コーディング, self-prompting, vibe-coding]
category: "agent-arch"
related: [5496, 4753, 6745, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-30T21:07:09.138877"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeという開発者向け2日間イベントを開催した。同日はGoogle I/Oと重なったが、偶然とのこと。イベントの冒頭、AnthropicエンジニアのJeremy Hadfieldが「先週Claude完全生成のプルリクエストをshipした人」と問うと、会場の約半数が挙手。さらに「コードを一切読まずにshipした人」と聞くと、大半の手が下がらなかった。AnthropicのBoris Cherneyは「デフォルトは今や『自分がClaudeにプロンプトする』ではなく、『Claudeがself-promptする』だ」と基調講演で述べた。Anthropicの目標は人間がエラーメッセージを見ることすらなく、Claudeがtest→tweak→testを自律反復する完全自動化。新機能「Dreaming」はClaude Managed Agents（クラウドベースのマルチエージェント基盤）の機能で、エージェントがタスク実行中に自分向けのノートを書き残し、後続エージェントが同一コードベースを扱う際にそのノートを参照・統合することで知識を継承・蓄積する仕組み。SpotifyやDelivery Hero、vibe-codingスタートアップのLovable・Base44・Monday.comなども自社開発体制をClaude Code中心に再編した事例を発表した。一方、会場外では批判的な声も上がっている。HackerNewsやRedditでは「生成コードを読まずにshipすることで品質・セキュリティリスクが蓄積する」「AI依存でコーディング能力が低下した」などの指摘が続く。AnthropicのKatelyn Lesseは「ソフトウェア開発のベストプラクティスは今も変わらず有効であり、一時的に見失っているチームが多い」と応じつつ、大量生成されたコードのレビュー負荷に疲弊している技術マネージャーが社内にいることも認めた。Lesseは「現在のClaudeはミドルレベルエンジニア相当のコード品質」と評価し、システム設計・難問のトラブルシューティングには引き続き上級エンジニアが必要と述べた。最終目標はClaudeが自分自身をビルドできるようになること。監査エージェント開発の観点では、Dreamingのような「エージェント間のコンテキスト継承・知識蓄積メカニズム」は、長期にわたる監査プロセスでエージェントが過去の調査結果や判断根拠を引き継ぐ設計に直接応用できる。

## アイデア

- Dreamingはエージェントが実行中に構造化メモを残し、後続エージェントがそれを読み込んで知識を継承する仕組みで、監査エージェントが複数タスクにまたがって証跡・判断根拠を引き継ぐ設計パターンに転用できる
- 「Claudeがself-promptする」というパラダイムシフトは、人間がプロンプトを設計する段階から、エージェントが自律的にサブタスクを分解・実行するオーケストレーションへの移行を示しており、LangGraphのようなフレームワーク設計の方向性と一致する
- 大量自動生成コードのレビュー負荷問題は、コード品質をLLM-as-judgeで自動評価するパイプライン（例: 静的解析＋LLMレビューの組み合わせ）への需要を示唆しており、監査領域の自動チェック設計にも通じる

## 前提知識

- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **プルリクエスト** → /deep_1665 Hugging Face Hubにプルリクエストとディスカッション機能が追加
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **オーケストレーション** → /deep_571 Heddle: エージェントRL推論のための分散オーケストレーションシステム

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示すコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
