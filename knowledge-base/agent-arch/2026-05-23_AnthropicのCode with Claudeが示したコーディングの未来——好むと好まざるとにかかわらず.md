---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-23
tags: [Claude Code, Dreaming, コーディングエージェント, 自律的自己修正, マルチエージェント, 知識継承, AI駆動開発]
category: "agent-arch"
related: [6193, 4753, 5496, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-23T21:02:27.810868"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeと題した開発者向け2日間イベントを開催した（同日GoogleのI/Oがパロアルトで開催されていたが、偶然とのこと）。会場で行われたアンケートでは、参加者の約半数が「先週、Claudeが完全に書いたPull Requestをshipした」と手を挙げ、さらにその大半が「コードを一切読まずにshipした」とも回答した。

Claude Codeのヘッド・Boris Chernyは基調講演で「デフォルトはもはや『Claudeにプロンプトを送る』ではなく、『ClaudeがClaudeにプロンプトを送る』だ」と述べ、自律的な自己修正ループを標榜した。エンジニアのRavi Trivediが紹介した新機能「Dreaming」は、複数のコーディングエージェントが同一コードベースを扱う際に、各エージェントが作業ログ（notes）を書き残し、後続エージェントがそれを読み込んで文脈を引き継ぐ仕組みだ。Dreamingはこれらのnotesをまとめて読み込み、パターンや共通エラーを抽出・統合することでコードベース固有の知識をClaude Code全体で蓄積する。イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなど、開発チームをClaude Code中心に再編した企業が参加し、成功事例を発表した。

ClaudeエンジニアリングリードのKatelyn Lesseは「Claudeは現時点でミドルレベルのエンジニアと同程度のコーディング能力がある」と評価しつつも、システム設計や難問のトラブルシューティングには依然として上級エンジニアが必要だと述べた。Anthropicの技術マネージャーがコードレビューの量に疲弊しているという実態も明かされた。プロダクトリードのAngela Jiangは「最終的にはClaudeがClaudeを自身でビルドできる状態を目指している」と語った。

一方、イベント外では批判的な声もある。RedditやHacker Newsでは「AIが生成したコードのレビューが増えて開発が難しくなった」「AIに任せることでコーディング能力が低下している」「レビューせずにshipされたコードが将来的なセキュリティ・保守リスクになる」といった懸念が上がっている。Lesseはこれらに対し「古いソフトウェア開発のベストプラクティスは今も有効であり、単に見失っているチームが多いだけ」と応じたが、自動化が進むにつれて人間の監視を省く誘惑が高まる構造的な矛盾は解消されていない。

監査エージェント開発への示唆：Dreamingのようなエージェント間の知識継承・統合メカニズムは、複数の監査エージェントが同一の調査対象や証跡ベースを繰り返し扱う場合に有効な設計パターンとなり得る。また「コードを読まずにshipする」という行動が常態化しつつある現象は、AI生成アウトプットの信頼性評価（LLM-as-judge的な品質ゲーティング）の重要性を改めて示している。

## アイデア

- Dreamingは複数エージェントが作業ログを共有・統合することでコードベース固有の暗黙知を蓄積する仕組みであり、エージェント間の非同期知識継承パターンとして監査エージェントへの応用が考えられる
- 「ClaudeがClaudeにプロンプトを送る」という自己プロンプトループの設計は、人間のフィードバックなしに品質を収束させるRLAIF的な発想に近く、ループ終了条件とエラー検知の設計が実装上の核心となる
- Claudeが書いたコードをレビューせずにshipする実態が半数に達しているという事実は、コード生成の精度向上と同時に、AI生成コードの品質を自動検証するゲーティング機構（静的解析・セキュリティスキャン・テスト自動化）の整備が急務であることを示している

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Pull Request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **RLAIF** → /deep_1372 LLMチャットボットに欠けているもの：目的意識のある対話

## 関連記事

- /deep_6193 AI Daily Digest 2026/5/20 — Agentic Workflows、コーディングエージェント、エンベデッドAI
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
