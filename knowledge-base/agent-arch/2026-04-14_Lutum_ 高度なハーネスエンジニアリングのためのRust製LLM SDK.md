---
title: "Lutum: 高度なハーネスエンジニアリングのためのRust製LLM SDK"
url: "https://zenn.dev/ryo33/articles/lutum-introduction"
date: 2026-04-14
tags: [Rust, LLM SDK, ハーネスエンジニアリング, Hooks, 型駆動開発, マルチターン, Tool呼び出し, Telemetry, エージェント制御]
category: "agent-arch"
related: [94, 1251, 41, 1788, 771]
memo: "[Zenn LLM] Lutum: 高度なハーネスエンジニアリングのための Rust製 LLM SDK"
processed_at: "2026-04-14T12:24:46.536702"
---

## 要約

LutumはRust製のLLM SDKで、「エージェント抽象を排除することでエージェント実装をシンプルにする」という設計思想に基づいている。開発者のRyo氏が注意スキーマ理論に基づく人工意識の再現を目標に開発を開始し、既存のフレームワーク（LangGraph等）が「高度な制御とメンテナンス性の両立」を解決できないと判断して独自SDKを設計した。

主な設計原則は4つ。①Rustの型システムとマクロを最大活用（ツール定義から JsonSchema・LLM API記述を自動生成、構造化出力も型駆動）。②ユーザーから制御を奪わない（フレームワーク側の自動ループ・状態管理なし、while/if/break等を直接記述可能）。③プロバイダ固有機能を共通抽象で潰さない（キャッシュ範囲指定やレスポンス情報の差異をViewとして保持し、Sessionの完全永続化を実現）。④アプリコードが特定プロバイダを意識しない（ExtensionシステムとHooksでLLM Provider Adapterを注入し、モデル選択ロジックも同じ仕組みで外部化）。

主要機能として、マルチターンAPI（Session::new → push_system/push_user → text_turn）、Completion API、型駆動・関数定義駆動のToolset（#[lutum::tool_fn]/#[lutum::tool_input]マクロ）、Hooksシステム（traitライクなインターフェースでシステムプロンプト・ツール呼び出しバリデーション等を注入可能）、Telemetry（tracingおよびlutum-traceライブラリによるAgent動作収集と評価）、予算管理（Budget Manager + Request Extensionsによるトークン消費追跡）を提供する。

動作確認済みの実装としてClaude AdapterでSQLiteを操作するTUIエージェント（demo-apps/sqlite）があり、lutum-eval + lutum-traceによる評価も実施済み。OpenAI adapter経由でvLLM/OpenRouterへの接続も確認済み。監査エージェント開発への示唆として、Hooksによるツール呼び出しの検証ロジック（空入力拒否・架空地名ブロック等）の多重登録パターンは、監査手続きのバリデーション層を型安全に実装する際に直接応用可能。またSessionの完全永続化と侵襲的評価（実行中にHooksで動作介入）は、監査ログの完全性保証とリアルタイム監視に対応できる設計である。

## アイデア

- 「エージェント抽象をやめることでエージェント実装がシンプルになる」という逆説的設計思想：フレームワークによる自動ループ・状態管理を排除し、Rustの制御構文（while/if/break）をそのまま使うことで、ローカル変数による軽量な状態管理と高度な分岐ロジックを型安全に実現できる
- Hooksシステムによる多段バリデーション：ツール呼び出し時に複数のHook実装（RejectBlankCity、RejectAtlantis等）をチェーン登録し、Runtime時にバリデーション数を調整できる設計は、監査エージェントの手続きチェック層として直接転用可能
- プロバイダ固有レスポンスをViewパターンで抽象化：各LLMプロバイダのキャッシュ範囲指定や差分情報をそのまま保持しつつ、横断的な共通Viewを提供することで、APIレベルのキャッシュ最適化を損なわずにプロバイダ非依存コードを書ける設計

## 前提知識

- **Rust型システム・マクロ** (TODO: 読むべき)
- **LLM Tool Calling** (TODO: 読むべき)
- **Chat Completions API** (TODO: 読むべき)
- **エージェントループ制御** (TODO: 読むべき)
- **OpenTelemetry / tracing** (TODO: 読むべき)

## 関連記事

- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_1251 マルチターン医療診断のベンチマーク：保留・誘惑・自己修正（MINT）
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素
- /deep_771 チャンクからブロックへ：Hugging Face Hubにおけるアップロード・ダウンロードの高速化

## 原文リンク

[Lutum: 高度なハーネスエンジニアリングのためのRust製LLM SDK](https://zenn.dev/ryo33/articles/lutum-introduction)
