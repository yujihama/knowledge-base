---
title: "「並列は速い」は本当か──subagent 76% DENIED検証とCladeの選択"
url: "https://zenn.dev/satoh_y_0323/articles/7869b9a7f318ec"
date: 2026-04-23
tags: [Claude Code, subagent, parallel execution, permissions, race condition, Clade, multi-agent, worktree]
category: "agent-arch"
related: [2537, 43, 609, 2254, 1736]
memo: "[Zenn LLM] 「並列は速い」は本当か──subagent76%DENIED検証とCladeの選択"
processed_at: "2026-04-23T12:09:43.489706"
---

## 要約

Claude Code上で動作するエージェントフレームワーク「Clade」の開発者が、並列subagentで頻発する「Permission to use Bash/Write has been denied」エラーの真因を72セッション分のログ解析から特定し、並列実行機能を完全廃止するまでの記録。

当初は「heredocの文字数が長すぎる（1〜2万字）」という仮説のもと、1回のBash実行を2000文字以内に制限するルールを導入（v1.18.3）。次に「絶対パスがpermissionsパターンにマッチしない」という問題を発見し相対パス必須ルールを追加（v1.18.4）。どちらも頻度を下げる効果はあったが根本解決にならなかった。

決定的な検証は「同一コマンドの単独実行vs並列実行比較」。Bash 2,365文字の全く同じコマンドを、並列subagentから呼ぶとDENIED、親Claudeが単独で実行すると成功という結果を3回再現。さらにBashをWriteツールに切り替えても同様にDENIEDが発生（17,853文字と15,978文字の書き込みがどちらも拒否）したことで、特定のツールの問題ではなくClaude Codeのpermissionsチェッカー全体に並列処理時のrace conditionがあるという結論に至った。

過去72セッションの.claude/projects/以下のJSONLを全件grepした集計では、並列subagentを使用したセッションの76%（55件）で何らかのDENIEDが記録されており、Bash DENIEDが累計約100件、Write DENIEDが累計約90件。これまで表面化しにくかった理由は、多くのエージェントがDENIED後に自力で別アプローチへ切り替えて処理を継続するため、外から見ると「動いている」ように見えていたからだった。

DENIED後のリトライ・回避試行（Write 17KB再生成、Bash代替パス探索等）はすべてトークンを消費し、回避経路が毎回異なるため結果の予測可能性も低い。「速さ」の恩恵より、トークン浪費・サイレントバグリスク・ユーザーが失敗に気づけない構造的問題のほうが大きいと判断し、v1.19.0でworktree-developer・merger・parallel_groupsモード等の並列実行機能を全廃。v1.20.0ではレポート出力フローの全エージェント共通化、plannerのモード判定をファイル有無からタイムスタンプ比較へ変更、「現サイクル＝最新plan-reportのタイムスタンプ以降」という概念の導入によりシンプル化を図った。監査エージェント開発観点では、並列処理の信頼性検証なしに並列化を採用するリスクと、予測可能な直列実行の価値を実データで示した事例として参考になる。

## アイデア

- Claude Codeのpermissionsチェッカーに並列subagent処理時のrace conditionが存在し、コマンド内容・ツール種別に関わらず確率的にDENIEDが発生する──これは単独実行vs並列実行の対照実験で初めて可視化できる種類のバグ
- DENIED後のエージェントの自律的リトライ・回避行動が「表面上は動いている」状態を作り出し、フレームワーク作者すら72セッション分のログを掘るまで気づけなかったというサイレントバグの構造的危険性
- 時間効率（並列）vs トークン効率・予測可能性・結果品質（直列）のトレードオフを実測値で定量化し、76%という失敗率を根拠に「速さを捨てて予測可能性を取る」という設計判断を下した意思決定プロセス

## 前提知識

- **Claude Code subagent** (TODO: 読むべき)
- **permissions チェッカー** (TODO: 読むべき)
- **race condition** (TODO: 読むべき)
- **worktree** → /deep_2537 サブエージェントが実はレポートを書けていなかった──Clade v1.17.1〜v1.18.1
- **heredoc** (TODO: 読むべき)

## 関連記事

- /deep_2537 サブエージェントが実はレポートを書けていなかった──Clade v1.17.1〜v1.18.1
- /deep_43 AI社員8人で取締役会を開いたら、完全に人間の組織論だった件
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- /deep_2254 同僚の「細かすぎた」が機能になった──Cladeが育つ仕組み【v1.15.0】
- /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話

## 原文リンク

[「並列は速い」は本当か──subagent 76% DENIED検証とCladeの選択](https://zenn.dev/satoh_y_0323/articles/7869b9a7f318ec)
