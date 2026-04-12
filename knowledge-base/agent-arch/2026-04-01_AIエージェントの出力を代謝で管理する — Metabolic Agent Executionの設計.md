---
title: "AIエージェントの出力を代謝で管理する — Metabolic Agent Executionの設計"
url: "https://zenn.dev/zima11/articles/6622f0a55896e0"
date: 2026-04-01
tags: [Metabolic-Agent-Execution, Validator-Ladder, LLM-output-validation, asyncio, repair-loop, post-hoc-validation, parallel-execution, rollback]
category: "agent-arch"
memo: "[Zenn LLM] AIエージェントの出力を代謝で管理する — Metabolic Agent Executionの設計"
processed_at: "2026-04-01T21:09:31.667019"
---

## 要約

Metabolic Agent Executionは、生物の代謝（変換・検証・修復・排出）をモデルにしたAIエージェント実行パターン。broadcast-os（AI自律放送局OS）に実装されており、中核となるのはrun_metabolic_parallel（Metabolic Execution Kernel）。

実行単位はChunkと呼ばれ、AGENT_RUN（複数エージェント並列実行）、PRIMARY_RUN、REVIEW_PASS、BUILD_STEP、INVESTIGATION、PRODUCTIONの6種類に分類される。ChunkタイプによってLLMタスク間の依存関係と並列実行可否が決まる。

Chunk出力の品質保証はValidator Ladderという4段階構造で行われる。L1は出力の存在確認（空でないか）、L2は最低品質チェック（文字数・繰り返し・エラー混入）、L3はbriefとの整合性確認、L4は複数エージェント出力間の差別化・多様性比較（post-hoc）。L1失敗は即ハードフェイル、L2以降は深刻度によりhard failureとwarningに分類される。

検証失敗時はrepair_chunkが作動し、失敗タイプ（repetitive_output、output_too_short、error_in_outputなど）に応じた具体的ヒントを元プロンプトに付加して再実行する。修復不能な場合はrollback_chunkで当該実行を無効化する。

Kernelは3フェーズで動作する。Phase 1でasyncio.gatherによる全エージェント並列実行、Phase 2でpost-hoc検証と必要に応じた修復、Phase 3で全件揃った後のcomparative merit比較。既存のparallel_compareの並列実行特性を維持しつつ、バリデーション層を上から被せる設計により、既存テスト769件を維持しつつ783件（+14）に拡張できた。

Phase A完了時点でExecutionStateMemoryが各Chunkの実行状態・修復回数・失敗履歴を保持し、グラフ経由で下流に伝播される。Phase Bではknotカタログ（過去実行パターンの知識ベース）とexecution profile（タスク種別ごとの実行設定）を組み合わせたルーティングを実装予定。現状の課題はL4のcomparative merit基準の曖昧さで、knot catalogによる強化を計画している。

## アイデア

- 失敗を単純なリトライではなく「失敗タイプ別ヒント付きプロンプト修正」として扱うrepairループにより、文脈を持った再実行が実現できる点
- 並列実行レイテンシ特性を維持しながらpost-hocでvalidation層を追加する設計により、既存コードを破壊せずに品質保証を組み込める点
- L1（機械的存在確認）からL4（意味的・比較的品質評価）への段階的ラダー構造により、検証コストと精度のトレードオフを制御できる点
## 関連記事

- /deep_1241 Clade v1.4.0 — Gitワークツリーを使った並列マルチエージェント開発

## 原文リンク

[AIエージェントの出力を代謝で管理する — Metabolic Agent Executionの設計](https://zenn.dev/zima11/articles/6622f0a55896e0)
