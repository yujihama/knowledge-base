---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好む好まざるにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-06-02
tags: [Claude Code, マルチエージェント, Dreaming, Claude Managed Agents, コーディング自動化, プルリクエスト, AI開発ツール]
category: "agent-arch"
related: [5496, 4753, 6745, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-06-02T09:18:08.943455"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeと題した2日間の開発者向けイベントを開催した。同日にGoogleがPalo AltoでI/Oを開催するという偶然の一致の中、Anthropicはコーディング自動化の現状と今後の方向性を披露した。

イベントの冒頭、AnthropicエンジニアのJeremy Hadfieldがステージから参加者に問いかけた。「先週、Claudeが完全に書いたプルリクエストをシップした人は？」——会場の約半数が手を挙げた。続けて「コードを全く読まずにシップした人は？」という問いにも、多くの手が残ったままだった。これはAIコーディングツールの普及がすでに「コードを読まずに本番リリース」という段階に達しつつあることを示している。

Claude Codeのリード Boris Chernyは基調講演で、Anthropicの目標を「人間がプロンプトを打つのではなく、Claudeが自分自身にプロンプトを打つ」設計への移行と説明した。エラーメッセージの処理もClaudeが自律的に行い、テストと修正を繰り返すことで人間の介入を最小化するというビジョンだ。

注目の新機能として「Dreaming」が紹介された。これはClaude Managed Agents（マルチエージェントシステム構築・実行のためのクラウド基盤）の機能であり、Claudeエージェントがタスク固有の情報をノートとして記録・保存し、後続エージェントがそれを参照してコードベースへの理解を蓄積できる仕組みだ。Dreamingはこれらのノートを横断的に読み込んでパターンや共通の問題を抽出し、エージェントがコードベースへの熟練度を高めていけるように設計されている。

参加企業にはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが名を連ね、Claude Codeを中心に開発チームを再編した事例が紹介された。

一方でイベント外では批判的な声も上がっている。HackerNewsやRedditでは「管理職が生産性向上を追求してAIツールを押し付けるが、実際にはレビューすべきコードが増えて開発が困難になっている」という意見が散見される。また、AIへの依存によりエンジニア自身のコーディング能力が低下するリスクや、AIが生成するコードのセキュリティ脆弱性も指摘されている。

Claude engineering leadのKatelyn Lesseは「従来のソフトウェア開発のベストプラクティスは依然として有効であり、見失われてはいけない」と述べつつ、大量コード生成によって技術マネージャーが疲弊しているという現実も認めた。また「現在のClaudeはミドルレベルのエンジニアと同程度のコード品質を持つ」とし、最終的にはClaudeが自分自身のコードをビルドできるようになることが目標と述べた。

監査AI開発への示唆としては、Dreamingのような「エージェント間の知識共有・蓄積機構」はLangGraphベースの監査エージェントシステムにも応用可能であり、タスク横断的なパターン認識と誤り学習の仕組みとして参考になる。また、コードレビューなし本番リリースの常態化は内部統制上のリスクであり、AIコード生成の監査統制設計という新たな課題領域を示唆している。

## アイデア

- Dreamingはエージェントが過去タスクのノートを横断的に読み込んでパターンを抽出する仕組みで、コードベース固有の暗黙知をエージェント間で継承・蓄積できる設計である
- 「人間がプロンプトを打つのではなくClaudeが自分自身にプロンプトを打つ」というself-promptingの設計思想は、エージェントの自律ループ設計における重要な方向性を示している
- コードを読まずに本番リリースが常態化しつつある現状は、AIコード生成に対する内部統制・監査統制の設計が新たな必須要件になりつつあることを示唆する

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **プルリクエスト** → /deep_1665 Hugging Face Hubにプルリクエストとディスカッション機能が追加
- **LLMコーディング補助** (TODO: 読むべき)
- **Claude Managed Agents** → /deep_2364 Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好む好まざるにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
