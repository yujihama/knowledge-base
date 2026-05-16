---
title: "Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす"
url: "https://zenn.dev/solvio/articles/7f8d2008526234"
date: 2026-04-19
tags: [Claude Managed Agents, Anthropic, エージェントループ, SSE, サンドボックス, agent_toolset_20260401, Python SDK, フルマネージド]
category: "agent-arch"
related: [593, 2278, 1407, 1679, 1629]
memo: "[Zenn LLM] Claude Managed Agentsを触ってみた"
processed_at: "2026-04-19T12:44:58.861498"
---

## 要約

2026年4月にAnthropicがパブリックベータとしてリリースした「Claude Managed Agents」の概要と実装例を紹介する記事。従来のMessages APIはテキストの入出力のみを担うのに対し、Managed AgentsはAnthropicが管理するクラウドコンテナ上でClaudeが自律的に動作し、ファイル操作・シェルコマンド実行・Web検索まで一括して担う。開発者が自前で構築する必要があったサンドボックス環境、エージェントループ、ツール実行基盤、セッション管理、セキュリティ制御をすべてAnthropicが提供する点が最大の特徴。

システムは3つのコア概念で構成される。①Agent（モデル・システムプロンプト・ツールの定義）、②Environment（実行コンテナの設定。ネットワークアクセスはunrestrictedかlimited選択可）、③Session（AgentとEnvironmentを紐付けた実行インスタンス）。エージェントとアプリ間の通信はSSEによるリアルタイムストリーミングで行われる。

`agent_toolset_20260401`を指定することで、bash・read・write・edit・glob・grep・web_fetch・web_searchの8ツールが一括有効化される。個別ツールのon/offも設定可能。料金はセッション時間あたり$0.08が目安とされる。

実装例として「Web検索→情報整理→Markdownファイル書き出し」タスクをPythonで実行。`client.beta.agents.create()`でエージェント定義→`client.beta.environments.create()`で環境作成→`client.beta.sessions.create()`でセッション起動→`client.beta.sessions.events.send()`でメッセージ送信→`client.beta.sessions.events.stream()`でストリーミング受信、という流れ。`python run_agent.py`1コマンドだけで、Web検索2回・ファイル書き出し・内容確認まで自律実行された。

設計思想として、Anthropicは「エージェントハーネスはモデル進化とともに陳腐化する」課題に対応するため、OSがハードウェアを抽象化したアーキテクチャを採用。Session（追記専用ログ）・Harness（エージェントループ）・Sandbox（分離実行環境）を仮想化レイヤーとして提供する。

制限事項として、モデルがClaudeに限定されること、長時間・並列実行時のコスト急増リスク（$200/月のMaxプランが$1,000〜$5,000相当の計算量を消費したケースも報告）、ベータ段階での仕様変更リスクが挙げられる。監査エージェント開発への示唆として、自前でエージェントループ・サンドボックスを構築するコストを大幅削減できる点は注目に値するが、Claudeロックインとコスト構造の事前評価が必須。

## アイデア

- エージェントハーネスをOSのハードウェア抽象化レイヤーに例えた設計思想：モデルアップグレードごとにハーネスの前提が無効化される問題を、Session/Harness/Sandboxの仮想化レイヤーで解決するアプローチは、監査エージェントのメンテナンスコスト削減に直結する
- agent_toolset_20260401という日付入りのツールセット識別子：将来のツールセットバージョニング戦略を示唆しており、APIの後方互換性維持とエージェント動作の再現性確保の設計意図が読み取れる
- 生成ファイルはローカルではなくAnthropicのクラウドコンテナに保存され、セッションIDが生きている間は状態が保持される：長時間タスクの中断・再開やマルチステップ監査ワークフローへの応用可能性がある

## 前提知識

- **Messages API** → /deep_1517 Claude Codeが『言ってもいない指示』を実行する — ロール混同バグの構造と対策
- **エージェントループ** → /deep_64 Open Responses: オープンな推論APIスタンダードの概要
- **SSEストリーミング** (TODO: 読むべき)
- **サンドボックス実行環境** (TODO: 読むべき)
- **Anthropic SDK** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編

## 関連記事

- /deep_593 国防総省のAnthropicに対するカルチャーウォー戦術は裏目に出た
- /deep_2278 仕事とAIの関係を実際に解明できる唯一のデータとは何か
- /deep_1407 ペンタゴンのAnthropicへのカルチャー戦争戦術は裏目に出た
- /deep_1679 ペンタゴンのAnthropicへのカルチャーウォー戦術は裏目に出た
- /deep_1629 ペンタゴンのAnthropicへの「文化戦争」戦術は裏目に出た

## 原文リンク

[Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす](https://zenn.dev/solvio/articles/7f8d2008526234)
