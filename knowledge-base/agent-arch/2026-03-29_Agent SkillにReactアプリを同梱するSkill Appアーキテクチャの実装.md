---
title: "Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装"
url: "https://nyosegawa.com/posts/skill-with-app/"
date: 2026-03-29
tags: [Agent Skill, Claude Agent SDK, Codex App Server, SSE, React, MCP, AG-UI, A2UI, プラグインアーキテクチャ, Vite]
category: "agent-arch"
memo: "Skillにアプリケーションを組み込んでみる - 逆瀬川ちゃんのブログ"
related: [1247, 1307, 652, 1349, 2]
processed_at: "2026-03-29T21:55:31.684965"
---

## 要約

Coding AgentをラップするGUIアプリケーション上で、Agent SkillにReactコンポーネントを同梱する「Skill App」パターンの実装報告。アーキテクチャは「Coding Agent → curl POST /api/app → API Server (SSE) → Frontend (React)」という構成で、Agentがワークフロー内でAPIを叩き、SSEでフロントエンドにビュー表示を指示する。各スキルはSKILL.md・apps/・data/のself-containedパッケージとして設計され、Viteのimport.meta.globによる自動発見でホスト側のコード変更なしにスキルを追加可能。AgentはデータのFetchと推論を担い、Appは表示と人間のインタラクション（承認/却下/編集）を担うという責務分離の哲学を採用。MCP・AG-UI・A2UIなどのUI統合プロトコルの動向も整理されており、セキュリティ課題（ToxicSkills研究では36%のスキルに問題）やAAIF標準化の動きにも言及している。

## 要点

- Agentがプラットフォームとなりアプリを呼び出す逆転の発想：SKILL.md+apps/+data/のself-containedパッケージでホスト側変更なしにスキルを追加できる
- Agent/App間の責務分離原則：データ取得・推論・スコアリングはAgent、表示・承認・編集操作はAppと明確に分離することでLLMの負荷を下げ人間のインタラクションを最適化
- スキルマーケットのセキュリティが現実的課題：ToxicSkills研究で無料スキルの36%に問題が発見されており、署名・レビュー・スキャン自動化の仕組みが必要
## 関連記事

- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_1307 Transformers.jsでMLパワードWebゲームを作る方法
- /deep_652 GradioでMCPサーバーを5行のPythonで構築する方法
- /deep_1349 ALTK-Evolve: AIエージェントのオンザジョブ学習システム
- /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 原文リンク

[Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装](https://nyosegawa.com/posts/skill-with-app/)
