---
title: "Evidence Log設計――責任経路を後から再構成するための監査ログ"
url: "https://zenn.dev/dantarg/articles/evidence-log-design"
date: 2026-05-09
tags: [Evidence Log, 責任経路工学, 監査ログ設計, AIガバナンス, LangGraph, Human-in-the-loop, EU AI Act, NIST AI RMF, Stop Authority, トレーサビリティ]
category: "audit-ai"
related: [4033, 3899, 4521, 3764, 3685]
memo: "[Zenn LLM] Evidence Log設計――責任経路を後から再構成するための監査ログ"
processed_at: "2026-05-09T09:38:40.046711"
---

## 要約

AIエージェント運用において「ログはある」のに「責任経路が再構成できない」という失敗を防ぐための設計論。著者は「責任経路工学」シリーズの第5回として、Evidence Logを「判断・承認・実行・停止・修復を後から再構成するための証跡」と定義する。

通常のイベントログ（APIが呼ばれた、メールが送信された等）は「出来事の羅列」に過ぎず、「誰が承認したか」「承認者が何を見ていたか」「なぜ止まらなかったか」という責任経路上の問いに答えられない。Evidence Logはこの問いに答えるための設計である。

残すべきログは7種類に分類される。①Request Log（誰が何を依頼したか）、②Context Log（AIに渡された文脈：参照文書・検索結果・システム指示等）、③Proposal Log（AIの提案・根拠・代替案・リスク表示）、④Approval Log（承認者が何を見て承認したか、差分・影響範囲・リスクの表示有無）、⑤Execution Log（AIか人間かツールか外部APIか、実行主体の識別と戻し方）、⑥Stop Log（停止条件・Stop Authorityの所在・なぜ継続されたか）、⑦Repair Log（修復者・修復内容・再発防止・組織報告）。

7種のログをつなぐID設計も重要で、case_id・request_id・proposal_id・approval_id・execution_id・external_trace_id・stop_id・repair_idを連鎖させることで、一つの案件の責任経路を端から端まで追跡可能にする。

LangGraph（persistence・Human-in-the-loop）やModel Context Protocolとの類似点も指摘されるが、目的が異なる。MCP等は「エージェントを動かし続けるための基盤」であり、Evidence Logは「動いた後に責任経路を失わないための基盤」である。

最小スキーマとしてEvidenceLogEntryに17フィールド（event_id, timestamp, action_class, request_owner, decision_owner, approval_gate, execution_actor, stop_authority, human_return_point等）を提案。保存範囲の最小化（個人情報マスキング・参照IDのみ保持・削除要求への対応）も設計対象として明示。

参照規格としてEU AI Act Article 12（記録保持）・Article 14（人間監督）、NIST AI RMF 1.0、ISO/IEC 42001:2023を挙げており、規制対応の文脈でも実用性が高い。監査エージェント設計においては、LangGraphのcheckpoint機構にEvidence Logのスキーマを重ね、承認ゲートごとにApproval LogとStop Logを自動生成する構成が直接応用できる。

## アイデア

- 7種のログ（Request/Context/Proposal/Approval/Execution/Stop/Repair）をcase_idで連鎖させることで、AIエージェントの判断から修復まで一本の責任経路として再構成できる設計は、LangGraphのgraphステートとcheckpoint機構に直接マッピング可能
- Approval Logに「承認者が何を見たか（差分表示・影響範囲・リスク表示の有無）」を記録するという発想は、承認ボタンのクリック記録だけでは実質的な承認の検証にならないという内部統制上の本質的問題を突いている
- Stop Log に『なぜ止まらなかったか』を記録対象とする設計は、停止権限（Stop Authority）の不行使を可視化するもので、AIエージェントの暴走事故後の原因分析において決定的な差を生む

## 前提知識

- **LangGraph persistence** (TODO: 読むべき)
- **Human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **EU AI Act Article 12/14** (TODO: 読むべき)
- **NIST AI RMF** → /deep_4033 責任固定から責任経路設計へ――AIガバナンスに必要な「固定後」の設計

## 関連記事

- /deep_4033 責任固定から責任経路設計へ――AIガバナンスに必要な「固定後」の設計
- /deep_3899 ISO/IEC 42001時代の責任経路工学――AIマネジメントシステムを実装粒度へ落とす
- /deep_4521 責任あるAIから、責任を扱えるAIへ――AIエージェント時代に必要な責任経路という補助線
- /deep_3764 責任を固定するだけでは足りない――責任経路工学という設計対象
- /deep_3685 エンゲージド AI ガバナンス：内部専門家協働による「ラストマイル課題」への対応

## 原文リンク

[Evidence Log設計――責任経路を後から再構成するための監査ログ](https://zenn.dev/dantarg/articles/evidence-log-design)
