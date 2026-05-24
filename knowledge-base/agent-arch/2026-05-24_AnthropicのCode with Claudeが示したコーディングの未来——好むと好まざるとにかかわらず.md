---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-24
tags: [Claude Code, AIコーディング, dreaming, 自律エージェント, 知識継承, 自動化, PR生成]
category: "agent-arch"
related: [2688, 2541, 6333, 6251, 6140]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-24T09:14:54.481677"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeという開発者向け2日間イベントを開催した。基調講演でClaude CodeのヘッドBoris Chernyは「デフォルトは『Claudeにプロンプトを送る』ではなく、『Claudeが自分自身にプロンプトを送る』になった」と述べ、人間の介入を最小化した完全自律的なコーディングを目指す方向性を明確にした。

イベント会場では、AnthropicエンジニアのJeremy Hadfieldが「直近1週間でClaudeが完全に書いたPRをshipした人は？」と問いかけると参加者の約半数が手を挙げ、さらに「コードを一切読まずにshipした人は？」という質問でも大半の手が下りなかった。Anthropic社内でも「ほとんどのソフトウェアはClaudeが書いており、Claude Code自体のコードもClaudeが大部分を書いた」と公言している。

技術的な注目点として、「dreaming」と呼ばれる新機能が紹介された。Claude Codeのエージェントが特定タスクに関するメモを自律的に記録・保存し、後続のコーディングエージェントがそのメモを参照してコードベースを素早く把握し、過去のエラーから学習できる仕組みだ。dreamingシステムはこれらのメモを横断的に読み込み、パターンや共通の問題点を抽出・統合することで、特定コードベースへの適応精度を継続的に向上させる。これはエージェントの長期記憶・知識継承の実装例として位置づけられる。

Spotify、Delivery Hero、Lovable、Monday.comなど複数企業が開発チームをClaude Code中心に再編した事例を発表。一方でイベント外部では、AIコーディングツールへの懸念も広がっている。Hacker News等では「生成コードを問題ないと言うのはコードを読んでいない人だけ」という批判や、開発者のコーディングスキル低下、AIが生成する安全でないコードによるセキュリティリスクが指摘されている。

Claude engineeringリードのKatelyn Lesseは「従来のソフトウェア開発のベストプラクティスは今も有効」と述べつつ、急速な自動化の進行によってAnthropicの技術マネージャーが増大するコードのレビューに疲弊していることも認めた。「現時点でClaudeはミドルレベルエンジニア程度のコード品質」とし、システム設計や難しい問題のトラブルシューティングには依然として専門家が必要だとした。最終的な目標としてClaudeが自分自身をビルドできる状態を目指すと表明している。

監査エージェント開発への示唆：dreamingのようなエージェント間のメモ共有・知識継承の仕組みは、監査エージェントが過去の監査結果・エラーパターン・判断ロジックを蓄積し、後続エージェントに引き継ぐアーキテクチャに直接応用できる。また「コードを読まずにshipする」実態が広がることで、AIが生成したコードの品質・セキュリティを自動検証する監査的役割の重要性が増す。

## アイデア

- dreamingは複数エージェント間でタスク固有のメモを共有・統合する長期記憶の実装であり、マルチエージェントシステムにおける知識継承パターンの具体例
- 「Claudeが自分自身にプロンプトを送る」という自己駆動型ループは、人間のフィードバックなしにテスト→修正→テストを繰り返すReActループの発展形
- AIが生成したコードを人間が読まずにshipする実態が常態化すると、コードの品質・セキュリティ・保守性を自動検証するレイヤーの需要が構造的に高まる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **AIコーディングエージェント** → /deep_3774 Claude Codeに「/create-design-md」を自作して、0→1開発のUIブレをなくした話
- **自律型エージェントループ** (TODO: 読むべき)
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **マルチエージェント協調** → /deep_3906 検証付きマルチエージェント協調：「計画・実行・検証・再計画」フレームワーク VMAO

## 関連記事

- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_2541 なぜLLM AIにはリファクタリングを「委任」してはいけないのか？
- /deep_6333 Google I/O 2026：コーディングAIでの挽回、科学AI、そして業界ドラマ
- /deep_6251 Google I/O 2026直前：コーディングAIでの遅れと科学AIでの強みを分析
- /deep_6140 Google I/O 2026のAI発表を読むエンジニア・研究視点

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
