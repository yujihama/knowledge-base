---
title: "AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-26
tags: [Claude Code, Claude Managed Agents, Dreaming, multi-agent, 自律コーディング, vibe-coding, human-in-the-loop]
category: "agent-arch"
related: [5496, 609, 31, 3828, 5159]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-26T21:27:10.795337"
---

## 要約

2026年5月19日、AnthropicはロンドンでGoogle I/Oと同日に開発者向けイベント「Code with Claude」を開催した。登壇したAnthropicエンジニアのJeremy Hadfieldが「先週Claudeが完全に書いたPRをシップした人は？」と問うと会場の約半数が挙手し、「コードを一切読まずにシップした人は？」という問いでも大半の手が下がらなかった。AnthropicはClaudeが現在自社コードの大半を書いていると公言している。

Claude CodeヘッドのBoris Chernyはキーノートで「デフォルトは『Claudeにプロンプトを送る』ではなく、『ClaudeがClaudeにプロンプトを送る』になった」と述べ、人間がエラーメッセージを見ることなくClaudeがtest-and-tweakループを自律的に繰り返す完全自動化を目標として掲げた。

新機能として「Dreaming」が発表された。これはClaude Managed Agents（クラウドベースのマルチエージェント基盤）の機能で、コーディングエージェントがタスク実行中に自己メモを書き残し、後続エージェントがそのノートを読んでコードベースの知識や過去のエラーを学習できる仕組み。Dreamingはこれらノートを横断的に解析しパターンや共通課題を抽出することで、エージェント群が特定コードベースへの習熟度を継続的に向上させる設計になっている。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが登壇し、開発チームをClaude Code中心に再編した事例を紹介。会場内に懸念の声はなかったとされる。

一方、会場外ではRedditやHacker Newsで「生成コードは管理職がKPI目的で押しつけているだけ」「レビュー量が増えて開発が難しくなった」「コーディング能力が落ちた」といった声も上がっている。セキュリティ研究者はAIツールが脆弱なコードを生成しやすいとも警告している。

Claude engineering leadのKatelyn Lesseは「旧来のソフトウェア開発ベストプラクティスは依然有効だが、多くのチームが見失っている」とコメント。「現時点でClaudeはミッドレベルエンジニア程度のコード品質」としつつ、システム設計やトラブルシューティングには依然エキスパートが必要と述べた。Claude product leadのAngela Jiangは「最終目標はClaudeが自分自身をビルドできるようになること」と明言した。

監査エージェント開発への示唆として、Dreamingのようなエージェント間知識共有・自己改善ループは、監査ナレッジの蓄積・再利用に直接応用可能なアーキテクチャパターンである。また「人間がコードを読まずにシップ」という現象は、AIが生成した監査根拠や判定をレビューなしに採用するリスクと構造的に同質であり、監査AIにおけるヒューマン・イン・ザ・ループ設計の重要性を改めて示している。

## アイデア

- Dreamingはエージェントが自己メモを書き残し後続エージェントが学習するという、エージェント間の非同期知識継承メカニズムであり、監査ナレッジベースの自動蓄積に応用できる
- 「ClaudeがClaudeにプロンプトを送る」という自己指示ループは、エージェントのメタ認知層として捉えられ、ReActやLangGraphの自律反復パターンの延長線上にある
- コードを読まずにPRをシップする開発者が半数を超えるという現象は、AIが生成した成果物に対する人間の監視機能が急速に形骸化しつつあることを示しており、監査AIの設計原則（説明可能性・承認フロー）の重要性を裏付ける

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **Claude Managed Agents** → /deep_2364 Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け
- **human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- /deep_3828 エージェントオーケストレーション：今のAIで重要な10のこと
- /deep_5159 エヴァで理解するAIエージェント組織論：NERVとMAGIとゼーレ、あなたはどこから設計する？

## 原文リンク

[AnthropicのCode with Claudeが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
