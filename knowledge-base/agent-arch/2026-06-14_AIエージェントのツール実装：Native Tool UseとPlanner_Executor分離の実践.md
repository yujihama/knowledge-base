---
title: "AIエージェントのツール実装：Native Tool UseとPlanner/Executor分離の実践"
url: "https://zenn.dev/shuzan/articles/5f83a5ab3fbcd8"
date: 2026-06-14
tags: [tool-use, function-calling, Claude Sonnet, Claude Haiku, multi-agent, prompt-injection, JSON Schema, SSE, TypeScript, planner-executor]
category: "agent-arch"
related: [1561, 31, 77, 526, 55]
memo: "[Zenn LLM] AIエージェントのツール実装に関して"
processed_at: "2026-06-14T09:04:43.695484"
---

## 要約

本記事は、個人秘書AIアプリ「結衣」のエージェント設計を技術的に詳述したもの。Claude Code + MCPによる外部SaaS連携から脱却し、機能をアプリ内に自前実装した理由と、その実現手段としてのtool use設計を解説する。

エージェントの中核はAnthropicのNative Tool Use（function calling）。各ツールはTypeScriptで`ToolDef`型として定義され、`name`・`description`・`input_schema`（JSON Schema）・`handler`に加え、`callableBy`・`surface`・`allowedModes`・`confirmationPolicy`・`untrustedOutput`などのセキュリティメタデータを持つ。descriptionとinput_schemaがモデルへのプロンプトそのものとなるため、ツール記述のチューニングが秘書機能の品質を左右する。

実行ループはシンプルなwhileループ：ツール一覧をAnthropicのmessages.createに渡す→モデルがtool_useを返す→handlerを実行→tool_resultをメッセージに積む→繰り返す。最大反復数（MAX_ITER）で無限ループを防止。

最大の工夫が「3軸フィルタ（toolsForContext）」。数十個のツールを毎ターン3軸で絞り込む：①`mode`（normal/timer/background）でタイマー発火時は削除系ツールを除外、②`caller`でメインエージェントと専門エージェントの権限を分離、③`isAvailable()`でGoogle未連携時はgcal_*系ツールを非表示。これによりコンテキスト節約・誤用防止・権限制御を同時に実現。

アーキテクチャはメイン結衣（Claude Sonnet）＋専門エージェント（Claude Haiku）の二段構成。メインはask_mail_specialist/ask_schedule_specialistといった傘ツールのみを持ち、Haikuサブエージェントがgcal_list_events等のドメイン固有ツールを独自ループで処理。狙いはコンテキストの軽量化・コスト削減・権限境界の明確化。

同期/非同期の使い分けも重要：web_fetchのような即値が必要なものはその場で同期実行、ask_*_specialistはバックグラウンドにディスパッチしてSSEで結果を返却。不可逆操作（削除・メール送信）にはWorkflow型の確認フローを組み込み、untrustedOutput=trueのツール露出時はシステムプロンプトにプロンプトインジェクション対策ガードを自動挿入する。

監査エージェント開発への示唆：本設計のcallableBy/surface/confirmationPolicyによる権限制御とワークフロー型確認フローは、不可逆な監査アクション（証跡の作成・修正・削除）の制御に直接応用可能。ツールのメタデータから防御ロジックを自動生成する手法は、監査エージェントの統制設計として参考になる。

## アイデア

- ツールのメタデータ（surface/untrustedOutput/confirmationPolicy）からセキュリティガードとプロンプトインジェクション対策を自動生成する設計：ツールを追加するだけで防御が自動付与される
- 3軸フィルタ（mode/caller/availability）による動的ツール絞り込み：コンテキスト節約と権限制御を同一メカニズムで実現し、タイマー発火時の誤操作リスクを構造的に排除
- 同期・非同期ディスパッチの使い分けとSSEによる非同期応答：ask_*_specialistをバックグラウンド実行してメインの応答レイテンシを下げながら、専門エージェントが独立したtool useループを回すオーケストレーション設計

## 前提知識

- **Native Tool Use / Function Calling** (TODO: 読むべき)
- **Anthropic Messages API** (TODO: 読むべき)
- **JSON Schema** → /deep_6556 RustでLLMコードレビューエージェントを作った
- **Planner/Executor パターン** (TODO: 読むべき)
- **SSE（Server-Sent Events）** (TODO: 読むべき)

## 関連記事

- /deep_1561 リーダーシップクラスシステムにおける高スループット材料スクリーニングのためのマルチエージェントオーケストレーション
- /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- /deep_77 パーソナルヘルスエージェントの解剖：マルチエージェント構造による個人健康支援フレームワーク
- /deep_526 Consilium: 複数LLMが協調して意思決定するマルチLLMプラットフォーム
- /deep_55 AprielGuard: 現代LLMシステムにおける安全性と敵対的ロバスト性のためのガードレール

## 原文リンク

[AIエージェントのツール実装：Native Tool UseとPlanner/Executor分離の実践](https://zenn.dev/shuzan/articles/5f83a5ab3fbcd8)
