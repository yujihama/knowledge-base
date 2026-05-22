---
title: "Claude Code・Codex時代に重要になる「ハーネス」という考え方"
url: "https://zenn.dev/taka000/articles/ffe2f97499a151"
date: 2026-05-22
tags: [ハーネス, Claude Code, Codex, Harness Engineering, Tool Use, MCP, エージェントアーキテクチャ, サブエージェント, 権限制御, Verification Loop]
category: "agent-arch"
related: [2538, 2963, 2356, 3001, 3002]
memo: "[Zenn LLM] Claude Code・Codex時代に重要になる「ハーネス」という考え方"
processed_at: "2026-05-22T09:08:36.077594"
---

## 要約

AIエージェント（Claude Code、Codex、Cursor等）の本質的な構造を「LLM」と「ハーネス（Harness）」の2層に分けて解説する記事。LLM（Claude Opus/Sonnet、GPTシリーズ）は推論を担当する「脳」に過ぎず、それ単体ではリポジトリの読み取り・ファイル編集・テスト実行・git操作・コマンド実行といった実務作業が一切できない。これを補う実行基盤がハーネスであり、Claude CodeやCodexはその具体的な実装例である。ハーネスの機能は多岐にわたり、コンテキスト取得（ファイル・Issue・PR読み込み）、ツール実行（grep/lint/test/build）、状態管理（作業履歴・差分・途中状態）、検証（テスト・型チェック）、権限制御（allow/deny list・human approval・sandbox）、ワークフロー（タスク分解・順序制御）、サブエージェント管理（並列作業）、UI/CLIの8カテゴリに整理される。Harness Engineeringとして今後重要になる設計ポイントは4つ：①何をLLMに見せるか（CLAUDE.md・AGENTS.md等のコンテキスト設計）、②どこまで権限を与えるか（危険コマンド制御）、③どう検証するか（CI/CD統合）、④長時間タスク管理（checkpoint・retry・resume・memory・state）。特に④は「チャットボット」の延長ではなく分散システム設計の領域に踏み込む。AI進化の本質として、モデル性能の向上よりもハーネス側の進化（Tool Use、MCP、Self-healing、Verification Loop等）が実用上の差別化要因になりつつある点を指摘。今後の競争軸はLLM競争→Agent競争→Harness競争へ移行するという見立てを示す。監査エージェント開発への示唆として、LangGraphで構築するReActエージェントは「ハーネス」そのものであり、Pydanticによる型チェックや検証ループはHarness Engineeringの「検証」フェーズに直接対応する。エージェントの信頼性・安全性を高めるには、モデル選択よりも実行環境（権限制御・human approval・Verification Loop）の設計が本質的に重要であることが再確認できる。

## アイデア

- AIエージェントの進化の大部分はモデル改善ではなくハーネス側（Tool Use・MCP・状態管理・Self-healing）の改善であるという視点は、LLM-as-judgeやRAGの設計を「ハーネス工学」として体系化できることを示唆する
- 長時間エージェントタスクに必要なcheckpoint・retry・resumeの設計は分散システム設計と同義であり、LangGraphのState管理やPersistenceレイヤーがこれに直接対応するアーキテクチャ選択である
- CLAUDE.md・AGENTS.mdのようなコンテキスト設計ファイルがLLMの性能を左右するという指摘は、プロンプトエンジニアリングをファイルシステムレベルで構造化する「コンテキスト設計」という新たな実践領域の存在を示す

## 前提知識

- **LLM推論** → /deep_1173 エッジにおける分散生成AI推論のためのトラスト対応ルーティング（G-TRAC）
- **Tool Use** → /deep_3094 LLMに図面情報を全部見せる設計をやめた話
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装

## 関連記事

- /deep_2538 【Claude Code】Workflowを自分で作ってみた！CC Workflow Studioがあるけどね
- /deep_2963 SOWでシンプルにClaude Codeを活用する
- /deep_2356 Claude CodeからCodexを呼び出す3つの方法を整理した
- /deep_3001 AIコーディングツールを乗り換えまくっていたら、エージェント経済の入口にいた
- /deep_3002 AIは役割だけでどこまで本気の議論ができるのか：マルチAIファシリテーター会議ツールの開発記録

## 原文リンク

[Claude Code・Codex時代に重要になる「ハーネス」という考え方](https://zenn.dev/taka000/articles/ffe2f97499a151)
