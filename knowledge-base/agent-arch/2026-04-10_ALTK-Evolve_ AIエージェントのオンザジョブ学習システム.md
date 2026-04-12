---
title: "ALTK-Evolve: AIエージェントのオンザジョブ学習システム"
url: "https://huggingface.co/blog/ibm-research/altk-evolve"
date: 2026-04-10
tags: [episodic-memory, on-the-job-learning, ReAct, LangGraph, MCP, AppWorld, LangFuse, OpenTelemetry, CUGA, guidelines-extraction]
category: "agent-arch"
memo: "[HF Blog] ALTK‑Evolve: On‑the‑Job Learning for AI Agents"
processed_at: "2026-04-10T09:40:34.547774"
---

## 要約

ALTK-Evolveは、IBMリサーチが開発したAIエージェント向け長期エピソードメモリシステム。従来のエージェントは過去の実行ログをプロンプトに再注入するだけで「原則」を学べず、同じミスを繰り返す「永遠のインターン問題」を抱えていた。MITの研究によれば95%のパイロット失敗はエージェントがオンザジョブ学習できないことに起因するとされ、ALTK-Evolveはこの課題に正面から取り組む。

システムは2つのフローで動作する。下向きフロー（観測・抽出）では、LangfuseなどOpenTelemetryベースの観測基盤でエージェントの完全な軌跡（発話・思考・ツール呼び出し・結果）をキャプチャし、プラガブルなエクストラクタが構造的パターンをマイニングして候補エンティティとして保存する。上向きフロー（精錬・検索）では、バックグラウンドの統合ジョブが重複排除・弱いルール削減・実証済み戦略のブーストを行い、ガイドライン・ポリシー・SOP等の高品質ライブラリを構築。推論時にはJust-in-timeで関連項目のみをコンテキストに注入する。

AppWorldベンチマーク（平均9.5 API・1.8アプリを使う多段階タスク）での評価では、ReActエージェントに上位5件の検索済みガイドラインを付与した結果、全体SGC（シナリオゴール達成率）が50.0%→58.9%（+8.9pt）に改善。特にHardタスクは19.1%→33.3%（+14.2pt、相対74%向上）と複雑な制御フローへの効果が顕著だった。テスト未見タスクでも改善が確認され、レシピの暗記ではなく原則の汎化が起きていることを示している。

統合方法は3段階。Lite modeではClaude CodeプラグインとしてCLIコマンド2行で導入可能（ファイルシステムにエンティティを保存、Claude Codeのhooksで自動検索）。Low-codeでは`altk_evolve.auto`インポート1行でArize Phoenix UIへのトレース送信が可能で、OpenAI・LiteLLM・HFエージェント等に対応。Pro-codeではMCPを介してCUGAと統合し、`get_guidelines`と`save_trajectory`のMCPツールで学習ループを形成する。

## アイデア

- エージェント軌跡から「原則」を抽出し再利用可能なガイドラインライブラリを構築するアーキテクチャは、単なるログ再注入より汎化性が高く、HardタスクでSGC+14.2ptという定量的根拠がある
- スコアリングによるメモリのガベージコレクション（弱いルールの刈り込み・重複排除）で、コンテキスト肥大化を防ぎながら記憶の品質を維持する設計思想
- MCP経由で`get_guidelines`と`save_trajectory`の2ツールで学習ループを閉じるプロコード統合は、既存エージェントフレームワークへの最小侵襲的な組み込みパターンとして参考になる

## Yujiの取り組みへの示唆

監査エージェントは監査手続きの反復実行でミスパターンを蓄積しやすく、ALTK-EvolveのガイドラインライブラリをLangGraphの各ノード呼び出し前にMCP経由で注入する構成は、監査証跡→原則抽出→次回監査での活用というサイクルに直接応用できる。LangFuse等のOpenTelemetryベース観測基盤を既に使っている場合、Low-codeパスで既存LangGraphエージェントにほぼ変更なく導入できる点も実用的。また、SOPやポリシーをエンティティとして管理する設計は、内部監査のコントロールライブラリとの親和性が高く、GRPO/RLAIFによる報酬設計と組み合わせてガイドラインの品質スコアを強化学習的に更新する拡張も考えられる。

## 原文リンク

[ALTK-Evolve: AIエージェントのオンザジョブ学習システム](https://huggingface.co/blog/ibm-research/altk-evolve)
