---
title: "Claude Fable 5 を API 視点で読み解く — Opus 4.8 から何が変わったのか"
url: "https://zenn.dev/aiden_ai/articles/00fd9f3839b548"
date: 2026-06-12
tags: [Claude Fable 5, Anthropic API, breaking changes, extended thinking, output_config.effort, protected thinking, refusal handling, tokenizer, fallback, ZDR]
category: "ai-ml"
related: [2953, 6276, 6839, 2248, 8059]
memo: "[Zenn 機械学習] Claude Fable 5 を API 視点で読み解く — Opus 4.8 から何が変わったのか"
processed_at: "2026-06-12T09:11:16.521095"
---

## 要約

2026年6月9日に一般提供が開始された Claude Fable 5（claude-fable-5）の、API開発者向けの破壊的変更と実装パターンをまとめた記事。Fable 5 の優位性は「難しく・長時間・自律的なタスク」に集中しており、SWE-bench Pro で80.3%（Opus 4.8: 69.2%）、FrontierCode で29.3%（同13.4%）と長時間エージェントコーディングで顕著な差が出る一方、日常的な短いタスクでは体感差が出にくい。破壊的変更は主に5点。①思考が常時ONとなり、thinking パラメータでの無効化（disabled）や budget_tokens が廃止され、思考の深さは output_config.effort（low/medium/high/xhigh/max）で制御する。②protected thinking ポリシーにより生の思考連鎖は返却されず、display: 'summarized' で要約のみ取得可能。マルチターンでは受け取った thinking ブロックを改変せず返却する必要がある。③新トークナイザの採用により同一内容が約30%多くトークン化され、単価自体も2倍（$10/$50 per 1M tokens）なのでコスト増は実質2倍以上になり得る。count_tokens に input_tokens_prior_tokenizer フィールドが追加され移行前の差分測定が可能。④安全分類器による拒否が HTTP 200 + stop_reason: 'refusal' で返るため、content[0] を無条件に読むコードが壊れる。対処としてサーバーサイド fallbacks（beta: 'server-side-fallback-2026-06-01'）、SDKミドルウェア（BetaRefusalFallbackMiddleware）、手組みリトライの3方式が提供される。⑤ゼロデータ保持（ZDR）が不可で30日データ保持が必須。組織の保持設定が短い場合は正常なリクエストも400エラーになる。またアシスタント prefill も400エラーとなり、structured outputs（output_config.format）への置き換えが必要。実装上のベストプラクティスとして、タスク全体を最初の1ターンで渡してhigh〜xhigh effortで実行し、単発リクエストが数分〜15分走ることを前提に非同期ストリーミング設計にすることが推奨されている。監査エージェント開発では、長時間自律実行・stop_reason ハンドリング・fallback 設計が直接適用できる。

## アイデア

- 思考の深さ制御を budget_tokens から effort レベル（low〜max）の定性指定に変更したことで、開発者はトークン数ではなくタスク難度の意図を直接指定できる設計になっている
- stop_reason: 'refusal' が HTTP 200 で返るという設計は、クライアント側のエラーハンドリングパターン自体を再設計させる。ステータスコードではなくレスポンスボディの構造検査が必須になる
- サーバーサイド fallbacks により、拒否発生時の別モデルへの切り替えをクライアントロジックなしで実現できる点は、マルチモデル構成のエージェントシステム設計に直接応用可能

## 前提知識

- **Claude extended thinking** (TODO: 読むべき)
- **Anthropic Messages API** (TODO: 読むべき)
- **stop_reason** → /deep_3504 harness engineering を5層で整理する — Pythonで1から書いて見えたこと
- **tokenizer** → /deep_5963 HTMLファーストAI駆動開発 — Markdown一択論の4盲点
- **structured outputs** → /deep_6485 LLMワークフローにおける決定論という罠

## 関連記事

- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_6276 製造業RAGの本番運用設計：Evals・Observability・Prompt Versioning・Fallback【コード付き】
- /deep_6839 エンジニアが最低限押さえたいLLMの基礎知識
- /deep_2248 【LLM基礎】トークンとは何か？トークナイザーの仕組みと日本語のコスト特性
- /deep_8059 「有意差なし ≠ 差なし」をClaude Fable 5は理解しているか――設計書レビューで見えたOpus 4.8との差

## 原文リンク

[Claude Fable 5 を API 視点で読み解く — Opus 4.8 から何が変わったのか](https://zenn.dev/aiden_ai/articles/00fd9f3839b548)
