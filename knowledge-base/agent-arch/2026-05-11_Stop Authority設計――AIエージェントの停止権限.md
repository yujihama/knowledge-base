---
title: "Stop Authority設計――AIエージェントの停止権限"
url: "https://zenn.dev/dantarg/articles/stop-authority-design"
date: 2026-05-11
tags: [Stop Authority, AIガバナンス, 責任経路工学, Emergency Stop, Human-in-the-loop, EU AI Act, NIST AI RMF, LangGraph, guardrails, audit-trail]
category: "agent-arch"
related: [4625, 4033, 4521, 4750, 3899]
memo: "[Zenn LLM] Stop Authority設計――AIエージェントの停止権限"
processed_at: "2026-05-11T12:42:40.886363"
---

## 要約

AIエージェントがツール呼び出し・ファイル更新・外部API連携など実際の業務行為を実行するようになると、「止める設計」が不可欠になる。本稿はその設計概念として「Stop Authority（停止権限）」を提唱する。Stop Authorityは単なる停止ボタンではなく、①誰が止めるか（権限の定義）、②どの条件で止めるか（停止条件の事前定義）、③止めた後に責任をどこへ戻すか（Repair Ownerとの接続）の三要素を含む設計である。

核心的な論点は「実行権限と停止権限の分離」である。実行したい主体が自分の実行を止める判断を持つと、納期・依頼・承認済みという圧力により停止が遅れる。そのため、Execution Authority・Approval Authority・Stop Authority・Repair Authorityを独立した役割として設計する。

停止条件は承認者未定義・影響範囲未評価・不可逆操作・外部送信・個人情報処理・Evidence Logが残せないケースなど16項目を例示する。エラー発生時だけでなく「エラーは出ていないが責任経路が未定義」な状況も停止対象とする点が重要。

停止レベルはLevel 1（Pause：確認のための一時停止）からLevel 5（Emergency Stop：即時停止・隔離）まで5段階に分け、行為クラス（Observe-Only / Suggest-Only / Approval-Required / Reversible External Action / Irreversible Action / Emergency Stop）と対応させる。

Emergency Stopはツール呼び出し停止・外部送信停止・セッション隔離・権限縮退・Safe-Only Modeへの移行など具体的な動作を事前設計する。またStop-and-Await Modeでは、AIは完全沈黙ではなく「何が未確定か・どの選択肢があるか」の提示は継続しつつ実行は禁止する。

Stop Logには「いつ/何を/誰が/どの条件で/AIか人間か自動か/停止できなかった理由/どこへ戻したか/誰が再開判断したか」を記録し、Evidence Logと接続することで事後の責任経路再構成を可能にする。

組織設計面では「止めると責められる」文化が停止権限を形骸化させるとして、停止行為を正当な行為として明示・不利益扱いの禁止・誤停止を改善材料として扱うことを求める。EU AI Act Article 14やNIST AI RMFの人間監督要件を、エージェント運用の実装粒度へ落とし込む設計として位置づけている。監査エージェント開発においては、停止条件の事前定義・Stop Logの設計・Repair Ownerの指定がガバナンス要件と直結する。

## アイデア

- 実行権限と停止権限を組織的に分離するという発想は、財務統制における職務分掌（Segregation of Duties）をAIエージェント設計に適用したものとして捉えられ、内部統制フレームワークとの親和性が高い
- Stop-and-Await Modeの概念——AIが実行を止めながら「未確定事項の説明・選択肢提示」は継続する——は、LangGraphのHuman-in-the-loopにinterrupt条件を責任経路として意味付けする実装指針になり得る
- 停止条件を「エラー発生時」だけでなく「Evidence Logが残せない」「Human Return Pointがない」といった責任経路の欠落として定義する視点は、技術的なguardrailsと監査可能性要件を統合する設計原則として応用できる

## 前提知識

- **LangGraph Human-in-the-loop** (TODO: 読むべき)
- **guardrails / tripwire** (TODO: 読むべき)
- **EU AI Act Article 14** (TODO: 読むべき)
- **NIST AI RMF** → /deep_4033 責任固定から責任経路設計へ――AIガバナンスに必要な「固定後」の設計
- **ReAct Agent** (TODO: 読むべき)

## 関連記事

- /deep_4625 Evidence Log設計――責任経路を後から再構成するための監査ログ
- /deep_4033 責任固定から責任経路設計へ――AIガバナンスに必要な「固定後」の設計
- /deep_4521 責任あるAIから、責任を扱えるAIへ――AIエージェント時代に必要な責任経路という補助線
- /deep_4750 なぜ「責任経路工学」だったのか：証拠連鎖を超えたAI責任設計の補助線
- /deep_3899 ISO/IEC 42001時代の責任経路工学――AIマネジメントシステムを実装粒度へ落とす

## 原文リンク

[Stop Authority設計――AIエージェントの停止権限](https://zenn.dev/dantarg/articles/stop-authority-design)
