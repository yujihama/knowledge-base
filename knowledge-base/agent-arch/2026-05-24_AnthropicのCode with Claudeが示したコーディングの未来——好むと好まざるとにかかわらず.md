---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-24
tags: [Claude Code, 自律エージェント, dreaming, コード自動生成, Anthropic, AI駆動開発, 自己改善ループ]
category: "agent-arch"
related: [2688, 2541, 2205, 3092, 3504]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-24T21:04:21.870636"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeイベントを開催した（Google I/Oと同日）。登壇したAnthropicエンジニアのJeremy Hadfieldは、会場の約半数の開発者が「Claudeが完全に書いたPRをマージした」「コードを一切読まずにマージした」と挙手したことを紹介した。

Boris Cherny（Claude Codeのヘッド）は基調講演で、方針を明確にした。「デフォルトは『Claudeにプロンプトを打つ』ではなく、『ClaudeがClaudeにプロンプトを打つ』だ」と述べ、人間がエラーメッセージを見ることなくClaude自身がテストと修正を繰り返す自律的なループを目標として掲げた。

新機能「dreaming」も紹介された。これはClaude Codeエージェントがタスクに関するノートを自分自身に書き残す仕組みで、後続のエージェントがそのノートを参照することで過去の失敗から学習し、特定コードベースへの習熟を蓄積できる。複数ノートを横断してパターンや共通問題を抽出し、知識を統合する点が特徴だ。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが参加し、Claude Codeを中心に再編した開発チームの事例を発表した。「Anthropicのほとんどのソフトウェアは今やClaudeが書いている」「Claude CodeのコードのほとんどはClaudeが書いた」とも語られた。

一方、会場外では懸念も広がっている。RedditやHacker Newsでは「AIが生成したコードのレビュー負担が増え、開発が難しくなった」「生成コードを問題ないと言うのはそれを読まない人だけ」といった批判が相次ぐ。また、AI利用により自身のコーディング能力が低下したという報告や、安全でないコードがセキュリティ脆弱性を増やすという研究者の警告もある。

エンジニアリングリードのKatelyn Lesseは「従来のソフトウェア開発ベストプラクティスは今も有効で、見失っているチームが多い」と述べる一方、急増するコード量を管理するAnthropicの技術マネージャーたちが疲弊していることも認めた。「Claudeは今やミドルレベルエンジニア程度のコード品質を持つが、システム設計や難問のトラブルシュートにはまだ専門家が必要」とも語った。プロダクトリードのAngela Jiangは「最終目標はClaudeがClaudeそのものをビルドできるようになること」と述べた。

監査エージェント開発への示唆：「dreaming」のような自律的なメモ蓄積・パターン抽出の仕組みは、監査エージェントが過去の監査結果を参照し精度を向上させるアーキテクチャに直接応用できる。また、人間のレビューを介さないコードデプロイが増える状況では、監査ログの自動生成・整合性検証の需要がさらに高まると考えられる。

## アイデア

- 「dreaming」機能：エージェントがノートを書き残し後続エージェントが学習する非同期的知識蓄積の仕組みは、LangGraphなどのマルチエージェント系で応用可能な記憶共有パターン
- 「ClaudeがClaudeにプロンプトを打つ」という自己ループ構造は、LLM-as-judgeやRLAIFと組み合わせることで人間フィードバック不要の品質保証サイクルとして設計できる
- コードレビューを人間が行わないPRが増加している現実は、静的解析・脆弱性スキャン・監査トレースを自動化するツールチェーンの重要性を高める

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **自律エージェントループ** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Pull Request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 関連記事

- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_2541 なぜLLM AIにはリファクタリングを「委任」してはいけないのか？
- /deep_2205 なぜAnthropicは軍と戦う？1億ドルPartner NetworkとAI研究所の全貌
- /deep_3092 その生産性向上、現場が静かに支払っているコストの話
- /deep_3504 harness engineering を5層で整理する — Pythonで1から書いて見えたこと

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
