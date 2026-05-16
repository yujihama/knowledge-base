---
title: "Responsibility Pathway Layer――AIエージェントに責任経路を実装する最小構成"
url: "https://zenn.dev/dantarg/articles/33825ca3f8c0e6"
date: 2026-05-01
tags: [Responsibility Pathway Layer, AIガバナンス, Human-in-the-loop, Guardrails, Fail-Closed, RACI, エージェントアーキテクチャ, 監査ログ, Action Class Matrix, 責任設計]
category: "agent-arch"
related: [1426, 1516, 2103, 847, 1704]
memo: "[Zenn LLM] Responsibility Pathway Layer――AIエージェントに責任経路を実装する最小構成"
processed_at: "2026-05-01T12:22:39.176793"
---

## 要約

AIエージェントが業務システムへの書き込み・メール送信・外部API呼び出しなど不可逆な実行を伴う時代において、モデル性能・ガードレール・HITL・Fail-Closedだけでは「責任の空白」が生じる。本記事はその空白を埋めるOS Layerとして「Responsibility Pathway Layer（RPL）」を定義する。

RPLは「AIに責任を持たせる」仕組みではなく、AIを経由した判断を人間・組織の責任構造へ再接続するための流路設計である。既存概念（RACI・HITL・Guardrails・Fail-Closed）はいずれも責任の一側面しか扱えず、止まった後に誰が拾うか・どこへ責任が戻るかを設計しない点が限界とされる。

最小構成（Minimum Set）として7要素が定義される。①Decision Owner：判断を採用する責任主体、②Approval Gate：行為ごとの承認設計（承認者が何を理解し何の責任を引き受けるかまで含む）、③Execution Actor：AI・ツール・API・人間のどれが実行したかの区別、④Stop Authority：実行権とは独立した停止権の定義、⑤Evidence Log：判断・承認・実行・停止・修復の証跡、⑥Repair Owner：失敗後の修復責任者（最も抜けやすい）、⑦Human Return Point：責任が人間へ戻れる経路の明示（形式的なHITLではなく「Human-returnable」設計）。

周辺レイヤとして、行為をObserve-Only/Suggest-Only/Approval-Required/Reversible/Irreversible/Emergency Stopに分類するAction Class Matrix、環境信頼度（Trusted Internal〜Adversarial）に応じたEnvironment Trust Levels、責任経路が不安定な際の安全縮退ポリシー（Full Mode〜Stop-and-Await Mode）、外部入力を「見たこと」と「従ってよいこと」を分離するInput Contamination Handling Protocolが挙げられる。

実装例として、ファイル更新（可逆・中程度の外部影響）、メール送信（不可逆・外部影響大）、DB更新・外部API実行（最強度の責任経路が必要）の3パターンで各7要素のマッピングを示す。

監査エージェント開発への示唆：内部監査領域では証跡の完全性と承認の実質性が特に重要であり、LangGraphで実装するReActエージェントにRPLを適用する場合、各ノード遷移をEvidence Logへ記録し、外部システム書き込みノード手前にApproval GateとStop Authorityを明示的に置く設計が直結する。特にRepair Ownerの定義は、監査報告書の訂正・再発防止策の責任帰属と対応する。

## アイデア

- 「Human-in-the-loop」ではなく「Human-returnable」という概念の分離：人間が形式的に存在するだけでなく、責任が戻れる経路として設計されているかを問う点は、承認の形骸化問題（『ヨシ！スタンプ』化）への具体的な処方箋になっている
- Repair Ownerを独立した設計要素として定義している点：既存のIncident Responseでも見落とされがちな「止まった後に誰が拾うか」を7要素の一つとして明示することで、AI事故後の責任の空白を構造的に防ぐ
- OS Layerとしての位置付け：Model/Tools→Harness→Responsibility Pathway Layer→Human/Organizationという積層モデルにより、RPLをモデルやランタイムの実装ではなく上位の設計責務として分離する思考枠組みは、既存エージェントフレームワーク（LangGraph、OpenAI Agents SDK等）への後付け適用を容易にする

## 前提知識

- **AIエージェント / Agent Runtime** (TODO: 読むべき)
- **HITL（Human-in-the-loop）** (TODO: 読むべき)
- **Guardrails / Fail-Closed** (TODO: 読むべき)
- **RACI** → /deep_1426 RACI / HITL / Guardrails / 責任経路設計の違い
- **OpenAI Agents SDK / Tripwire** (TODO: 読むべき)

## 関連記事

- /deep_1426 RACI / HITL / Guardrails / 責任経路設計の違い
- /deep_1516 責任経路設計はMeaningful Human Controlと何が違うのか―軍事AIのaccountability議論との接点とは
- /deep_2103 製造業RAG運用編：監査ログ + イベント駆動再インデックスを実装する
- /deep_847 直交性を超えて：徳倫理的エージェンシーとAIアライメント
- /deep_1704 機械学習ディレクターたちの現場インサイト【前編】：メディア・製薬・研究分野での実践知

## 原文リンク

[Responsibility Pathway Layer――AIエージェントに責任経路を実装する最小構成](https://zenn.dev/dantarg/articles/33825ca3f8c0e6)
