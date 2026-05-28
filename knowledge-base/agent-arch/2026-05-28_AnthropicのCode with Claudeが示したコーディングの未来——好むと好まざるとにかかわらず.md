---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-28
tags: [Claude Code, マルチエージェント, Dreaming, Claude Managed Agents, 自律コーディング, プルリクエスト自動化, エージェント知識共有]
category: "agent-arch"
related: [5496, 4753, 4520, 6126, 2254]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-28T09:19:54.231795"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeと題した開発者向けイベント（2日間）を開催した。同日はGoogleのI/Oと重なったが、Anthropic側は偶然だとしている。

イベントのオープニングでAnthropicエンジニアのJeremy Hadfieldが行った問いかけは象徴的だった。「先週、Claudeが完全に書いたプルリクエストをshipした人は？」——参加者の約半数が手を挙げた。「コードをまったく読まずにshipした人は？」——多くの手がそのまま残った。Claude Codeの責任者であるBoris Chernyは基調講演で、開発のデフォルトが「Claudeにプロンプトを送る」から「ClaudeがClaudeにプロンプトを送る」へ移行しつつあると表現した。

Anthropicが発表した新機能「Dreaming」は、Claude Managed Agents（クラウドベースのマルチエージェント実行基盤、2週間前に発表）の機能として実装されている。Claudeエージェントがタスク実行中にノートを書き残し、後続のエージェントがそのノートを参照して同一コードベースへの理解をスピードアップできる仕組みだ。Dreamingはこれらのノートを横断的に分析してパターンや共通エラーを検出し、エージェント集合体がコードベースへの適応を継続的に改善できるように設計されている。

Spotify、Delivery Hero、Lovable、Base44、Monday.comなどの企業がClaude Codeを中心に開発チームを再編した事例を発表。一方でイベント外では批判的な声も根強い。RedditやHacker Newsでは「管理者が生産性指標を追求するためにAIコーディングを推進しているが、実際にはレビュー対象のコードが増え開発がかえって困難になる」「生成コードに問題がないと言っているのはそれを読まない人だけだ」といった意見が出ている。

Claude技術リードのKatelyn Lesseは「従来のソフトウェア開発のベストプラクティスは今も有効であり、多くのチームがこの局面でそれを見失っている」と認めた上で、「現時点のClaudeはミッドレベルエンジニア程度のコーディング能力がある」と評価。上級エンジニアによるシステム設計やトラブルシューティングは依然必要だとした。ClaudeプロダクトリードのAngela Jiangは最終目標として「ClaudeがClaudeを自律的にビルドできる状態」を挙げた。

監査エージェント開発への示唆：Dreamingのような「エージェント間知識共有・パターン学習」の仕組みは、監査エージェントが複数の監査プロジェクトをまたいでルールや過去のエラーパターンを蓄積・再利用する設計に直接応用できる。また、コードレビューを省略しているという事実は、AIが生成する成果物に対する内部統制・品質ゲートの設計が急務であることを示している。

## アイデア

- Dreamingによるエージェント間ノート共有：複数のエージェントが同一コードベースで作業した履歴をメタ分析し、エラーパターンを集約することで、エージェント群が自律的に学習・改善するアーキテクチャ
- 「ClaudeがClaudeにプロンプトを送る」自己ループ型自動化：人間が直接指示する代わりに、オーケストレーターエージェントが下位エージェントにタスクを割り振り、エラー検出・修正まで完結させる設計思想
- AIが生成したコードを読まずにshipするという実態：これは内部統制の観点では重大なコントロールギャップであり、AIコード生成に対する品質・セキュリティゲートの自動化（AI-as-reviewer）の必要性を浮き彫りにしている

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **プルリクエスト** → /deep_1665 Hugging Face Hubにプルリクエストとディスカッション機能が追加
- **LLMオーケストレーション** → /deep_4 DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する
- **RAG／知識共有** (TODO: 読むべき)

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した
- /deep_2254 同僚の「細かすぎた」が機能になった──Cladeが育つ仕組み【v1.15.0】

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
