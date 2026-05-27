---
title: "AnthropicのCode with Claudeが示したコーディングの未来：好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-27
tags: [Claude Code, Claude Managed Agents, Dreaming, マルチエージェント, 自律コーディング, Code with Claude, Anthropic, PR自動生成]
category: "agent-arch"
related: [5496, 4753, 4902, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-27T21:10:13.060434"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeという開発者向け2日間イベントを開催した。同日はGoogle I/Oも開催されていたが偶然とのこと。会場では「先週Claudeが完全に書いたPRをシップした人」への挙手で半数近くが手を挙げ、さらに「コードを一切読まずにシップした人」でもほとんどの手が下がらなかった。Anthropicエンジニアのジェレミー・ハドフィールドは「AnthropicのほとんどのソフトウェアはClaudeが書いており、Claude Code自身もClaudeが書いたコードで構成されている」と発言。Claude CodeヘッドのBoris Chernyは基調講演で「デフォルトが『Claudeにプロンプトする』から『Claudeが自分自身にプロンプトする』に変わった」と述べ、人間が介在せずにClaudeが自律的にテスト・修正を繰り返す方向性を明確にした。新機能「Dreaming」はClaude Managed Agents（クラウドベースのマルチエージェント基盤）の機能として発表された。これはコーディングエージェントがタスク遂行中にメモを残し、別のエージェントが同じコードベースを扱う際にそのメモを参照・統合することで、過去のエラーパターンや知見を共有する仕組みである。理論的にはコードベースへの習熟度が蓄積される自己改善ループとなる。イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどがClaude Code活用事例を発表。一方、カンファレンス外では「AIが生成した大量のコードのレビュー負担が増大している」「AIツールに依存しすぎて自分のコーディング能力が低下した」「生成コードにセキュリティ脆弱性が含まれる」といった批判もRedditやHacker Newsで上がっている。Claudeエンジニアリングリードのカテリン・レッシーは「従来のソフトウェア開発ベストプラクティスは今も有効」と述べつつ、Anthropicの技術マネージャーたちが急増するコード量の管理に疲弊していることも認めた。「現在Claudeはミドルレベルエンジニアのコーディングにはほぼ同等」とも評価。製品リードのアンジェラ・ジャンは「最終的にはClaudeが自分自身をビルドできる状態を目指している」と述べた。監査エージェント開発への示唆としては、Dreamingのようなエージェント間知識共有の仕組みは、監査ワークフローにおける複数エージェント間での監査証跡・判断根拠の蓄積と再利用に直接応用可能な設計パターンである。

## アイデア

- Dreamingはエージェントがタスクメモを残し後続エージェントが参照する非同期知識蓄積パターンで、RAGとは異なる『エージェント間エピソード記憶』の実装例として注目に値する
- 『Claudeが自分自身にプロンプトする』という自己指示ループは、外部人間フィードバックなしにエラー修正を完結させるRLAIF的アーキテクチャの実用化を示す
- ミドルレベルエンジニア相当とされるClaudeのコーディング能力評価は、監査エージェントにおけるタスク委任可能範囲（定型的リスク評価vs複雑な判断）の設計基準として活用できる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **Pull Request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **RLAIF** → /deep_1372 LLMチャットボットに欠けているもの：目的意識のある対話
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_4902 週刊AIニュース（2026/5/4号）：OpenAI Symphony公開・Microsoft独占契約終了・ハルシネーション論文
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来：好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
