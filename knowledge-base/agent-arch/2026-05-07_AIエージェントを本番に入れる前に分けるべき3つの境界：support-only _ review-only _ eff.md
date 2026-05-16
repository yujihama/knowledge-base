---
title: "AIエージェントを本番に入れる前に分けるべき3つの境界：support-only / review-only / effect-bearing"
url: "https://zenn.dev/kanaria007/articles/78d706292d0968"
date: 2026-05-07
tags: [AIエージェント, effect-bearing, review-only, support-only, 境界設計, 監査可能性, TypeScript, 冪等性, ワークフロー設計, 本番運用]
category: "agent-arch"
related: [3898, 4033, 2203, 78, 3095]
memo: "[Zenn LLM] AIエージェントを本番に入れる前に分けるべき3つの境界"
processed_at: "2026-05-07T21:43:15.433375"
---

## 要約

LLMや AIエージェントを業務システムに組み込む際、精度だけでなく「AIの出力がどの効果境界に接続されているか」を明示的に設計することが安全な本番運用の核心だという実務的知見をまとめた記事。

提案する3つの境界は以下の通り。

**support-only**：外部状態を変更しない。要約・分類・返信案の生成など、あくまで「判断の材料」を提供する段階。失敗しても人間が確認して止められるため被害が小さい。TypeScriptでは `{ boundary: "support-only", summary: string, suggestions: string[], confidence: "low"|"medium"|"high" }` のような型で表現し、この出力をそのまま外部effectに接続しないことが原則。

**review-only**：AIが提案を作るが実行には人間の承認が必要。重要なのは「UIの雰囲気ではなくシステム上の必須条件」として人間レビューを強制すること。`ReviewRecord` 型（review_id, request_id, reviewer_id, reviewer_role, decision, reviewed_at）をrequest_idと紐づけて管理し、別の提案へのレビュー記録の流用を防ぐ。`if (aiResponse.looksGood) { sendEmail(...) }` のような実装は「レビューしている風」であって実質AI送信であり危険と指摘。

**effect-bearing**：実際に外部状態を変更する。DB更新・メール送信・権限付与・請求処理など。この境界に入る処理は通常の関数呼び出しではなく「監査可能な実行要求」として扱い、誰が承認したか・何を変更するか・どの証拠に基づくか・変更前状態・rollback可否を必ず記録する `EffectRecord` を残す。`idempotency_key` も必須。

境界の強制はコードで行う。`canExecute()` 関数でeffect-bearing実行時に `evidence_refs`・`review_id`・対応する承認済み `ReviewRecord`・`required_reviewer_role` の合致・`idempotency_key` の存在をすべて検証し、条件を満たさない場合は実行不可とする。

最もよくある事故パターンは、support-onlyだった機能が段階的な効率化の中でいつの間にかeffect-bearingになり、設計が追いつかないケース。「一定条件なら自動返信」にした時点でeffect-bearingだが、support-only前提で作ったプロンプト・ログ・UI・権限・テストはeffect-bearingの責任に耐えられない。

reversibilityも3分類（reversible: ラベル変更等、compensatable: 誤通知後の訂正通知、irreversible: 外部メール送信・法的確定処理）し、effect recordに持たせることで障害対応を構造化する。

監査エージェント開発への示唆：内部監査領域でAIが生成した発見事項・勧告・是正指示は典型的なreview-onlyであり、承認なしに経営層への報告や是正アクション実行に直結させるのはeffect-bearingへの設計変更を伴う。LangGraph等で実装する際はnodeレベルでboundary typeをスキーマに組み込み、effect-bearingなnodeへの入力にはReviewRecord検証を必須化すべき。

## アイデア

- 境界をドキュメントではなくTypeScriptの型システムとruntime checkで強制するアプローチ：`canExecute()`関数がevidence_refs・review_id・idempotency_keyを全て検証し、条件未充足なら実行不可にする設計は、LangGraphのconditional edgeと組み合わせてagentのgate層として実装できる
- ReviewRecordをrequest_idと必ず紐づける設計：「誰かが何かを承認した」だけでは足りず、どのrequestへの承認かまで紐づけることで承認記録の流用を防ぐ点は、監査エージェントにおける証拠の追跡可能性（traceability）設計に直結する
- reversibility（reversible / compensatable / irreversible）をeffect typeの属性として型に持たせる発想：障害対応・rollback設計を実行時スキーマに組み込むことで、補償トランザクション（saga pattern）の実装基盤にもなる

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **TypeScript型システム** (TODO: 読むべき)
- **冪等性キー** (TODO: 読むべき)
- **補償トランザクション** (TODO: 読むべき)
- **ワークフロー設計** (TODO: 読むべき)

## 関連記事

- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_4033 責任固定から責任経路設計へ――AIガバナンスに必要な「固定後」の設計
- /deep_2203 自律型AIエージェントが生む新たな攻撃面：認証情報漏えいとプロンプトインジェクションのリスク
- /deep_78 広告の届け先はAIになる — B2A (Business to Agent) Platform という未来
- /deep_3095 伏線エンジンの設計 — 計画的伏線とAI自動生成を両立させる

## 原文リンク

[AIエージェントを本番に入れる前に分けるべき3つの境界：support-only / review-only / effect-bearing](https://zenn.dev/kanaria007/articles/78d706292d0968)
