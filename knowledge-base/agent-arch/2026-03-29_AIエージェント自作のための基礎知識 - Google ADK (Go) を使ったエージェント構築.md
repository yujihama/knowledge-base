---
title: "AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築"
url: "https://ymmt.hatenablog.com/entry/2026/03/24/221754"
date: 2026-03-29
tags: [Google ADK, Gemini, Go, SSE, マルチエージェント, ツール呼び出し, セッション管理, Vertex AI, サブエージェント, AG-UI]
category: "agent-arch"
memo: "AIエージェント自作のための基礎知識 - 誰かの役に立てばいいブログ"
processed_at: "2026-03-29T21:55:10.511468"
---

## 要約

Google Agent Development Kit (ADK) を使ったAIエージェント開発の基礎を解説した技術記事。エージェントの構成要素（LLM・ツール・セッション状態・オーケストレーションループ）、フロントエンドとのSSEベースのイベントストリーミング通信、スレッド/ブランチ/セッション/インボケーションの概念整理、ADKとgenai SDKのレイヤー構造（genaiが低レベルHTTPクライアント、ADKがエージェントフレームワーク）、Google AI Studio vs Vertex AIの使い分け、インストラクション設計・グラウンディング・ツール定義・サブエージェント連携まで網羅。Go言語での具体的なコード例を交えており、LangGraphに相当するGoogle製フレームワークの全体像を把握できる内容。

## 要点

- ADKはgenai SDKの上に構築された高レベルフレームワークで、セッション管理・ツールオーケストレーション・マルチエージェント連携・コールバックを提供する
- エージェントとフロントエンドの通信はREST APIではなくSSEベースのイベントストリーミングが適切で、AG-UIプロトコルが標準化を担う
- 会話のブランチ（編集してリトライ）はADKのrewindメカニズムで実現でき、巻き戻されたイベントは監査目的で履歴に保持される
## 関連記事

- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装
- /deep_260 Learn Your Way: 生成AIによる教科書の再構想
- /deep_1474 GoのAIフレームワーク「Eino」を徹底解説！LangChainGoとの実測比較も

## 原文リンク

[AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築](https://ymmt.hatenablog.com/entry/2026/03/24/221754)
