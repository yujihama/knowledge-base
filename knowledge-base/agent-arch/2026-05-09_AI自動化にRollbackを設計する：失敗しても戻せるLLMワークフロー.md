---
title: "AI自動化にRollbackを設計する：失敗しても戻せるLLMワークフロー"
url: "https://zenn.dev/kanaria007/articles/82151af4c2641e"
date: 2026-05-09
tags: [LLMワークフロー, rollback設計, effect-bearing, idempotency, TypeScript, 自動化アーキテクチャ, 補償トランザクション, human-in-the-loop]
category: "agent-arch"
related: [4232, 3898, 1704, 1619, 4373]
memo: "[Zenn LLM] AI自動化にRollbackを設計する：失敗しても戻せるLLMワークフロー"
processed_at: "2026-05-09T09:37:46.184480"
---

## 要約

LLMや AIエージェントを本番環境に導入する際、「失敗したときに戻せるか」を設計の起点に置くべきという実践的アーキテクチャパターンを解説した記事。

中核となる概念は、外部状態変更を伴う処理（effect-bearing）を3種類に分類することだ。①reversible（ほぼ元に戻せる：GitHubラベル付与・権限付与など）、②compensatable（完全には戻せないが補償可能：Slack誤通知後の訂正投稿など）、③irreversible（戻せない・戻すべきでない：外部メール送信・法的確定・請求処理など）。

各effectには TypeScript型として `EffectRequest`（idempotency_key、reversibility必須）と `EffectRecord`（実行結果・rollback_ref・compensation_ref含む）を定義する。特筆すべきは結果を "succeeded" / "failed" / "unknown" の3値で管理する点で、外部APIのタイムアウト時に "unknown" として記録することで二重送信を防ぐ。

rollbackとcompensationの設計パターンも具体的に示される。reversibleな処理では実行前に `RollbackPlan`（rollback_type, payload, expected_current_state）を生成しておく。ステータス変更のrollbackには変更前の `from_status` が必須であり、「変更前状態の保存→effect実行→EffectRecord+rollback_ref保存」の順序が重要。compensatableでは `CompensationPlan` を用いた前方修正ワークフローとして設計し、履歴は積み上げる形で管理する。

実行制御には `AutomationPolicy` 型（auto-after-gate / human-review-required / do-not-auto-execute）を導入し、reversibilityに応じて自動実行ゲートを制御する。irreversibleには human review必須＋idempotency key必須を課す。

監査エージェント開発への示唆として、このパターンはLangGraphなどのワークフローエンジンで実装するエージェントが外部システム（ERP・ワークフローツール・通知システム）を操作する際の副作用管理に直接応用できる。audit-aiの文脈では、自動化した監査アクション（承認・却下・エスカレーション）をeffect-bearingとして分類し、RollbackPlan/CompensationPlanを必ずペアで設計することが内部統制上の要件に合致する。

## アイデア

- 外部APIタイムアウト時の結果を 'failed' ではなく 'unknown' として記録し二重送信を防ぐ3値EffectResult設計が、分散システムの実務的課題への具体的解法になっている
- rollback planをeffect実行「前」に作成し expected_current_state を持たせることで、第三者による状態変更後のrollback衝突をDEGRADE（人間レビュー戻し）として検出できる安全機構
- reversibility分類を処理名（API名）ではなく「誰に見えるか・どれくらい拡散するか・訂正しても残る影響」の組み合わせで決定するという観点が、単純なAPI分類より実務に即している

## 前提知識

- **effect-bearing処理** (TODO: 読むべき)
- **補償トランザクション** (TODO: 読むべき)
- **idempotency key** (TODO: 読むべき)
- **LLMエージェント設計** (TODO: 読むべき)
- **human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト

## 関連記事

- /deep_4232 AIエージェントを本番に入れる前に分けるべき3つの境界：support-only / review-only / effect-bearing
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_1704 機械学習ディレクターたちの現場インサイト【前編】：メディア・製薬・研究分野での実践知
- /deep_1619 敵対的データを用いた動的モデル訓練の方法（MNISTを例に）
- /deep_4373 効果的なAIエージェントの作り方 — Anthropic Barry Zhangが語る3つの原則

## 原文リンク

[AI自動化にRollbackを設計する：失敗しても戻せるLLMワークフロー](https://zenn.dev/kanaria007/articles/82151af4c2641e)
