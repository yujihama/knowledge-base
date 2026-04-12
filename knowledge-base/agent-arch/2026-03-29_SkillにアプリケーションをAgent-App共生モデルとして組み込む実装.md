---
title: "SkillにアプリケーションをAgent-App共生モデルとして組み込む実装"
url: "https://nyosegawa.com/posts/skill-with-app/"
date: 2026-03-29
tags: [Agent Skill, MCP, AG-UI, A2UI, React, SSE, Codex App Server, self-contained skill, Claude Code]
category: "agent-arch"
memo: "Skillにアプリケーションを組み込んでみる - 逆瀬川ちゃんのブログ"
processed_at: "2026-03-29T21:55:55.758577"
---

## 要約

Coding AgentのSkillにReactアプリを同梱するself-containedパッケージ構造「skill-with-app」の実装報告。アーキテクチャはCoding Agent → curl POST /api/app → API Server(SSE) → Frontend(React)という単方向フロー。各スキルはSKILL.md + apps/ + data/の3要素で構成され、Viteのimport.meta.globによる自動発見機構でホスト側コードの変更なしにスキルを追加可能。Agentはデータ取得・推論・構造化を担い、AppはUI表示・ユーザー操作を担うという責務分離が設計思想の核心。レシピ管理・経費管理・CRM等13スキルを並列生成で実験。現状の限界はJSONベース永続化の脆弱性、マルチデバイス非対応、法規制対応（電子帳簿保存法等）。セキュリティ面ではSnyk調査でClawHub上スキルの36%に問題が検出された事例も言及。MCP Apps・AG-UI・A2UIなど関連プロトコルの動向も整理されている。

## 要点

- SKILL.md + apps/ + data/のself-containedパッケージ構造により、ホスト側コード変更なしにスキル追加が可能なプラグインアーキテクチャを実現
- AgentとAppの責務を明確に分離（Agent: データ取得・推論、App: 表示・ユーザー操作）することで、人間の判断介在ポイントを設計に組み込める
- スキルマーケットのセキュリティ問題（ClawHub上の36%に脆弱性）やAAIF/MCPによる標準化動向は、エージェントシステムの本番導入時に無視できないリスク要因

## 監査エージェントへの示唆

Agent-App責務分離モデル（Agentが推論・構造化、Appが表示・承認操作を担当）は監査エージェントにそのまま応用可能で、監査調書の自動生成→人間によるレビュー・承認というワークフローの実装パターンとして参考になる。スキルのself-contained化により監査固有のワークフロー（証跡収集・仕訳確認・リスクスコアリング等）をポータブルなSkillとして配布・再利用できる。

## 原文リンク

[SkillにアプリケーションをAgent-App共生モデルとして組み込む実装](https://nyosegawa.com/posts/skill-with-app/)
