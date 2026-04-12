---
title: "LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装"
url: "https://zenn.dev/acntechjp/articles/efcc4f224cc8ca"
date: 2026-03-29
tags: [長期記憶, SQLite, sentence-transformers, RAG, MCP, Claude Code, エピソード記憶, ベクトル検索, 忘却曲線, エージェント記憶]
category: "agent-arch"
memo: "LLMに長期記憶を実装する"
related: [68, 1242, 430, 1470, 1247]
processed_at: "2026-03-29T21:56:24.467127"
---

## 要約

Claude Code（Anthropic CLI）に人間の脳の記憶メカニズムを模倣した長期記憶システムを実装する手法を解説。SQLite + sentence-transformers（multilingual-e5-small）を用い、情動ゲーティング（扁桃体）、エビングハウス忘却曲線、連想ネットワーク（拡散活性化）、再固定化、干渉忘却、フラッシュバック（プルースト効果）、気分状態依存記憶、睡眠中の海馬リプレイ・統合、再構成的想起、予期記憶、スキーマ生成など16のメカニズムをPythonで実装。記憶の検索スコアは類似度・情動強度・鮮度・アクセス頻度・プライミング・時間帯・気分の7因子の積で算出。LLMへの返却は完全テキストではなくキーワード断片のみとし、LLMが文脈に応じて再構成する設計。Bron-KerboschアルゴリズムによるクリークからスキーマをMCPサーバー経由でClaude Codeに接続する構成を採用。

## 要点

- 記憶検索スコアを7因子（類似度・情動・鮮度・アクセス頻度・プライミング・時間帯・気分）の積で補正することで、文脈依存的な想起を実現している
- LLMへの返却をキーワード断片のみにすることで再構成的想起を模倣し、同一クエリでも時間・気分・乱数により毎回異なる結果を返す設計になっている
- 睡眠（/sleepコマンド）でクラスタリング・統合・スキーマ生成を実行し、エピソード記憶から意味記憶への昇華をBron-Kerboschアルゴリズムで自動化している
## 関連記事

- /deep_68 Claudeは明日もあなたを忘れる — MCP Memory Server cpersona 設計と実践
- /deep_1242 AI AgentメモリーOSS「MemPalace」徹底解説 — 記憶の宮殿アーキテクチャとベンチマーク論争
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_1470 ベクトル検索は不要なのか――従来RAGとAgentic RAG・階層的検索の使い分け
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷

## 原文リンク

[LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装](https://zenn.dev/acntechjp/articles/efcc4f224cc8ca)
