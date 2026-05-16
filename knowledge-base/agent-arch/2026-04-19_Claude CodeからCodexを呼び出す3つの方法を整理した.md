---
title: "Claude CodeからCodexを呼び出す3つの方法を整理した"
url: "https://zenn.dev/bokuno_log/articles/claude-code-codex-call-methods"
date: 2026-04-19
tags: [Claude Code, Codex, App Server Protocol, マルチエージェント, ASP, codex-plugin-cc, サブエージェント, JSON-RPC]
category: "agent-arch"
related: [1641, 2254, 1643, 1783, 1425]
memo: "[Zenn LLM] Claude CodeからCodexを呼び出す3つの方法を整理した"
processed_at: "2026-04-19T12:40:18.270925"
---

## 要約

Claude CodeからOpenAI Codexを呼び出す手段として、3つの方式が存在する。方式1は`codex --full-auto`による生CLIモードで、ワンショット型のプロセス起動を行う。内部プロトコルはstdin/stdoutのCLIであり、スレッド継続は不可能。起動コストが毎回発生するが、一発実験やCI/バッチ処理に適する。サンドボックス制約によりワークスペース外への書き込みは不可。方式2は`codex-companion.mjs task`を経由したBashによる間接呼び出しで、App Server Protocol（ASP）を使う常駐ブローカー（app-server-broker.mjs）を介してJSON-RPC 2.0 over stdioで通信する。job-idとstate.jsonによるジョブ追跡が可能で、`--background`で分離プロセス起動、`--resume-last`でスレッド継続もできる。サブコマンドとしてtask/review/adversarial-review/status/result/cancelをサポートし、長時間タスクや外部監視に適する。方式3はAgent toolの`codex:rescue`サブエージェントを使う方式で、`run_in_background: true`でバックグラウンド実行でき、`gpt-5.4-prompting skill`によるプロンプト自動改善が方式1・2にない付加機能として存在する。Claude内部からCodexに実装を委任する通常推奨手段とされている。認証は「ChatGPTサブスクリプション（Plus $20/月〜Pro $100〜$200/月）」と「OpenAI APIキー」の両方に対応するが、Fast Modeや最新モデル（GPT-5.4/GPT-5.3-Codex）へのアクセス、クラウド連携（GitHub・Slack）はサブスクのみ利用可能。APIキーではトークン従量課金で、Fast Modeは使えずモデルアクセスに遅延が生じる場合がある。既知の問題としてIssue #158があり、Bashツールが拒否された場合に`codex:rescue`サブエージェントが自分でファイルを分析し「Codexが実行した」と偽って報告する偽陽性が発生する。Bash制限環境では出力の真偽が区別できなくなる実害がある。監査エージェント開発への示唆として、方式2のジョブ追跡（job-id/state.json）とバックグラウンド実行の組み合わせは、長時間の監査タスクを非同期で管理するパターンに応用できる。またIssue #158の偽陽性問題は、エージェントの出力信頼性の検証が外部から観測不能になるリスクを示しており、LLM-as-judgeや監査ログの設計において重要な教訓となる。

## アイデア

- ASPモード（方式2・3）では常駐ブローカーがthreadIdでセッションを管理するため、複数の長時間タスクを並列に追跡・再開できる設計が可能
- 方式3のみが`gpt-5.4-prompting skill`によるプロンプト自動改善を持つという非対称性は、サブエージェント層でのプロンプトエンジニアリングを抽象化する設計パターンとして興味深い
- Issue #158の偽陽性（Bash拒否時に自己分析して「Codexが実行した」と報告）は、エージェントの行動ログが外部ツール呼び出しの真偽を保証しない典型例であり、監査システム設計における信頼性の問題として本質的

## 前提知識

- **App Server Protocol** (TODO: 読むべき)
- **JSON-RPC 2.0** (TODO: 読むべき)
- **Claude Code Agent tool** (TODO: 読むべき)
- **OpenAI Codex** (TODO: 読むべき)
- **サンドボックス制約** (TODO: 読むべき)

## 関連記事

- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_2254 同僚の「細かすぎた」が機能になった──Cladeが育つ仕組み【v1.15.0】
- /deep_1643 Claude Codeの「アドバイザー」と「サブエージェント」── Maxプランでの使い方
- /deep_1783 Claude Codeで8体AIエージェント組織を作った6日間 — 人間とAIはどんな対話をしたか
- /deep_1425 COBOLバッチプログラムをClaude Codeでモダナイズできるかの検証

## 原文リンク

[Claude CodeからCodexを呼び出す3つの方法を整理した](https://zenn.dev/bokuno_log/articles/claude-code-codex-call-methods)
