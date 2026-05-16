---
title: "AI-nativeなWebアプリはrouteではなくcapabilityから設計したほうがいい"
url: "https://zenn.dev/53able/articles/5e32c6e5a4b511"
date: 2026-05-16
tags: [capability-first, AI-native, agent-harness, deterministic-runtime, Human-in-the-loop, policy, audit-log, Pi, tool-calling, WebFramework]
category: "agent-arch"
related: [1704, 1619, 4620, 4373, 877]
memo: "[Zenn LLM] AI-nativeなWebアプリは route ではなく capability から設計したほうがいい"
processed_at: "2026-05-16T09:01:47.434532"
---

## 要約

本記事は、AI agentを前提としたWebアプリケーション設計において、従来の「Route → Controller → Service → DB」という構造を廃し、「Intent → Agent Harness → Capability → Deterministic Runtime → State」という capability-first アーキテクチャを提唱する。

従来のWebアプリはHTTP endpointや画面を起点に設計されるが、LLM agentはURLではなく業務操作単位（例: invoice.searchOverdue, email.composeReminder）を必要とする。そこで capability を「入力・出力・権限・副作用・承認条件をまとめた安全な業務操作定義」として中心に置く設計を提案する。

capability の定義例として `capability("invoice.create", { input, policies: [requireRole("accounting"), requiresApprovalWhen(amount > 100000)], handler })` のような構造を示す。この定義から agent tool schema、API endpoint、admin form、audit schema、テスト fixture を派生させることができ、capability registry が single source of truth となる。

Pi（minimal terminal coding harness）の設計思想から3点を借用する：①コアを小さく保つ、②feature ではなく primitive を作る（小粒度の capability を並べる）、③PiをSDK/RPCとして埋め込む。Pi は本番 runtime ではなく planning・tool calling・session tree管理・provider abstraction を担う agent control plane として位置づける。一方、Web フレームワーク側は認可・transaction管理・副作用実行・audit/approval という deterministic runtime を担う。

設計5原則として以下を提示する：①primitive は小さくする（`manageCustomerBilling()` より `customer.find()`+`invoice.createDraft()` 等に分割）、②すべての副作用に policy を付ける（read=自動実行可、write=policy次第、money=必ずapproval、delete=reversibleまたはapproval）、③agent実行は必ず trace 可能にする（intent/plan/tool calls/inputs/outputs/approval/final resultを記録）、④Human-in-the-loopを最初から入れる（メール送信・課金・削除は必ず人間承認）、⑤UIもcapabilityから生成する。

監査エージェント開発への示唆：capability定義に policy と audit schema を組み込む構造は、内部統制の3点セット（権限・証跡・承認）をコードで表現する手法として直接応用可能。LangGraphのノード設計においても、各ノードをcapabilityとして定義し副作用種別ごとに承認フローを差し込む設計と親和性が高い。

## アイデア

- capability を single source of truth にすることで、agent tool schema・API endpoint・admin form・audit schema を同一定義から自動派生できる点は、LangGraph の tool 定義と OpenAPI スキーマを統一管理する実装パターンに直結する
- 副作用の種別（read/write/money/delete/external）ごとに policy を明示的にコードに書く設計は、内部監査における統制マトリクスをプログラマブルに表現する手法として、監査エージェントのガードレール設計に応用できる
- LLM は判断（capability 選択・実行順序計画）、コードは実行（DB更新・認可・transaction）という役割分離は、LLM-as-judge パターンと deterministic executor パターンを組み合わせた実装設計の基礎概念として整理される

## 前提知識

- **tool calling** → /deep_946 HuggingChatにコミュニティツール機能を導入：任意のSpaceをLLMツールとして利用可能に
- **ReAct agent** (TODO: 読むべき)
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **RBAC** → /deep_5264 Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS
- **audit log** (TODO: 読むべき)

## 関連記事

- /deep_1704 機械学習ディレクターたちの現場インサイト【前編】：メディア・製薬・研究分野での実践知
- /deep_1619 敵対的データを用いた動的モデル訓練の方法（MNISTを例に）
- /deep_4620 厳密性が要求される業務プロセスへのAIエージェント応用設計：ポリシー制約評価・専門家判断・中期記憶・段階的自律化によるアーキテクチャ
- /deep_4373 効果的なAIエージェントの作り方 — Anthropic Barry Zhangが語る3つの原則
- /deep_877 ベイズ最適化による効率的・原理的な科学的発見：チュートリアル

## 原文リンク

[AI-nativeなWebアプリはrouteではなくcapabilityから設計したほうがいい](https://zenn.dev/53able/articles/5e32c6e5a4b511)
