---
title: "AIワークフローのテストケースを作る：golden case / regression / incident replay"
url: "https://zenn.dev/kanaria007/articles/e20e1b92ee5258"
date: 2026-05-11
tags: [golden case, regression test, incident replay, Parse Guard, Effect Catalog Gate, Effect Permission Gate, AI workflow testing, LLM testing, receipt, boundary]
category: "agent-arch"
related: [4333, 4751]
memo: "[Zenn LLM] AIワークフローのテストケースを作る：golden case / regression / incident replay"
processed_at: "2026-05-11T09:40:46.947926"
---

## 要約

LLMや AIエージェントを本番環境に導入する際のテスト設計について、golden case・regression test・incident replayという3つのパターンを中心に解説した記事。

最大のポイントは「生成文の完全一致テストをしない」こと。自然言語の出力は同一入力でも表現が変わるため壊れやすく、本番で重要なのはAIの出力がどのboundaryを通り、どのgateで止まり、どのreceiptを残し、どのeffectを起こすかという構造的な判定である。

ワークフローのテスト対象は Input → Parse Guard → Effect Intent Classification → Effect Catalog Gate → Effect Permission Gate → Runtime Mode Gate → Receipt/Effect Record という一連の流れ全体。

golden caseでは、入力に対して「parse_guardのdecision（allow/limit/block）」「許可されるboundary（support-only/review-only/effect-bearing）」「effect_bearing_allowedの真偽」「gate_verdict（ACCEPT/DEGRADE/REJECT）」「receipts_required」などを構造化された期待値として固定する。自然文の細かい言い回しは対象外。

fixturesには外部依存を固定するためのretrieved_docs・state_snapshot・actor_permissions・catalog_version・policy_version・prompt_template_version・model_profileなどを含め、テストの再現性を担保する。

expectedの由来は4種類に分類される：①design expected（仕様・policyから人間が書く、safety contractに向く）、②captured expected（過去の正常runを固定、regressionに向く）、③differential expected（新旧実装の差分比較、migrationに向く）、④incident expected（事故再発防止条件として記述、incident replayに向く）。effect-bearingに関わるgolden caseは人間が明示的にexpectedを書くべきで、実装から自動生成するとbugまで固定するリスクがある。

regression testでは「captured expected」として過去の正常runのgate verdict・permission decision・effect実行有無・receiptsをスナップショット化し、実装変更後の差分検出に使う。incident replayでは実際の障害ケースを再現可能な形でテストに変換し「この入力ではDEGRADEすること」「この条件では実行しないこと」を永続的に確認できる形にする。

監査エージェント開発への示唆として、本記事のアーキテクチャ（Parse Guard → Effect Permission Gate → receipt必須化）は内部統制のアクセス制御・承認フロー・監査ログ設計と直接対応する。「irreversibleなeffectは自動実行しない」「required receiptが欠けたらDEGRADE」という設計原則は監査AIにおけるヒューマン・イン・ザ・ループの実装パターンとして活用できる。

## アイデア

- テスト対象を「生成文」ではなく「gate verdict・permission decision・effect実行有無」という構造的判定に限定することで、自然言語の揺らぎに依存しない壊れにくいテストが実現できる
- expectedの由来をdesign/captured/differential/incidentの4種に分類し、safety contractはhuman-writtenで固定するという設計により、実装バグのexpected混入を防ぐ
- incident replayパターンにより、過去の本番障害をテストケースとして永続化し回帰防止できる点は、監査AIのリスク管理フレームワークと親和性が高い

## 前提知識

- **ReAct agent** (TODO: 読むべき)
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **Parse Guard** → /deep_4333 Parse Guard：LLMアプリに「読んだつもり」をさせない入力検証パターン
- **Effect Permission** (TODO: 読むべき)
- **idempotency key** (TODO: 読むべき)

## 関連記事

- /deep_4333 Parse Guard：LLMアプリに「読んだつもり」をさせない入力検証パターン
- /deep_4751 LLMアプリのログをレシート化する：あとから説明できるAI処理の作り方

## 原文リンク

[AIワークフローのテストケースを作る：golden case / regression / incident replay](https://zenn.dev/kanaria007/articles/e20e1b92ee5258)
