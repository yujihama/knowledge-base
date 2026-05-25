---
title: "AnthropicのCode with Claudeが示したコーディングの未来：好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-25
tags: [Claude Code, コーディングエージェント, Dreaming, 自律コーディング, Anthropic, マルチエージェント, プルリクエスト自動化]
category: "agent-arch"
related: [6193, 4753, 5496, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-25T21:05:01.084661"
---

## 要約

2026年5月19日、Anthropicはロンドンでソフトウェアデベロッパー向けの2日間イベント「Code with Claude」を開催した。基調講演でエンジニアのJeremy Hadfield氏が「過去1週間でClaudeが完全に書いたプルリクエストを出荷した人」と問うと、会場の約半数が挙手。さらに「そのコードをまったく読まずに出荷した人」という問いにも、大半の手が残ったままだった。Anthropicによれば、「Anthropicのソフトウェアの大半は今やClaudeが書いており、Claude CodeのコードもClaudeが書いた」という。OpenAI、Google、Microsoftも同様の主張をしており、AI駆動コーディングが業界標準として定着しつつある現状が浮き彫りになった。

Claude Codeの技術責任者Boris Cherny氏は「デフォルトが『Claudeにプロンプトを送る』ではなく、『Claudeが自分自身にプロンプトを送る』になった」と述べ、Anthropicがコーディングの完全自動化を目指していることを強調した。エラーメッセージも人間に見せることなくClaudeが自律的にテストと修正を繰り返す設計思想を「Let it cook（Claudeにやらせろ）」と表現した。

新機能として「Dreaming」が紹介された。これはClaude Codeエージェントが特定タスクに関するノートを記録・保存し、後続のエージェントがそのノートを参照して学習を引き継ぐ仕組みだ。Dreamingシステムはこれらのノートを横断的に分析してパターンや共通問題を発見し、特定コードベースに対するClaude Codeの性能を継続的に改善する設計となっている。いわばエージェント間の知識継承メカニズムであり、マルチエージェント環境での長期的な性能向上を狙っている。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが登壇し、開発チームをClaude Code中心に再編した事例を共有した。一方で会場外では懸念も広がっており、Reddit・Hacker Newsでは「生成コードのレビュー負荷が増大する」「AIへの依存でコーディング能力が低下した」「安全でないコードが増えセキュリティリスクが高まる」との声が上がっている。

エンジニアリングリードのKatelyn Lesse氏は「ソフトウェア開発のベストプラクティスは今も有効だが、多くのチームがその視点を失いかけている」と認め、Anthropic社内でも技術マネージャーが急増するコード量の管理に疲弊していることを認めた。現状のClaudeは「ミドルレベルエンジニア相当」であり、最終目標は「ClaudeがClaudeそのものをビルドできるようになること」（Jiang氏）と明言した。監査エージェント開発の観点では、Dreamingのような「エージェント間ナレッジ継承」機構は、監査ワークフロー内での反復的タスク学習・誤り低減に直接応用できる可能性がある。

## アイデア

- Dreamingによるエージェント間ナレッジ継承：過去のエージェントが残したノートを後続エージェントが参照・統合することで、コードベース固有の知識をセッションをまたいで蓄積する仕組みは、監査エージェントの反復業務（同一クライアントの監査サイクル等）にも転用可能
- 「Claudeが自分自身にプロンプトを送る」という設計思想：人間のプロンプト介在なしにエージェントが自律的にテスト・修正ループを回す構造は、ReActループの発展形として位置づけられ、LangGraph等のオーケストレーション設計に示唆を与える
- コード生成の品質保証問題：「コードを読まずにPRをマージする」という現象が半数以上に見られることは、LLM生成コードのセキュリティ・品質検証をエージェント自身が行うLLM-as-judgeアプローチの重要性を高める

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **自律エージェント** → /deep_17 AI vs. アンチボット：LLMが書き換えるウェブスクレイピングの全ルール
- **プルリクエスト** → /deep_1665 Hugging Face Hubにプルリクエストとディスカッション機能が追加
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントアーキテクチャ** (TODO: 読むべき)

## 関連記事

- /deep_6193 AI Daily Digest 2026/5/20 — Agentic Workflows、コーディングエージェント、エンベデッドAI
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来：好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
