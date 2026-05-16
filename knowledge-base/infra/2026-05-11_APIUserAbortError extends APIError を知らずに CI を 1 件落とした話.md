---
title: "APIUserAbortError extends APIError を知らずに CI を 1 件落とした話"
url: "https://zenn.dev/iori_001/articles/openai-apierror-instanceof-trap"
date: 2026-05-11
tags: [OpenAI SDK, TypeScript, instanceof, エラーハンドリング, CI, APIUserAbortError, APIError]
category: "infra"
related: [4333, 3898, 3095, 3947, 2962]
memo: "[Zenn LLM] APIUserAbortError extends APIError を知らずに CI を 1 件落とした話"
processed_at: "2026-05-11T12:40:12.315691"
---

## 要約

OpenAI SDK の error class 継承構造を見落とした結果、TypeScript の instanceof チェック順序が誤り、CI テストが 1 件失敗した実例。

著者は AI ゲーム生成サービスの内部コンポーネント「prompt-rewriter」を実装していた。Sonnet 4.6 を使い、ユーザーの自然言語ゲーム指示を Anthropic 向け XML+CoT と OpenAI 向け短文の 2 variants に変換する処理で、per-call timeout 5 秒・raw prompt へのフォールバック設計を採用。エラー分類は (1) parent abort → throw、(2) per-call timeout → TIMEOUT 警告、(3) 5xx/429 → TRANSIENT 警告、(4) 401/403/その他 4xx → throw の 4 段階。

問題は catch ブロックの分岐順序。`if (err instanceof APIError)` を `if (err instanceof APIUserAbortError)` より先に書いていた。OpenAI SDK では APIUserAbortError は APIError のサブクラスであるため、abort エラーが APIError ブランチに先に捕捉される。status プロパティが undefined → 0 になるため、401/403/4xx の throw 条件をすり抜け、最終的に TRANSIENT の rawFallback に流れた。結果、per-call timeout テストで期待値 `rewrite-timeout` に対し実際値 `rewrite-transient` が返り CI fail。

ローカルでは pnpm typecheck・lint・format・build がすべて green だった。Cloudflare Workers の sandbox 制約でローカルテストが走らないプロジェクトだったため CI 任せで運用しており、30 分ほど原因不明だった。

修正は 2 ブロックの入れ替えのみ。順序を「parent abort signal → APIUserAbortError → APIError → 未知 Error」に変更し、CI が緑になった。

教訓は 3 点。(1) instanceof チェックはサブクラス → 親クラスの順が基本。外部 SDK のクラス継承構造は名前からは分からないため、SDK 採用時に error class の継承図を最初に確認する。(2) テストでは素の Error ではなく実 SDK の error class を使う。(3) typecheck・lint・build が通っても意味の正しさはテストしか検証できない。

同様の罠は Anthropic SDK（APIError 配下に BadRequestError 等）、AWS SDK v3（ServiceException 配下）、Stripe SDK（StripeError 配下）でも存在する。SDK 横断で共通するアンチパターンである。

## アイデア

- 外部 SDK の error class 継承構造は名前から推測できないため、SDK 採用時に継承図をドキュメント化しておく習慣が CI fail を未然に防ぐ
- typecheck・lint・build が全部 green でも『意味の正しさ』はテストでしか検証できない点は、型安全言語の限界を示すケーススタディとして示唆深い
- status === 0 というセンチネル値が abort エラーと 5xx を同じ分岐に引き込む構造は、status ベース分岐より class ベース分岐を優先すべき理由を明示している

## 前提知識

- **TypeScript instanceof** (TODO: 読むべき)
- **OpenAI SDK error classes** (TODO: 読むべき)
- **プロトタイプ継承** (TODO: 読むべき)
- **AbortController / AbortSignal** (TODO: 読むべき)
- **CI テスト** (TODO: 読むべき)

## 関連記事

- /deep_4333 Parse Guard：LLMアプリに「読んだつもり」をさせない入力検証パターン
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_3095 伏線エンジンの設計 — 計画的伏線とAI自動生成を両立させる
- /deep_3947 pi-mono：完成品AIコーディングツールではなく、自作エージェント基盤として見ると強い
- /deep_2962 Windows上のLLMとxangiを接続し、BOT同士で会話させる

## 原文リンク

[APIUserAbortError extends APIError を知らずに CI を 1 件落とした話](https://zenn.dev/iori_001/articles/openai-apierror-instanceof-trap)
