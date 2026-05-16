---
title: "限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌"
url: "https://zenn.dev/53able/articles/a7b1ee26745302"
date: 2026-05-09
tags: [oh-my-claudecode, マルチエージェント, Claude Code, オーケストレーション, 並列実行, verifier, モデルルーティング, ReAct]
category: "agent-arch"
related: [3186, 3671, 3490, 3217, 3532]
memo: "[Zenn LLM] 限界ClaudeCodeユーザーの私がoh-my-claudecodeを調べてみた"
processed_at: "2026-05-09T21:01:20.087599"
---

## 要約

oh-my-claudecode（OMC）は、Claude Code上で動作するマルチエージェントオーケストレーションフレームワーク。「あなたは演奏者ではなく指揮者だ」というコンセプトのもと、単一エージェントの限界（有限コンテキスト・役割過負荷・領域転移の脆さ）を複数エージェントの並列分業で克服する。

導入はClaude Codeセッション内から`/plugin marketplace add`と`/plugin install`の2コマンド、またはnpm経由で完了。初期セットアップは`/omc-setup`ウィザードが自動実行する。

実行モードは用途別に6種類。`autopilot:`はAnalyst→Architect→Executor→UltraQA（検証フェーズ全体）の4段階パイプラインで「要件分析から実装・検証まで」を一括処理。`ralph:`はverifierエージェントがOKを出すまでループを継続する完了保証モードで、AgentForge論文の「実行結果根拠の検証を第一原則とする」手法を実装し、単一エージェントベースラインを26〜28ポイント上回る。`ulw`（ultrawork）は5つ以上のエージェントを同時並走させ、DynTaskMAS論文が示す21〜33%の実行時間短縮を実現。`/team N:role`は指定人数×役割のエージェントチームをplan→prd→exec→verify→fixの5ステージパイプラインで動かす（要`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:1`設定）。

モデルルーティングは自動最適化。explore・writerにはHaiku、executor・debuggerにはSonnet、architect・critic・analystにはOpusを振り分け、CASTER論文の手法に基づき推論コストを最大72.4%削減する。

付加機能として、セッション中の解決策をYAMLスキルとして`.omc/skills/`に保存しチーム共有できる`/learner`、APIレート制限時の自動待機再開`omc wait`、Issue番号からgitワークツリーを一発生成する`omc teleport`、Telegram/Discord/Slack通知対応の`/configure-notifications`、エージェント稼働状況をリアルタイム表示するHUD（`omc hud --watch`）がある。

HUDは`[OMC#4.13.5] | 5h:61%(3h44m) wk:81%(1d6h) | ctx:65% | 🔧235 🤖14 ⚡8`の形式で、5時間枠・週次枠の使用率、コンテキスト消費率、ツール/エージェント/スキル呼び出し累積回数を表示。ctx70%でアラート、85%超で圧縮検討が目安。

監査エージェント開発への示唆：plan→prd→exec→verify→fixのパイプライン設計は、監査ワークフロー（リスク評価→手続設計→証拠収集→検証→報告）に直接対応する構造。verifierループによる完了保証は、監査証拠の充足性判定への応用が考えられる。役割別モデルルーティングは、重い判断（audit opinionはOpus）と軽い定型処理（データ抽出はHaiku）の自動コスト配分に転用できる。

## アイデア

- verifierエージェントがOKを出すまでループし続けるralphモードは、監査証拠充足性の自動判定ループとして転用できる設計パターン
- タスク難易度に応じてOpus/Sonnet/Haikuを自動振り分けするモデルルーティングは、コスト最適化の実装として即座に参考になる（CASTER論文で最大72.4%削減）
- `.omc/skills/`にYAMLでスキルを蓄積しチーム共有する仕組みは、ナレッジベースのコンテキスト自動注入の実装例として応用可能

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **LLMオーケストレーション** → /deep_4 DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する
- **tmux** → /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話

## 関連記事

- /deep_3186 エージェントオーケストレーション：マルチエージェントAIが変えるホワイトカラー業務の全貌
- /deep_3671 エージェントオーケストレーション：今のAIで重要な10のこと
- /deep_3490 エージェントオーケストレーション：今AIで重要な10のこと｜MIT Technology Review
- /deep_3217 エージェントオーケストレーション：今AIで重要な10のこと（MIT Technology Review）
- /deep_3532 エージェントオーケストレーション：今AIで重要な10のこと

## 原文リンク

[限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌](https://zenn.dev/53able/articles/a7b1ee26745302)
