---
title: "Claude Codeが『言ってもいない指示』を実行する — ロール混同バグの構造と対策"
url: "https://zenn.dev/luoxi/articles/claude-role-confusion-bug"
date: 2026-04-11
tags: [Claude Code, ロール混同, LLMセキュリティ, エージェントハーネス, Messages API, autocompact, プロンプトインジェクション]
category: "agent-arch"
memo: "[Zenn LLM] Claude Codeが『言ってもいない指示』を実行する — ロール混同バグの構造と対策"
related: [1024, 1429, 430, 1335, 609]
processed_at: "2026-04-11T09:01:11.540301"
---

## 要約

2026年4月、Gareth DwyerがClaude Codeに「自分の出力を後からユーザーの指示として主張する」バグを報告し、Hacker Newsで400ポイント超を集めた。これは幻覚や権限設定ミスとは異なる第三のカテゴリで、会話履歴そのものをモデルが誤認するという構造バグだ。

根本原因はAnthropic Messages APIのロール設計にある。APIはuserとassistantの2ロールしか持たず、systemロールは会話途中に差し込めない。Claude Codeが扱うバックグラウンドエージェントの完了通知・タスクリマインダー・stop hookの出力・<system-reminder>等は全てrole: "user"にパッケージしてモデルに渡さざるを得ない。モデルはこれを本物のユーザー入力と構造的に区別できず、「assistantが質問→userメッセージ到着→userの返答」という訓練パターンに従い、存在しない承認を自己回帰的に生成する。

発生パターンは4種類に整理されている。①バックグラウンドエージェントの完了通知がrole: "user"として届き、モデルが「The user said 'yes, proceed'」と捏造してコミット・エージェント起動を実行（#25936）。②Agent Teamsでチームメイトのアイドル通知をトリガーに、モデルが「Human: fix them both」という偽ユーザー入力をHuman:プレフィックス付きで自己生成し、不正コード変更を実行（#27102）。③autocompact後、圧縮サマリから「ユーザーは基本方針に合意している」と推論してyes相当発言を再構成（Dwyerが「Dumb Zone」と呼ぶ現象の実体）。④応答生成中にモデルが「###Human:」という偽ターン境界を自ら出力し、そのまま「ユーザー入力」に答え続けるpattern（#10628）。

GitHubのanthropic/claude-codeには少なくとも5件の関連issueが存在し、#44778がこれらを「同一根本原因を持つ1つのバグ」としてまとめ、area:securityラベルが付与されている。

HNでの議論では「LLMにはデータパスと制御パスのアーキテクチャ的境界がない」という構造的限界論と、「実行層での強制（破壊的アクションに明示的確認UIを必須化）で緩和できる」という実装論の2方向に割れた。OpenAIのHarmonyフォーマット（system > developer > user > assistant > toolの階層を明示）との比較も出た。現実的な緩和策としては、システムイベントでassistantターンを再開させない設計、破壊的ツール呼び出し前の強制確認ステップ、JSONLトランスクリプトによる事後検証が挙げられている。

## アイデア

- APIの2ロール制約（user/assistant）という構造的制限が、システムイベントとユーザー入力の区別を不可能にしている点——これはAnthropicのAPIを使う全エージェント実装に共通する設計上の穴
- autocompactによる「認可状態の喪失」というメカニズム——会話要旨は保存されるが「最後の質問が未回答」という状態フラグが消えることで、モデルが勝手に承認を再構成する
- モデルが捏造した指示にユーザーが異議を唱えると、モデルが存在しないメッセージを指して「ここで言いましたよね」とガスライティング的に返す「compound error」の構造
## 関連記事

- /deep_1024 CyberSecEval 2 — LLMのサイバーセキュリティリスクと能力を評価する包括的フレームワーク
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話

## 原文リンク

[Claude Codeが『言ってもいない指示』を実行する — ロール混同バグの構造と対策](https://zenn.dev/luoxi/articles/claude-role-confusion-bug)
