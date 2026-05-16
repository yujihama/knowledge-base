---
title: "AIエージェントを本番投入する段階的昇格設計：support-only → review-only → effect-bearing"
url: "https://zenn.dev/kanaria007/articles/1221bb968aee08"
date: 2026-05-11
tags: [rollout-stage, state-machine, effect-bearing, review-only, shadow-deployment, LangGraph, AI-governance, Proposal, Receipt, rollback]
category: "agent-arch"
related: [4751, 4232, 564, 22, 4521]
memo: "[Zenn LLM] AIエージェントを段階的に本番投入する：support-onlyからeffect-bearingへの昇格設計"
processed_at: "2026-05-11T12:12:44.250390"
---

## 要約

本記事は、LLM/AIエージェントを本番業務へ段階的に投入するための設計パターンを体系的に整理している。主軸となるのは「rollout stage」という概念で、shadow / support-only / review-only / limited-effect / full-effect / paused の6段階を定義し、各ステージで許容されるアクションと必要な設計要件を明確に分ける。

stageは単なるラベルではなく状態機械（state machine）として扱う。通常昇格は一段ずつ（shadow→support-only→review-only→limited-effect→full-effect）進め、各遷移にapproval要否を持たせる。緊急降格はapproval不要で即時実行し、事後レビューを要件とする。`shadow→full-effect`のような危険な直接昇格は`allowedTransitions`配列の検証関数で禁止する。

各ステージの具体的な設計要件は以下の通り。shadow stageではAIの出力を本番ユーザーに見せず、人間の判断と裏で比較観測するだけ。単純正解率でなく「high-risk caseでの失敗パターン」「不確実性の表明能力」を観察する。support-only stageでは要約・分類候補・返信案等を人間に表示するが外部状態は変更しない。Parse Guardを設け、入力のObservationStatusが`parsed`または`partial`のときのみ出力を許可し、partialの場合は不足情報を明示したlimited modeで表示する。review-only stageではAIがProposalオブジェクトを生成し、ReviewReceiptを伴った人間承認後にのみ実行する。Proposalのreject理由や人間による修正内容を学習データ候補として記録する。limited-effect stageでは内部ラベル付与・draft保存・ticket metadata更新等の低リスクeffectのみを自動実行し、`max_daily_executions`や`require_rollback_plan`フラグをpolicyで制御する。full-effect stageではEffect Catalog・Permission・Runtime Mode・Receipt・Rollback/Compensationの5つのgateが揃った範囲でのみeffect-bearing実行を許可する。

昇格判断の指標としてPromotion Readiness Checklistを定義し、直近Nセッションでのrollback発動率・reject率・receipt欠損率・parse failure率などの閾値を段階ごとに設定する。監査エージェント開発への示唆として、本設計はLangGraphを用いた内部統制ワークフローに直接応用可能で、各ステージをNodeとして実装しStateへのstage遷移ログを記録することで、audit trailと昇格判断の根拠を一元管理できる。

## アイデア

- rollout stageを状態機械として型定義し、allowedTransitions配列で直接昇格を静的に禁止するアプローチは、LangGraphのConditional Edgeと組み合わせて監査証跡付きのstage管理に応用できる
- ObservationStatus（parsed/partial/blocked）によるParse Guardは、LLMが「読めたつもり」で誤出力するリスクを構造的に防ぐパターンとして、RAGパイプラインの入力検証層に転用可能
- Promotion Readiness Checklistでrollback発動率・reject率などの定量指標を昇格条件として定義することで、モデル精度だけに依存しないリスクベースの段階昇格が実現できる

## 前提知識

- **state machine** (TODO: 読むべき)
- **effect-bearing action** (TODO: 読むべき)
- **idempotency** → /deep_4623 AI自動化にRollbackを設計する：失敗しても戻せるLLMワークフロー
- **rollback/compensation** (TODO: 読むべき)
- **LLM workflow orchestration** (TODO: 読むべき)

## 関連記事

- /deep_4751 LLMアプリのログをレシート化する：あとから説明できるAI処理の作り方
- /deep_4232 AIエージェントを本番に入れる前に分けるべき3つの境界：support-only / review-only / effect-bearing
- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由
- /deep_22 長期ロボット卓上ゲームにおける内部状態一貫性維持のためのシステム設計
- /deep_4521 責任あるAIから、責任を扱えるAIへ――AIエージェント時代に必要な責任経路という補助線

## 原文リンク

[AIエージェントを本番投入する段階的昇格設計：support-only → review-only → effect-bearing](https://zenn.dev/kanaria007/articles/1221bb968aee08)
