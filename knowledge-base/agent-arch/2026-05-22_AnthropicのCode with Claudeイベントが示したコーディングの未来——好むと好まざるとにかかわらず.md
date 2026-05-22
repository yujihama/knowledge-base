---
title: "AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-22
tags: [Claude Code, AI coding, dreaming, autonomous agent, pull request, vibe coding, LLM-as-engineer]
category: "agent-arch"
related: [4374, 6170, 4233, 1429, 4753]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-22T09:16:53.907276"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeという2日間の開発者向けイベントを開催した。登壇したAnthropicエンジニアのJeremy Hadfieldが会場に質問したところ、半数近くの参加者が「Claudeが完全に書いたPull Requestをレビューせずにそのままシップした」と回答した。これはAIコーディングツールの浸透度を象徴する場面だった。

AnthropicのClaude Code責任者Boris Chernyは基調講演で、今後のデフォルトは「Claude Code自身がClaudeにプロンプトを送る」自律ループであると述べた。人間の開発者はエラーメッセージを見ることなく、Claude Codeがテストと修正を繰り返して問題を解決する設計を目指している。

新機能として「dreaming」が紹介された。これはClaude Codeエージェントが作業中に取ったメモを後続エージェントが参照できる仕組みで、特定コードベースへの習熟を積み上げていく。dreamingシステムはこれらのメモを横断的に読み込み、パターンや共通の問題を抽出・統合することで、コードベース固有の知識を蓄積する。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが登壇し、Claude Codeを中心に開発体制を再構成した事例を共有した。「Anthropicのソフトウェアの大部分は現在Claudeが書いている」「Claude CodeのコードはClaudeが書いた」とHadfieldは述べた。

一方で会場外では懸念も広がっている。RedditやHacker Newsでは、AIが生成したコードのレビュー負担増、開発者自身のコーディング能力の低下、セキュリティ脆弱性の増加といった問題が議論されている。Claude engineeringリードのKatelyn Lesseは「旧来のソフトウェア開発ベストプラクティスはすべて今も有効」と述べつつ、急増するコード量に技術マネージャーが疲弊していることも認めた。また「現在のClaudeはミッドレベルエンジニア程度の実力」と評価し、将来的にはClaudeがClaudeを構築できる状態を目指すとClaudeプロダクトリードのAngela Jiangが語った。

監査エージェント開発への示唆としては、dreamingのような「エージェント間メモ共有によるコードベース習熟の蓄積」は、監査ワークフロー内での知識継承メカニズムとして応用可能性がある。また、「AIが生成したアウトプットの人間によるレビュー省略」問題は監査品質管理と直結しており、AI出力の信頼性評価フレームワーク設計に示唆を与える。

## アイデア

- dreamingメカニズム：複数のコーディングエージェントが残したメモを横断的に統合し、コードベース固有の知識をエージェント間で継承する設計は、マルチエージェントシステムにおける分散記憶の実用例として注目に値する
- 「Claude自身がClaudeにプロンプトを送る」自律ループ：人間介在なしにテスト→修正→テストを繰り返すアーキテクチャは、エージェントの自己評価・自己修正ループ設計の具体的モデルになる
- AIコード生成の品質管理問題：レビューなしでシップされるコードが増えることで、AI出力の信頼性・セキュリティを担保するための評価フレームワーク（LLM-as-judge的アプローチ）の必要性が高まっている

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Pull Request** → /deep_1665 Hugging Face Hubにプルリクエストとディスカッション機能が追加
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **LLM自律ループ** (TODO: 読むべき)
- **コードレビュー** → /deep_2626 Vibe-Coding：人間のコードレビューなしにフィードバックベースの自動検証を実現する可能性研究

## 関連記事

- /deep_4374 Re:TechTalk#19 参加レポート：AI-DLCでClaude Codeと要件定義してみた
- /deep_6170 Google I/O 2026に向けた期待：コーディングAIの挽回、科学AI、業界ドラマ
- /deep_4233 AIにテストを丸投げしてはいけない理由と、その先の付き合い方
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌

## 原文リンク

[AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
