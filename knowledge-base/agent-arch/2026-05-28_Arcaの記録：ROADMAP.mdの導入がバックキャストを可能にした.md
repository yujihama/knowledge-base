---
title: "Arcaの記録：ROADMAP.mdの導入がバックキャストを可能にした"
url: "https://zenn.dev/sisiodos/articles/5bb97e95ace33b"
date: 2026-05-28
tags: [ROADMAP.md, backcast, future-state reasoning, exploratory planning, workflow, Arca, agent autonomy, GOAL.md, visible cognition, task decomposition]
category: "agent-arch"
related: [2538, 6555, 1742, 6554]
memo: "[Zenn LLM] Arcaの記録: ROADMAP が backcast を可能にした"
processed_at: "2026-05-28T09:07:26.614386"
---

## 要約

本記事は、AIエージェントシステム「Arca」の開発記録であり、2026年4月19日にGOAL.mdとROADMAP.mdをリポジトリに配置したことで、エージェントの振る舞いが「ワークフロー実行」から「目的推論・探索的計画」へと質的に変化した経緯を記述している。

初期のArcaはrole separation・review loop・handoff・PR-based operationといった明示的なワークフローで構成されていた。しかしtaskとworkflowだけでは、エージェントが局所的な作業に閉じやすく、プロジェクト全体の方向性を即座に把握できないという問題があった。そこでまずGOAL.mdを導入し、「現在どこへ向かっているのか」をキャッシュ状態として明示した。これはgit logやissueから復元可能な情報だが、毎回履歴を辿る非効率を避け、人間とエージェント双方が即座に方向性を共有できる仕組みとして機能した。

しかしGOAL.mdには副作用があった。エージェントがGOALに強く引っ張られるあまり、短期的な収束（local optimization）が発生し、視野が近い未来に閉じる傾向が生じた。これを解決するためROADMAP.mdを追加した。ROADMAP.mdの役割は2つで、①やや投機的な将来方向の記述、②future stateから現在地点を逆算するstage backcastの実施である。

ROADMAP導入後、エージェントへの指示スタイルが変化した。従来はCodex CLIによるtask decompositionが中心だったが、ROADMAPを読み込んだエージェントが自律的に次のstageや必要な作業を推測するようになり、細かなtask分割の頻度が著しく低下した。エージェントはroadmapと現在地点を照合しながら、どのmaturity boundaryにいるかを解釈して行動するようになった。

この実験時点ではexploratory graphもplanning graphも存在せず、リポジトリに2つのmarkdownファイルを置いただけである。にもかかわらず、エージェントの探索性質は大きく変わり、「なぜその方向へ向かったか」「なぜ別案を捨てたか」といったreasoningがtask stateの外側に存在することが明確になった。この経験がtaskとexplorationを分離するという設計思想へと繋がり、後のexploratory graph・visible cognitionの方向性の起点となった。監査エージェント開発においても、GOAL/ROADMAPのような「現在地とゴールの二層構造」をコンテキストとして持たせることで、エージェントの自律的な計画立案能力を向上させられる可能性がある。

## アイデア

- GOAL.mdによるlocal optimizationの副作用：エージェントに単一の目標を持たせると近視眼的収束が起きるため、より遠い未来を記述するROADMAP層を追加することで視野を拡張できるという二層目標構造の発見
- future stateからの逆算（backcast）によるtask decompositionの自動化：ROADMAPを読ませるだけでエージェントが自律的にstageと必要作業を推測し、人間によるtask分割の頻度を大幅に削減できた
- workflowはexecutionを扱えてもexplorationを扱うには窮屈という観察：「なぜその判断をしたか」というreasoningはtask stateに収まらず、taskとexplorationを分離する設計の必要性を示唆している

## 前提知識

- **AIエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **Workflow Harness** (TODO: 読むべき)
- **Backcast** (TODO: 読むべき)
- **Task Decomposition** (TODO: 読むべき)
- **LLM Context Management** (TODO: 読むべき)

## 関連記事

- /deep_2538 【Claude Code】Workflowを自分で作ってみた！CC Workflow Studioがあるけどね
- /deep_6555 MCPとSkillsに続く第3の革命：Claude Code WorkflowがultraworkでAgentをコードに焼き付ける
- /deep_1742 Clade v1.13.0 — 「自動化」を疑って、シンプルに直す
- /deep_6554 Arcaの観察：役割分離がエージェントの振る舞いを変え始めた

## 原文リンク

[Arcaの記録：ROADMAP.mdの導入がバックキャストを可能にした](https://zenn.dev/sisiodos/articles/5bb97e95ace33b)
